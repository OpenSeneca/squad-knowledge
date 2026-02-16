#!/usr/bin/env python3
"""
env — Environment Variable Manager

Manage .env files, switch between environments, and securely handle secrets.
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class EnvManager:
    """Environment variable management."""

    def __init__(self):
        self.config_dir = Path.home() / '.env-manager'
        self.environments_file = self.config_dir / 'environments.json'
        self.current_env_file = self.config_dir / 'current'

        self._ensure_config()

    def _ensure_config(self):
        """Ensure config directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.environments_file.exists():
            with open(self.environments_file, 'w') as f:
                json.dump({}, f)

        if not self.current_env_file.exists():
            self.current_env_file.touch()

    def _read_environments(self) -> Dict:
        """Read environments configuration."""
        try:
            with open(self.environments_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_environments(self, envs: Dict):
        """Write environments configuration."""
        with open(self.environments_file, 'w') as f:
            json.dump(envs, f, indent=2)

    def _get_current_env(self) -> Optional[str]:
        """Get currently active environment."""
        if self.current_env_file.exists():
            with open(self.current_env_file, 'r') as f:
                content = f.read().strip()
                return content if content else None
        return None

    def _set_current_env(self, env_name: str):
        """Set currently active environment."""
        with open(self.current_env_file, 'w') as f:
            f.write(env_name)

    def _parse_env_file(self, path: Path) -> Dict[str, str]:
        """Parse .env file."""
        env_vars = {}

        if not path.exists():
            return env_vars

        with open(path, 'r') as f:
            for line in f:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()

        return env_vars

    def _write_env_file(self, path: Path, env_vars: Dict[str, str]):
        """Write .env file."""
        with open(path, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

    def _get_project_root(self) -> Optional[Path]:
        """Find project root (has .env or package.json)."""
        cwd = Path.cwd()

        for path in [cwd] + list(cwd.parents):
            if (path / '.env').exists() or (path / 'package.json').exists() or (path / '.git').exists():
                return path

        return cwd  # Fallback to current directory

    def list(self, show_values: bool = False):
        """List all environments."""
        envs = self._read_environments()
        current = self._get_current_env()

        if not envs:
            print("📝 No environments configured")
            print("   Add one with: env add <name> <path>")
            return

        print("📝 Environments:")
        print()

        for name, config in sorted(envs.items()):
            prefix = "→ " if name == current else "  "
            path = config.get('path', 'Unknown')
            active_status = " (active)" if name == current else ""

            if show_values and name == current:
                env_vars = self._parse_env_file(Path(path))
                print(f"{prefix}{name}{active_status}")
                print(f"    Path: {path}")
                print(f"    Variables: {len(env_vars)}")
                for key, value in sorted(env_vars.items()):
                    # Mask secret values
                    if 'secret' in key.lower() or 'key' in key.lower() or 'password' in key.lower():
                        value = '***'
                    print(f"      {key}={value}")
                print()
            else:
                print(f"{prefix}{name} — {path}{active_status}")

    def add(self, name: str, path: str = None, description: str = ''):
        """Add a new environment."""
        envs = self._read_environments()

        if name in envs:
            print(f"❌ Environment '{name}' already exists")
            return False

        # Use current directory or project root if not specified
        if not path:
            project_root = self._get_project_root()
            path = str(project_root / '.env')

        path_obj = Path(path).expanduser().absolute()

        # Check if .env exists
        if not path_obj.exists():
            print(f"⚠️  Creating new .env file at: {path_obj}")
            path_obj.touch()

        envs[name] = {
            'path': str(path_obj),
            'description': description,
            'created': datetime.now().isoformat()
        }

        self._write_environments(envs)
        print(f"✅ Added environment: {name}")
        print(f"   Path: {path_obj}")
        return True

    def remove(self, name: str, keep_file: bool = False):
        """Remove an environment."""
        envs = self._read_environments()

        if name not in envs:
            print(f"❌ Environment '{name}' not found")
            return False

        current = self._get_current_env()

        # Don't remove active environment
        if name == current:
            print(f"❌ Cannot remove active environment")
            print(f"   Switch to another environment first: env switch <name>")
            return False

        path = envs[name].get('path')
        del envs[name]

        self._write_environments(envs)

        # Delete .env file if requested
        if not keep_file and path:
            path_obj = Path(path)
            if path_obj.exists():
                path_obj.unlink()
                print(f"   Deleted .env file: {path_obj}")

        print(f"✅ Removed environment: {name}")
        return True

    def switch(self, name: str):
        """Switch active environment."""
        envs = self._read_environments()

        if name not in envs:
            print(f"❌ Environment '{name}' not found")
            return False

        current = self._get_current_env()

        # Backup current .env if exists
        if current:
            current_config = envs.get(current)
            if current_config:
                current_path = Path(current_config['path'])
                if current_path.exists():
                    backup_path = current_path.with_suffix('.env.backup')
                    shutil.copy2(current_path, backup_path)

        # Copy new environment to .env
        new_config = envs[name]
        new_path = Path(new_config['path'])

        if not new_path.exists():
            print(f"❌ Environment file not found: {new_path}")
            return False

        # Copy to project root .env
        project_root = self._get_project_root()
        target_env = project_root / '.env'

        shutil.copy2(new_path, target_env)

        self._set_current_env(name)

        print(f"✅ Switched to environment: {name}")
        print(f"   Copied from: {new_path}")
        print(f"   Copied to: {target_env}")
        return True

    def set(self, key: str, value: str, env_name: str = None):
        """Set environment variable."""
        envs = self._read_environments()

        # Determine target environment
        if env_name:
            if env_name not in envs:
                print(f"❌ Environment '{env_name}' not found")
                return False
            path = Path(envs[env_name]['path'])
        else:
            # Use current directory .env
            project_root = self._get_project_root()
            path = project_root / '.env'

        if not path.exists():
            path.touch()

        # Parse existing variables
        env_vars = self._parse_env_file(path)

        # Set new value
        env_vars[key] = value

        # Write back
        self._write_env_file(path, env_vars)

        print(f"✅ Set: {key}={value}")
        print(f"   File: {path}")
        return True

    def get(self, key: str, env_name: str = None):
        """Get environment variable."""
        envs = self._read_environments()

        # Determine target environment
        if env_name:
            if env_name not in envs:
                print(f"❌ Environment '{env_name}' not found")
                return False
            path = Path(envs[env_name]['path'])
        else:
            # Use current directory .env
            project_root = self._get_project_root()
            path = project_root / '.env'

        if not path.exists():
            print(f"❌ .env file not found: {path}")
            return False

        # Parse variables
        env_vars = self._parse_env_file(path)

        if key in env_vars:
            value = env_vars[key]
            # Mask secret values
            if 'secret' in key.lower() or 'key' in key.lower() or 'password' in key.lower():
                value = '***'
            print(f"{key}={value}")
            return True
        else:
            print(f"❌ Variable '{key}' not found")
            print(f"   Available: {', '.join(sorted(env_vars.keys()))}")
            return False

    def unset(self, key: str, env_name: str = None):
        """Unset environment variable."""
        envs = self._read_environments()

        # Determine target environment
        if env_name:
            if env_name not in envs:
                print(f"❌ Environment '{env_name}' not found")
                return False
            path = Path(envs[env_name]['path'])
        else:
            # Use current directory .env
            project_root = self._get_project_root()
            path = project_root / '.env'

        if not path.exists():
            print(f"❌ .env file not found: {path}")
            return False

        # Parse variables
        env_vars = self._parse_env_file(path)

        if key not in env_vars:
            print(f"❌ Variable '{key}' not found")
            return False

        del env_vars[key]

        # Write back
        self._write_env_file(path, env_vars)

        print(f"✅ Unset: {key}")
        return True

    def show(self, env_name: str = None, mask_secrets: bool = True):
        """Show all environment variables."""
        envs = self._read_environments()

        # Determine target environment
        if env_name:
            if env_name not in envs:
                print(f"❌ Environment '{env_name}' not found")
                return False
            path = Path(envs[env_name]['path'])
            name = env_name
        else:
            # Use current directory .env
            project_root = self._get_project_root()
            path = project_root / '.env'
            name = "current"

        if not path.exists():
            print(f"❌ .env file not found: {path}")
            return False

        # Parse variables
        env_vars = self._parse_env_file(path)

        print(f"📝 Environment: {name}")
        print(f"   Path: {path}")
        print()

        for key, value in sorted(env_vars.items()):
            # Mask secret values
            display_value = value
            if mask_secrets and ('secret' in key.lower() or 'key' in key.lower() or 'password' in key.lower()):
                display_value = '***'
            print(f"  {key}={display_value}")

    def export(self, env_name: str, output: str):
        """Export environment to shell format."""
        envs = self._read_environments()

        if env_name not in envs:
            print(f"❌ Environment '{env_name}' not found")
            return False

        path = Path(envs[env_name]['path'])

        if not path.exists():
            print(f"❌ Environment file not found: {path}")
            return False

        # Parse variables
        env_vars = self._parse_env_file(path)

        # Write shell format
        output_path = Path(output).expanduser()
        with open(output_path, 'w') as f:
            for key, value in sorted(env_vars.items()):
                f.write(f"export {key}='{value}'\n")

        print(f"✅ Exported {len(env_vars)} variable(s) to: {output_path}")
        return True

    def import_env(self, input_path: str, env_name: str = None):
        """Import environment from file."""
        input_file = Path(input_path).expanduser()

        if not input_file.exists():
            print(f"❌ File not found: {input_file}")
            return False

        # Parse input file
        env_vars = self._parse_env_file(input_file)

        if not env_vars:
            print(f"❌ No variables found in: {input_file}")
            return False

        # Determine target
        if env_name:
            envs = self._read_environments()
            if env_name not in envs:
                print(f"❌ Environment '{env_name}' not found")
                return False
            path = Path(envs[env_name]['path'])
        else:
            project_root = self._get_project_root()
            path = project_root / '.env'

        # Write to target
        self._write_env_file(path, env_vars)

        print(f"✅ Imported {len(env_vars)} variable(s) to: {path}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='env — Environment Variable Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  env list
  env add dev ~/projects/myapp/.env.dev
  env switch dev
  env set API_KEY "my-secret-key"
  env get API_KEY
  env show
  env export dev shell-vars.sh
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List
    list_parser = subparsers.add_parser('list', help='List environments')
    list_parser.add_argument('-v', '--values', action='store_true', help='Show variable values')

    # Add
    add_parser = subparsers.add_parser('add', help='Add environment')
    add_parser.add_argument('name', help='Environment name')
    add_parser.add_argument('path', nargs='?', help='Path to .env file (default: ./.env)')
    add_parser.add_argument('-d', '--description', default='', help='Description')

    # Remove
    remove_parser = subparsers.add_parser('remove', help='Remove environment')
    remove_parser.add_argument('name', help='Environment name')
    remove_parser.add_argument('--keep-file', action='store_true', help='Keep .env file')

    # Switch
    switch_parser = subparsers.add_parser('switch', help='Switch environment')
    switch_parser.add_argument('name', help='Environment name')

    # Set
    set_parser = subparsers.add_parser('set', help='Set variable')
    set_parser.add_argument('key', help='Variable name')
    set_parser.add_argument('value', help='Variable value')
    set_parser.add_argument('-e', '--env', help='Target environment (default: current .env)')

    # Get
    get_parser = subparsers.add_parser('get', help='Get variable')
    get_parser.add_argument('key', help='Variable name')
    get_parser.add_argument('-e', '--env', help='Target environment (default: current .env)')

    # Unset
    unset_parser = subparsers.add_parser('unset', help='Unset variable')
    unset_parser.add_argument('key', help='Variable name')
    unset_parser.add_argument('-e', '--env', help='Target environment (default: current .env)')

    # Show
    show_parser = subparsers.add_parser('show', help='Show variables')
    show_parser.add_argument('-e', '--env', help='Target environment (default: current .env)')
    show_parser.add_argument('--no-mask', action='store_true', help='Don\'t mask secret values')

    # Export
    export_parser = subparsers.add_parser('export', help='Export to shell format')
    export_parser.add_argument('name', help='Environment name')
    export_parser.add_argument('output', help='Output file path')

    # Import
    import_parser = subparsers.add_parser('import', help='Import from file')
    import_parser.add_argument('input', help='Input file path')
    import_parser.add_argument('-e', '--env', help='Target environment (default: current .env)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    manager = EnvManager()

    if args.command == 'list':
        manager.list(args.values)
    elif args.command == 'add':
        manager.add(args.name, args.path, args.description)
    elif args.command == 'remove':
        manager.remove(args.name, args.keep_file)
    elif args.command == 'switch':
        manager.switch(args.name)
    elif args.command == 'set':
        manager.set(args.key, args.value, args.env)
    elif args.command == 'get':
        manager.get(args.key, args.env)
    elif args.command == 'unset':
        manager.unset(args.key, args.env)
    elif args.command == 'show':
        manager.show(args.env, not args.no_mask)
    elif args.command == 'export':
        manager.export(args.name, args.output)
    elif args.command == 'import':
        manager.import_env(args.input, args.env)

    return 0


if __name__ == '__main__':
    sys.exit(main())
