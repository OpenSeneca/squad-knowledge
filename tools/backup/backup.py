#!/usr/bin/env python3
"""
backup - Configuration and Key Backup Tool

Automate backups of SSH keys, configs, and important workspace files.

Usage:
  backup create <name>            # Create a backup with given name
  backup list                     # List all backups
  backup restore <name>            # Restore from backup
  backup status                    # Show backup status
  backup auto                     # Auto backup with timestamp
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Configuration
BACKUP_DIR = Path.home() / '.backup'
BACKUP_INDEX = BACKUP_DIR / 'index.json'
BACKUP_LOG = BACKUP_DIR / 'backup.log'


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def print_color(color, text):
    """Print colored text."""
    print(f"{color}{text}{Colors.RESET}")


def init_backup_system():
    """Initialize backup system."""
    BACKUP_DIR.mkdir(exist_ok=True)

    if not BACKUP_INDEX.exists():
        with open(BACKUP_INDEX, 'w') as f:
            json.dump([], f)

    if not BACKUP_LOG.exists():
        BACKUP_LOG.touch()


def create_backup(name: str) -> bool:
    """Create a backup with specified name."""
    print_color(Colors.BOLD, f"\n📦 Creating backup: {name}")
    print("-" * 60)

    timestamp = datetime.now().isoformat()
    backup_path = BACKUP_DIR / name
    backup_path.mkdir(exist_ok=True)

    files_backed = []
    errors = []

    # Backup SSH keys
    ssh_dir = Path.home() / '.ssh'
    if ssh_dir.exists():
        print_color(Colors.CYAN, "\n🔐 Backing up SSH keys...")
        try:
            ssh_backup = backup_path / 'ssh'
            ssh_backup.mkdir(exist_ok=True)

            for item in ssh_dir.iterdir():
                if not item.name.startswith('.'):
                    dest = ssh_backup / item.name
                    shutil.copy2(item, dest)
                    files_backed.append(str(item.relative_to(Path.home())))
                    print_color(Colors.GREEN, f"  ✓ {item.name}")

        except Exception as e:
            errors.append(f"SSH keys: {e}")
            print_color(Colors.RED, f"  ✗ Failed: {e}")
    else:
        print_color(Colors.YELLOW, "⚠  No SSH directory found")

    # Backup workspace configs
    workspace = Path.home() / '.openclaw' / 'workspace'
    if workspace.exists():
        print_color(Colors.CYAN, "\n📝 Backing up workspace configs...")

        configs_to_backup = [
            'MEMORY.md',
            'USER.md',
            'IDENTITY.md',
            'HEARTBEAT.md',
        ]

        config_backup = backup_path / 'workspace'
        config_backup.mkdir(exist_ok=True)

        for config in configs_to_backup:
            source = workspace / config
            if source.exists():
                try:
                    dest = config_backup / config
                    shutil.copy2(source, dest)
                    files_backed.append(f'.openclaw/workspace/{config}')
                    print_color(Colors.GREEN, f"  ✓ {config}")
                except Exception as e:
                    errors.append(f"{config}: {e}")
                    print_color(Colors.RED, f"  ✗ Failed to backup {config}: {e}")

    # Backup tool configurations
    tools_dir = workspace / 'tools'
    if tools_dir.exists():
        print_color(Colors.CYAN, "\n🔧 Backing up tool configurations...")

        tool_backup = backup_path / 'tools'
        tool_backup.mkdir(exist_ok=True)

        # Backup tick tasks
        tick_data = Path.home() / '.tick' / 'tasks.json'
        if tick_data.exists():
            try:
                shutil.copy2(tick_data, tool_backup / 'tasks.json')
                files_backed.append('.tick/tasks.json')
                print_color(Colors.GREEN, "  ✓ tick tasks.json")
            except Exception as e:
                errors.append(f"tick tasks: {e}")

        # Backup squad status
        squad_status = Path.home() / '.squad' / 'status.json'
        if squad_status.exists():
            try:
                squad_backup_dir = tool_backup / 'squad'
                squad_backup_dir.mkdir(exist_ok=True)
                shutil.copy2(squad_status, squad_backup_dir / 'status.json')
                files_backed.append('.squad/status.json')
                print_color(Colors.GREEN, "  ✓ squad status.json")
            except Exception as e:
                errors.append(f"squad status: {e}")

        # Backup snip snippets
        snip_data = Path.home() / '.snip' / 'snippets.json'
        if snip_data.exists():
            try:
                shutil.copy2(snip_data, tool_backup / 'snippets.json')
                files_backed.append('.snip/snippets.json')
                print_color(Colors.GREEN, "  ✓ snip snippets.json")
            except Exception as e:
                errors.append(f"snip data: {e}")

    # Create backup metadata
    metadata = {
        'name': name,
        'timestamp': timestamp,
        'files_backed': files_backed,
        'errors': errors,
        'size_bytes': sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file()),
    }

    with open(backup_path / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    # Update index
    with open(BACKUP_INDEX) as f:
        backups = json.load(f)

    backups.append(metadata)
    backups.sort(key=lambda x: x['timestamp'], reverse=True)

    with open(BACKUP_INDEX, 'w') as f:
        json.dump(backups, f, indent=2)

    # Log backup
    log_entry = f"[{timestamp}] Created backup '{name}': {len(files_backed)} files, {len(errors)} errors\n"
    with open(BACKUP_LOG, 'a') as f:
        f.write(log_entry)

    # Summary
    print_color(Colors.BOLD, "\n" + "=" * 60)
    print_color(Colors.BOLD, "Backup Complete")
    print("=" * 60)

    print_color(Colors.GREEN, f"\n✓ Backed up {len(files_backed)} files")
    if errors:
        print_color(Colors.YELLOW, f"⚠ {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")

    print(f"\nLocation: {backup_path}")
    print(f"Size: {metadata['size_bytes']:,} bytes")

    return True


def list_backups():
    """List all backups."""
    print_color(Colors.BOLD, "\n📋 Available Backups")
    print("-" * 60)

    if not BACKUP_INDEX.exists():
        print_color(Colors.YELLOW, "No backups found")
        return True

    with open(BACKUP_INDEX) as f:
        backups = json.load(f)

    if not backups:
        print_color(Colors.YELLOW, "No backups found")
        return True

    print(f"\n{'Name':<30} {'Date':<20} {'Files':<10} {'Size':<15}")
    print("-" * 60)

    for backup in backups:
        name = backup['name']
        timestamp = backup['timestamp'][:10]  # YYYY-MM-DD
        files = len(backup['files_backed'])
        size = f"{backup['size_bytes'] / 1024:.1f} KB"
        errors = len(backup.get('errors', []))

        if errors > 0:
            name += " ⚠"

        print(f"{name:<30} {timestamp:<20} {files:<10} {size:<15}")

    return True


def restore_backup(name: str) -> bool:
    """Restore from a backup."""
    print_color(Colors.BOLD, f"\n🔄 Restoring backup: {name}")
    print("-" * 60)

    # Find backup
    if not BACKUP_INDEX.exists():
        print_color(Colors.RED, "No backups found")
        return False

    with open(BACKUP_INDEX) as f:
        backups = json.load(f)

    backup_info = next((b for b in backups if b['name'] == name), None)

    if not backup_info:
        print_color(Colors.RED, f"Backup '{name}' not found")
        return False

    backup_path = BACKUP_DIR / name

    if not backup_path.exists():
        print_color(Colors.RED, f"Backup directory not found: {backup_path}")
        return False

    print(f"Backup date: {backup_info['timestamp']}")
    print(f"Files to restore: {len(backup_info['files_backed'])}")

    # Restore SSH keys
    ssh_backup = backup_path / 'ssh'
    if ssh_backup.exists():
        print_color(Colors.CYAN, "\n🔐 Restoring SSH keys...")
        ssh_dir = Path.home() / '.ssh'
        ssh_dir.mkdir(exist_ok=True)

        for item in ssh_backup.iterdir():
            dest = ssh_dir / item.name
            try:
                if item.is_file():
                    shutil.copy2(item, dest)
                    print_color(Colors.GREEN, f"  ✓ {item.name}")
                else:
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                    print_color(Colors.GREEN, f"  ✓ {item.name}/")
            except Exception as e:
                print_color(Colors.RED, f"  ✗ {item.name}: {e}")

    # Restore workspace configs
    workspace_backup = backup_path / 'workspace'
    if workspace_backup.exists():
        print_color(Colors.CYAN, "\n📝 Restoring workspace configs...")
        workspace = Path.home() / '.openclaw' / 'workspace'

        for item in workspace_backup.iterdir():
            dest = workspace / item.name
            try:
                shutil.copy2(item, dest)
                print_color(Colors.GREEN, f"  ✓ {item.name}")
            except Exception as e:
                print_color(Colors.RED, f"  ✗ {item.name}: {e}")

    # Restore tool configs
    tools_backup = backup_path / 'tools'
    if tools_backup.exists():
        print_color(Colors.CYAN, "\n🔧 Restoring tool configurations...")

        # Restore tick tasks
        tick_backup = tools_backup / 'tasks.json'
        if tick_backup.exists():
            tick_dir = Path.home() / '.tick'
            tick_dir.mkdir(exist_ok=True)
            shutil.copy2(tick_backup, tick_dir / 'tasks.json')
            print_color(Colors.GREEN, "  ✓ tick tasks.json")

        # Restore snip snippets
        snip_backup = tools_backup / 'snippets.json'
        if snip_backup.exists():
            snip_dir = Path.home() / '.snip'
            snip_dir.mkdir(exist_ok=True)
            shutil.copy2(snip_backup, snip_dir / 'snippets.json')
            print_color(Colors.GREEN, "  ✓ snip snippets.json")

        # Restore squad status
        squad_backup = tools_backup / 'squad' / 'status.json'
        if squad_backup.exists():
            squad_dir = Path.home() / '.squad'
            squad_dir.mkdir(exist_ok=True)
            shutil.copy2(squad_backup, squad_dir / 'status.json')
            print_color(Colors.GREEN, "  ✓ squad status.json")

    # Log restore
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] Restored backup '{name}'\n"
    with open(BACKUP_LOG, 'a') as f:
        f.write(log_entry)

    print_color(Colors.BOLD, "\n" + "=" * 60)
    print_color(Colors.GREEN, "✓ Restore Complete")
    print("=" * 60)

    return True


def show_status():
    """Show backup system status."""
    print_color(Colors.BOLD, "\n📊 Backup System Status")
    print("-" * 60)

    # Backup directory
    if BACKUP_DIR.exists():
        print_color(Colors.GREEN, f"\n✓ Backup directory: {BACKUP_DIR}")
        total_size = sum(f.stat().st_size for f in BACKUP_DIR.rglob('*') if f.is_file())
        print(f"  Total size: {total_size / 1024 / 1024:.2f} MB")
    else:
        print_color(Colors.YELLOW, "\n⚠ Backup directory not found")

    # Backups count
    if BACKUP_INDEX.exists():
        with open(BACKUP_INDEX) as f:
            backups = json.load(f)
        print_color(Colors.GREEN, f"✓ Total backups: {len(backups)}")
    else:
        backups = 0
        print_color(Colors.YELLOW, "⚠ No backup index found")

    # Recent activity
    if BACKUP_LOG.exists():
        print_color(Colors.CYAN, "\n📜 Recent Activity:")
        with open(BACKUP_LOG) as f:
            lines = f.readlines()[-5:]  # Last 5 entries
        for line in lines:
            print(f"  {line.strip()}")
    else:
        print_color(Colors.YELLOW, "\n⚠ No backup log found")

    return True


def auto_backup():
    """Create automatic backup with timestamp."""
    timestamp = datetime.now()
    backup_name = f"auto-{timestamp.strftime('%Y%m%d-%H%M%S')}"

    print(f"Creating automatic backup: {backup_name}")
    return create_backup(backup_name)


def cleanup_old_backups(keep_count: int = 10):
    """Remove old backups, keeping specified count."""
    print_color(Colors.BOLD, f"\n🧹 Cleaning old backups (keeping {keep_count})")
    print("-" * 60)

    if not BACKUP_INDEX.exists():
        print_color(Colors.YELLOW, "No backups to clean")
        return True

    with open(BACKUP_INDEX) as f:
        backups = json.load(f)

    if len(backups) <= keep_count:
        print_color(Colors.GREEN, f"\n✓ {len(backups)} backups, within limit")
        return True

    # Sort by timestamp and remove old ones
    backups.sort(key=lambda x: x['timestamp'], reverse=True)
    to_remove = backups[keep_count:]

    if not to_remove:
        print_color(Colors.GREEN, "\n✓ No old backups to remove")
        return True

    removed = []
    for backup_info in to_remove:
        backup_path = BACKUP_DIR / backup_info['name']
        try:
            shutil.rmtree(backup_path)
            removed.append(backup_info['name'])
            print_color(Colors.GREEN, f"  ✓ Removed {backup_info['name']}")
        except Exception as e:
            print_color(Colors.RED, f"  ✗ Failed to remove {backup_info['name']}: {e}")

    # Update index
    backups = backups[:keep_count]
    with open(BACKUP_INDEX, 'w') as f:
        json.dump(backups, f, indent=2)

    print_color(Colors.BOLD, f"\n✓ Removed {len(removed)} old backups")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Configuration and Key Backup Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # create command
    create_parser = subparsers.add_parser('create', help='Create a backup')
    create_parser.add_argument('name', help='Backup name')

    # restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('name', help='Backup name to restore')

    # auto command
    subparsers.add_parser('auto', help='Create automatic backup with timestamp')

    # list command
    subparsers.add_parser('list', help='List all backups')

    # status command
    subparsers.add_parser('status', help='Show backup system status')

    # cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean old backups')
    cleanup_parser.add_argument('-k', '--keep', type=int, default=10,
                            help='Number of backups to keep (default: 10)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize
    init_backup_system()

    success = False

    if args.command == 'create':
        success = create_backup(args.name)
    elif args.command == 'restore':
        success = restore_backup(args.name)
    elif args.command == 'auto':
        success = auto_backup()
    elif args.command == 'list':
        success = list_backups()
    elif args.command == 'status':
        success = show_status()
    elif args.command == 'cleanup':
        success = cleanup_old_backups(args.keep)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
