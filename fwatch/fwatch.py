#!/usr/bin/env python3
"""
watch — File Watcher and Runner

Watch files and directories for changes, then run commands automatically.
Perfect for development workflows: tests, builds, linters, servers.

Uses polling (no external dependencies required).
"""

import os
import sys
import argparse
import subprocess
import time
import signal
import threading
from pathlib import Path
from typing import List, Dict, Set, Optional, Callable
import json
from datetime import datetime


class WatcherConfig:
    """Watcher configuration."""

    def __init__(self):
        self.watch_dirs: List[str] = []
        self.watch_patterns: List[str] = []
        self.exclude_patterns: List[str] = []
        self.command: str = ''
        self.on_create: str = ''
        self.on_modify: str = ''
        self.on_delete: str = ''
        self.on_move: str = ''
        self.debounce_ms: int = 300
        self.poll_interval: float = 1.0
        self.recurse: bool = True
        self.oneshot: bool = False
        self.initial_run: bool = False
        self.show_events: bool = False
        self.log_file: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'watch_dirs': self.watch_dirs,
            'watch_patterns': self.watch_patterns,
            'exclude_patterns': self.exclude_patterns,
            'command': self.command,
            'on_create': self.on_create,
            'on_modify': self.on_modify,
            'on_delete': self.on_delete,
            'on_move': self.on_move,
            'debounce_ms': self.debounce_ms,
            'poll_interval': self.poll_interval,
            'recurse': self.recurse,
            'oneshot': self.oneshot,
            'initial_run': self.initial_run,
            'show_events': self.show_events,
            'log_file': self.log_file,
        }


class FileInfo:
    """File information for change detection."""

    def __init__(self, path: str):
        self.path = path
        self.mtime = 0.0
        self.size = 0
        self.exists = False
        self.update()

    def update(self):
        """Update file information."""
        try:
            stat = os.stat(self.path)
            self.mtime = stat.st_mtime
            self.size = stat.st_size
            self.exists = True
        except (OSError, FileNotFoundError):
            self.exists = False

    def changed(self, other: 'FileInfo') -> bool:
        """Check if file changed."""
        return (
            self.exists != other.exists or
            self.mtime != other.mtime or
            self.size != other.size
        )


class ChangeHandler:
    """Handle file system events."""

    def __init__(self, config: WatcherConfig, log_callback: Optional[Callable] = None):
        self.config = config
        self.log_callback = log_callback
        self.last_change = 0
        self.file_states: Dict[str, FileInfo] = {}
        self.stop_flag = False
        self.lock = threading.Lock()

    def log(self, message: str):
        """Log message."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_line = f"[{timestamp}] {message}"
        print(log_line)

        if self.log_callback:
            self.log_callback(log_line)

        if self.config.log_file:
            try:
                with open(self.config.log_file, 'a') as f:
                    f.write(f"{log_line}\n")
            except Exception as e:
                print(f"⚠️ Failed to write to log file: {e}", file=sys.stderr)

    def should_process(self, path: str) -> bool:
        """Check if event should be processed."""
        # Check patterns
        if self.config.watch_patterns:
            path_obj = Path(path)
            match = False
            for pattern in self.config.watch_patterns:
                if pattern.startswith('.') and path_obj.suffix == pattern:
                    match = True
                    break
                elif pattern in path:
                    match = True
                    break
            if not match:
                return False

        # Check exclusions
        if self.config.exclude_patterns:
            for pattern in self.config.exclude_patterns:
                if pattern in path:
                    return False

        return True

    def _should_run(self) -> bool:
        """Check if command should run (debounce)."""
        now = time.time()
        elapsed = (now - self.last_change) * 1000

        if elapsed >= self.config.debounce_ms:
            self.last_change = now
            return True
        return False

    def _run_command(self, command: str, event_type: str, path: str):
        """Run command."""
        if not command:
            return

        # Wait for debounce
        if not self._should_run():
            if self.config.show_events:
                self.log(f"⏳ Debouncing: {path}")
            return

        self.log(f"🚀 Running: {command}")

        try:
            # Run command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.stdout:
                print(result.stdout)

            if result.stderr:
                print(result.stderr, file=sys.stderr)

            if result.returncode == 0:
                self.log(f"✅ {event_type} command succeeded")
            else:
                self.log(f"❌ {event_type} command failed (exit {result.returncode})")

        except subprocess.TimeoutExpired:
            self.log(f"⏰ Command timed out")
        except Exception as e:
            self.log(f"❌ Command error: {e}")

        if self.config.oneshot:
            self.stop_flag = True

    def handle_change(self, path: str, old_info: FileInfo, new_info: FileInfo):
        """Handle file change."""
        if not self.should_process(path):
            return

        is_dir = os.path.isdir(path) if os.path.exists(path) else False

        # Detect event type
        if old_info.exists and not new_info.exists:
            event_type = 'delete'
            if self.config.show_events:
                self.log(f"🗑️ File deleted: {path}")
            command = self.config.on_delete
        elif not old_info.exists and new_info.exists:
            event_type = 'create'
            if self.config.show_events:
                self.log(f"📄 File created: {path}")
            command = self.config.on_create
        else:
            event_type = 'modify'
            if self.config.show_events:
                self.log(f"📝 File modified: {path}")
            command = self.config.on_modify

        # Run command
        if command:
            self._run_command(command, event_type, path)
        elif self.config.command:
            self._run_command(self.config.command, event_type, path)


class FileWatcher:
    """File watcher and runner (polling-based)."""

    def __init__(self, config: WatcherConfig):
        self.config = config
        self.handler = ChangeHandler(config, self._log_to_file)
        self.log_history: List[str] = []

    def _log_to_file(self, message: str):
        """Log to history."""
        self.log_history.append(message)
        if len(self.log_history) > 1000:
            self.log_history = self.log_history[-1000:]

    def _scan_directory(self, directory: str) -> Dict[str, FileInfo]:
        """Scan directory and return file information."""
        file_map = {}

        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    file_map[filepath] = FileInfo(filepath)
                except Exception:
                    pass

            if not self.config.recurse:
                break

        return file_map

    def start(self):
        """Start watching."""
        # Determine directories to watch
        watch_dirs = self.config.watch_dirs if self.config.watch_dirs else [os.getcwd()]

        # Build watch paths
        watch_paths = []
        for dir_path in watch_dirs:
            dir_path = os.path.abspath(dir_path)
            if os.path.exists(dir_path):
                watch_paths.append(dir_path)
                print(f"📁 Watching: {dir_path}")
            else:
                print(f"⚠️ Directory not found: {dir_path}")

        if not watch_paths:
            print("❌ No valid directories to watch")
            return 1

        # Initial scan
        print("\n📡 Scanning initial state...")
        for dir_path in watch_paths:
            file_map = self._scan_directory(dir_path)
            self.handler.file_states.update(file_map)

        print(f"   Found {len(self.handler.file_states)} files")

        # Initial run if requested
        if self.config.initial_run and self.config.command:
            print(f"\n🚀 Initial run: {self.config.command}")
            subprocess.run(self.config.command, shell=True)

        # Start watching
        print(f"\n👀 Watching for changes...")
        print(f"   Patterns: {', '.join(self.config.watch_patterns) if self.config.watch_patterns else 'all files'}")
        print(f"   Excludes: {', '.join(self.config.exclude_patterns) if self.config.exclude_patterns else 'none'}")
        print(f"   Debounce: {self.config.debounce_ms}ms")
        print(f"   Poll interval: {self.config.poll_interval}s")
        if self.config.oneshot:
            print(f"   Mode: oneshot (will stop after first run)")
        print(f"\nPress Ctrl+C to stop\n")

        # Set up signal handler
        def signal_handler(sig, frame):
            print("\n\n⏹️ Stopping watcher...")
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        # Main loop
        try:
            while not self.handler.stop_flag:
                time.sleep(self.config.poll_interval)

                # Scan directories
                current_states = {}
                for dir_path in watch_paths:
                    current_states.update(self._scan_directory(dir_path))

                # Compare and detect changes
                all_paths = set(self.handler.file_states.keys()) | set(current_states.keys())

                for path in all_paths:
                    old_info = self.handler.file_states.get(path)
                    new_info = current_states.get(path)

                    if old_info and new_info:
                        if old_info.changed(new_info):
                            self.handler.handle_change(path, old_info, new_info)
                    elif old_info and not new_info:
                        # File deleted
                        deleted_info = FileInfo(path)
                        deleted_info.exists = False
                        self.handler.handle_change(path, old_info, deleted_info)
                    elif not old_info and new_info:
                        # File created
                        self.handler.handle_change(path, FileInfo(path), new_info)

                # Update states
                self.handler.file_states = current_states

        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

        return 0

    def stop(self):
        """Stop watching."""
        self.handler.stop_flag = True

    def save_config(self, filepath: str):
        """Save configuration to file."""
        with open(filepath, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=2)

    @staticmethod
    def load_config(filepath: str) -> WatcherConfig:
        """Load configuration from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        config = WatcherConfig()
        config.watch_dirs = data.get('watch_dirs', [])
        config.watch_patterns = data.get('watch_patterns', [])
        config.exclude_patterns = data.get('exclude_patterns', [])
        config.command = data.get('command', '')
        config.on_create = data.get('on_create', '')
        config.on_modify = data.get('on_modify', '')
        config.on_delete = data.get('on_delete', '')
        config.on_move = data.get('on_move', '')
        config.debounce_ms = data.get('debounce_ms', 300)
        config.poll_interval = data.get('poll_interval', 1.0)
        config.recurse = data.get('recurse', True)
        config.oneshot = data.get('oneshot', False)
        config.initial_run = data.get('initial_run', False)
        config.show_events = data.get('show_events', False)
        config.log_file = data.get('log_file', None)

        return config


def main():
    parser = argparse.ArgumentParser(
        description='watch — File Watcher and Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  watch --command "pytest"
  watch --patterns ".py" --command "pytest"
  watch --command "npm run build" --exclude node_modules
  watch -p ".js,.ts,.jsx,.tsx" -c "npm test" --initial-run
  watch -p ".md" --command "make docs"
  watch --oneshot -p ".py" -c "pytest" --initial-run

Common Use Cases:
  - Auto-run tests on code changes
  - Auto-build on source changes
  - Auto-format/lint on save
  - Auto-restart servers
  - Auto-generate documentation
        """
    )

    # Directories to watch
    parser.add_argument('-d', '--dir', action='append', help='Directory to watch (can repeat)')
    parser.add_argument('-p', '--patterns', help='File patterns to watch (comma-separated)')
    parser.add_argument('-x', '--exclude', help='Patterns to exclude (comma-separated)')

    # Commands
    parser.add_argument('-c', '--command', help='Command to run on any change')
    parser.add_argument('--on-create', help='Command to run on file creation')
    parser.add_argument('--on-modify', help='Command to run on file modification')
    parser.add_argument('--on-delete', help='Command to run on file deletion')
    parser.add_argument('--on-move', help='Command to run on file move/rename')

    # Options
    parser.add_argument('--debounce', type=int, default=300,
                    help='Debounce time in milliseconds (default: 300)')
    parser.add_argument('--poll', type=float, default=1.0,
                    help='Poll interval in seconds (default: 1.0)')
    parser.add_argument('--no-recurse', action='store_true',
                    help='Do not watch subdirectories')
    parser.add_argument('--oneshot', action='store_true',
                    help='Run once and exit')
    parser.add_argument('--initial-run', action='store_true',
                    help='Run command on start')
    parser.add_argument('--show-events', action='store_true',
                    help='Show all file events')
    parser.add_argument('--log-file', help='Log to file')

    # Config
    parser.add_argument('--save-config', help='Save configuration to file')
    parser.add_argument('--load-config', help='Load configuration from file')

    args = parser.parse_args()

    # Load or create config
    if args.load_config:
        config = FileWatcher.load_config(args.load_config)
    else:
        config = WatcherConfig()

        # Apply command line args
        if args.dir:
            config.watch_dirs = args.dir
        if args.patterns:
            config.watch_patterns = [p.strip() for p in args.patterns.split(',')]
        if args.exclude:
            config.exclude_patterns = [p.strip() for p in args.exclude.split(',')]
        if args.command:
            config.command = args.command
        if args.on_create:
            config.on_create = args.on_create
        if args.on_modify:
            config.on_modify = args.on_modify
        if args.on_delete:
            config.on_delete = args.on_delete
        if args.on_move:
            config.on_move = args.on_move

    # Apply options
    if args.debounce:
        config.debounce_ms = args.debounce
    if args.poll:
        config.poll_interval = args.poll
    if args.no_recurse:
        config.recurse = False
    if args.oneshot:
        config.oneshot = True
    if args.initial_run:
        config.initial_run = True
    if args.show_events:
        config.show_events = True
    if args.log_file:
        config.log_file = args.log_file

    # Save config if requested
    if args.save_config:
        watcher = FileWatcher(config)
        watcher.save_config(args.save_config)
        print(f"✅ Configuration saved to: {args.save_config}")
        return 0

    # Start watching
    watcher = FileWatcher(config)
    return watcher.start()


if __name__ == '__main__':
    sys.exit(main())
