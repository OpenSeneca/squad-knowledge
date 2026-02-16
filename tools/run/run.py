#!/usr/bin/env python3
"""
run — Command Runner and Launcher

Store, organize, and run frequently used commands with names, tags, and descriptions.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class CommandRunner:
    """Manage and run stored commands."""

    def __init__(self):
        self.config_dir = Path.home() / '.run'
        self.commands_file = self.config_dir / 'commands.json'
        self.history_file = self.config_dir / 'history.jsonl'

        self._ensure_config()

    def _ensure_config(self):
        """Ensure config directory and files exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if not self.commands_file.exists():
            self._write_commands({})
        if not self.history_file.exists():
            self.history_file.touch()

    def _read_commands(self) -> Dict[str, Any]:
        """Read commands from storage."""
        try:
            with open(self.commands_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_commands(self, commands: Dict[str, Any]):
        """Write commands to storage."""
        with open(self.commands_file, 'w') as f:
            json.dump(commands, f, indent=2)

    def _add_to_history(self, name: str, command: str, success: bool):
        """Add command to history."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'command': command,
            'success': success
        }
        with open(self.history_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def add(self, name: str, cmd: List[str], description: str = '',
            tags: List[str] = None, group: str = None):
        """Add a new command."""
        commands = self._read_commands()

        if name in commands:
            print(f"❌ Command '{name}' already exists. Use --force to overwrite.")
            return False

        # Join command parts into a single string
        command_str = ' '.join(cmd)

        commands[name] = {
            'command': command_str,
            'description': description,
            'tags': tags or [],
            'group': group or 'default',
            'created': datetime.now().isoformat(),
            'runs': 0
        }

        self._write_commands(commands)
        print(f"✅ Added command '{name}'")
        return True

    def remove(self, name: str):
        """Remove a command."""
        commands = self._read_commands()

        if name not in commands:
            print(f"❌ Command '{name}' not found")
            return False

        del commands[name]
        self._write_commands(commands)
        print(f"✅ Removed command '{name}'")
        return True

    def list(self, group: str = None, tags: List[str] = None):
        """List all commands, optionally filtered."""
        commands = self._read_commands()

        if not commands:
            print("📚 No commands stored yet")
            print("   Add one with: run add <name> <command>")
            return

        # Filter commands
        filtered = {}
        for name, cmd in commands.items():
            if group and cmd.get('group') != group:
                continue
            if tags and not any(tag in cmd.get('tags', []) for tag in tags):
                continue
            filtered[name] = cmd

        if not filtered:
            print("📚 No commands match filters")
            return

        # Group by group name
        groups = {}
        for name, cmd in sorted(filtered.items()):
            group_name = cmd.get('group', 'default')
            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append((name, cmd))

        print(f"📚 {len(filtered)} command(s):")
        print()

        for group_name, items in sorted(groups.items()):
            print(f"  📁 {group_name}:")
            for name, cmd in items:
                tags_str = ' '.join([f'[{t}]' for t in cmd.get('tags', [])])
                desc = f" — {cmd.get('description', '')}" if cmd.get('description') else ''
                print(f"    • {name} {tags_str}{desc}")
            print()

    def show(self, name: str):
        """Show command details."""
        commands = self._read_commands()

        if name not in commands:
            print(f"❌ Command '{name}' not found")
            return False

        cmd = commands[name]
        print(f"📝 Command: {name}")
        print()
        print(f"  Command: {cmd['command']}")
        print(f"  Description: {cmd.get('description', 'None')}")
        print(f"  Group: {cmd.get('group', 'default')}")
        print(f"  Tags: {', '.join(cmd.get('tags', [])) or 'None'}")
        print(f"  Runs: {cmd.get('runs', 0)}")
        print(f"  Created: {cmd.get('created', 'Unknown')}")
        return True

    def run(self, name: str, dry_run: bool = False, shell: bool = True):
        """Run a stored command."""
        commands = self._read_commands()

        if name not in commands:
            print(f"❌ Command '{name}' not found")
            return False

        cmd_data = commands[name]
        command = cmd_data['command']

        print(f"🚀 Running: {name}")
        print(f"   Command: {command}")
        print()

        if dry_run:
            print("🔍 Dry run (not executing)")
            return True

        try:
            result = subprocess.run(
                command,
                shell=shell,
                check=True,
                capture_output=False,
                text=True
            )
            success = result.returncode == 0
            self._add_to_history(name, command, success)

            # Update run count
            cmd_data['runs'] = cmd_data.get('runs', 0) + 1
            commands[name] = cmd_data
            self._write_commands(commands)

            if success:
                print(f"✅ Command '{name}' completed")
            return success

        except subprocess.CalledProcessError as e:
            self._add_to_history(name, command, False)
            print(f"❌ Command failed with exit code {e.returncode}")
            return False

    def search(self, query: str):
        """Search commands by name, description, or command."""
        commands = self._read_commands()
        query = query.lower()

        results = []
        for name, cmd in commands.items():
            if (query in name.lower() or
                query in cmd.get('description', '').lower() or
                query in cmd.get('command', '').lower()):
                results.append((name, cmd))

        if not results:
            print(f"🔍 No results for '{query}'")
            return

        print(f"🔍 {len(results)} result(s) for '{query}':")
        print()
        for name, cmd in results:
            tags_str = ' '.join([f'[{t}]' for t in cmd.get('tags', [])])
            desc = f" — {cmd.get('description', '')}" if cmd.get('description') else ''
            print(f"  • {name} {tags_str}{desc}")

    def groups(self):
        """List all command groups."""
        commands = self._read_commands()

        groups = {}
        for name, cmd in commands.items():
            group_name = cmd.get('group', 'default')
            if group_name not in groups:
                groups[group_name] = 0
            groups[group_name] += 1

        if not groups:
            print("📁 No groups yet")
            return

        print("📁 Groups:")
        for group_name, count in sorted(groups.items()):
            print(f"  • {group_name}: {count} command(s)")

    def history(self, limit: int = 10):
        """Show recent command history."""
        if not self.history_file.exists() or self.history_file.stat().st_size == 0:
            print("📜 No command history yet")
            return

        entries = []
        with open(self.history_file, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue

        if not entries:
            print("📜 No command history yet")
            return

        # Sort by timestamp (newest first) and limit
        entries.sort(key=lambda x: x['timestamp'], reverse=True)
        entries = entries[:limit]

        print(f"📜 Recent command history (last {min(limit, len(entries))}):")
        print()

        for entry in entries:
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
            status = '✅' if entry['success'] else '❌'
            print(f"  {status} {timestamp} — {entry['name']}")
            print(f"     {entry['command']}")
            print()

    def export(self, output_file: str):
        """Export commands to JSON file."""
        commands = self._read_commands()
        output_path = Path(output_file)

        with open(output_path, 'w') as f:
            json.dump(commands, f, indent=2)

        print(f"✅ Exported {len(commands)} command(s) to {output_path}")

    def import_commands(self, input_file: str, merge: bool = False):
        """Import commands from JSON file."""
        input_path = Path(input_file)

        if not input_path.exists():
            print(f"❌ File not found: {input_file}")
            return False

        with open(input_path, 'r') as f:
            imported = json.load(f)

        existing = self._read_commands()

        if merge:
            # Merge: existing commands take precedence
            for name, cmd in imported.items():
                if name not in existing:
                    existing[name] = cmd
            print(f"✅ Merged {len(imported)} command(s), added {len(imported) - len(set(existing.keys()) & set(imported.keys()))} new")
        else:
            # Replace: imported commands take precedence
            existing = imported
            print(f"✅ Imported {len(imported)} command(s)")

        self._write_commands(existing)
        return True


def main():
    parser = argparse.ArgumentParser(
        description='run — Command Runner and Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  run add deploy-dev "npm run build && ./deploy.sh dev" -d "Deploy to dev env" -g deployment
  run list
  run list -g deployment
  run list -t docker
  run show deploy-dev
  run deploy-dev
  run run deploy-dev --dry-run
  run search deploy
  run history
  run export commands-backup.json
  run import commands-backup.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new command')
    add_parser.add_argument('name', help='Command name')
    add_parser.add_argument('cmd', nargs='+', help='Shell command to run')
    add_parser.add_argument('-d', '--description', default='', help='Description')
    add_parser.add_argument('-t', '--tags', nargs='*', default=[], help='Tags')
    add_parser.add_argument('-g', '--group', default='default', help='Group name')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a command')
    remove_parser.add_argument('name', help='Command name')

    # List command
    list_parser = subparsers.add_parser('list', help='List commands')
    list_parser.add_argument('-g', '--group', help='Filter by group')
    list_parser.add_argument('-t', '--tags', nargs='*', help='Filter by tags')

    # Show command
    show_parser = subparsers.add_parser('show', help='Show command details')
    show_parser.add_argument('name', help='Command name')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run a stored command')
    run_parser.add_argument('name', help='Command name')
    run_parser.add_argument('--dry-run', action='store_true', help='Show command without executing')
    run_parser.add_argument('--no-shell', action='store_true', help='Don\'t use shell (direct execution)')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search commands')
    search_parser.add_argument('query', help='Search query')

    # Groups command
    subparsers.add_parser('groups', help='List command groups')

    # History command
    history_parser = subparsers.add_parser('history', help='Show command history')
    history_parser.add_argument('-n', '--limit', type=int, default=10, help='Number of entries')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export commands')
    export_parser.add_argument('file', help='Output file')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import commands')
    import_parser.add_argument('file', help='Input file')
    import_parser.add_argument('--merge', action='store_true', help='Merge with existing commands')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    runner = CommandRunner()

    if args.command == 'add':
        runner.add(args.name, args.cmd, args.description, args.tags, args.group)

    elif args.command == 'remove':
        runner.remove(args.name)

    elif args.command == 'list':
        runner.list(args.group, args.tags)

    elif args.command == 'show':
        runner.show(args.name)

    elif args.command == 'run':
        runner.run(args.name, args.dry_run, not args.no_shell)

    elif args.command == 'search':
        runner.search(args.query)

    elif args.command == 'groups':
        runner.groups()

    elif args.command == 'history':
        runner.history(args.limit)

    elif args.command == 'export':
        runner.export(args.file)

    elif args.command == 'import':
        runner.import_commands(args.file, args.merge)

    return 0


if __name__ == '__main__':
    sys.exit(main())
