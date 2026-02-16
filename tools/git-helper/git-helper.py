#!/usr/bin/env python3
"""
git-helper — Git Workflow Automation and Helper

Simplify Git operations with smart branch management, commit patterns, and release automation.
"""

import argparse
import subprocess
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class GitHelper:
    """Git workflow automation helper."""

    def __init__(self):
        self.config_dir = Path.home() / '.git-helper'
        self.config_file = self.config_dir / 'config.json'
        self.branch_patterns_file = self.config_dir / 'branch-patterns.json'

        self._ensure_config()

    def _ensure_config(self):
        """Ensure config directory and files exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            default_config = {
                'default_branch': 'main',
                'branch_prefix': 'feature/',
                'commit_pattern': 'conventional',
                'auto_push': False,
                'auto_pr': False
            }
            self._write_config(default_config)

        if not self.branch_patterns_file.exists():
            default_patterns = {
                'feature': 'feature/',
                'bugfix': 'bugfix/',
                'hotfix': 'hotfix/',
                'release': 'release/',
                'experiment': 'experiment/'
            }
            with open(self.branch_patterns_file, 'w') as f:
                json.dump(default_patterns, f, indent=2)

    def _read_config(self) -> Dict:
        """Read config from storage."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_config(self, config: Dict):
        """Write config to storage."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def _read_branch_patterns(self) -> Dict:
        """Read branch patterns."""
        try:
            with open(self.branch_patterns_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _git(self, *args, capture_output: bool = True) -> Tuple[int, str, str]:
        """Run git command."""
        try:
            result = subprocess.run(
                ['git'] + list(args),
                capture_output=capture_output,
                text=True,
                check=True
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr

    def _check_git_repo(self) -> bool:
        """Check if we're in a git repository."""
        code, _, _ = self._git('rev-parse', '--git-dir')
        return code == 0

    def _get_current_branch(self) -> Optional[str]:
        """Get current branch name."""
        code, stdout, _ = self._git('branch', '--show-current')
        if code == 0:
            return stdout.strip()
        return None

    def _get_branch_list(self) -> List[str]:
        """Get all local branches."""
        code, stdout, _ = self._git('branch', '--format=%(refname:short)')
        if code == 0:
            return [line.strip() for line in stdout.strip().split('\n') if line.strip()]
        return []

    def _get_remotes(self) -> Dict[str, str]:
        """Get git remotes."""
        code, stdout, _ = self._git('remote', '-v')
        if code != 0:
            return {}

        remotes = {}
        for line in stdout.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) == 2:
                name, url = parts
                remotes[name] = url.split()[0]
        return remotes

    def status(self) -> bool:
        """Show git repository status."""
        if not self._check_git_repo():
            print("❌ Not a git repository")
            return False

        config = self._read_config()

        # Current branch
        current = self._get_current_branch()
        print(f"📁 Repository: {Path.cwd().name}")
        print(f"🌿 Current branch: {current}")
        print()

        # Branch info
        code, stdout, _ = self._git('status', '--short', '--branch')

        # Check for changes
        if stdout:
            lines = stdout.strip().split('\n')
            if len(lines) > 1:  # First line is branch info
                changes = lines[1:]
                print(f"📝 {len(changes)} change(s):")
                for change in changes[:10]:  # Show first 10
                    status, file = change[0:2], change[3:]
                    status_icon = {'M': 'M', 'A': '+', 'D': '-', '??': '?'}.get(status[0], status[0])
                    print(f"  {status_icon} {file}")
                if len(changes) > 10:
                    print(f"  ... and {len(changes) - 10} more")
            else:
                print("✅ Working directory clean")
        else:
            print("✅ Working directory clean")

        print()

        # Remotes
        remotes = self._get_remotes()
        if remotes:
            print("📡 Remotes:")
            for name, url in remotes.items():
                print(f"  • {name}: {url}")

        print()

        # Configuration
        print("⚙️  Configuration:")
        print(f"  • Default branch: {config.get('default_branch', 'main')}")
        print(f"  • Branch prefix: {config.get('branch_prefix', 'feature/')}")

        return True

    def branch(self, action: str, name: str = None, base: str = None, pattern: str = None):
        """Branch operations."""
        if not self._check_git_repo():
            print("❌ Not a git repository")
            return False

        patterns = self._read_branch_patterns()

        if action == 'list':
            branches = self._get_branch_list()
            current = self._get_current_branch()

            print("🌿 Branches:")
            print()
            for branch in branches:
                if branch == current:
                    print(f"  * {branch} (current)")
                else:
                    print(f"    {branch}")
            return True

        elif action == 'new':
            if not name:
                print("❌ Branch name required")
                return False

            # Determine branch name
            if pattern:
                prefix = patterns.get(pattern, pattern + '/')
                branch_name = f"{prefix}{name}"
            elif base:
                # Branch from specific base
                branch_name = name
            else:
                # Use default prefix
                config = self._read_config()
                prefix = config.get('branch_prefix', 'feature/')
                branch_name = f"{prefix}{name}"

            # Check if branch already exists
            branches = self._get_branch_list()
            if branch_name in branches:
                print(f"❌ Branch '{branch_name}' already exists")
                return False

            # Create branch
            if base:
                code, _, stderr = self._git('checkout', '-b', branch_name, base)
            else:
                code, _, stderr = self._git('checkout', '-b', branch_name)

            if code == 0:
                print(f"✅ Created and switched to branch: {branch_name}")
                if base:
                    print(f"   (from {base})")
                return True
            else:
                print(f"❌ Failed to create branch: {stderr}")
                return False

        elif action == 'delete':
            if not name:
                print("❌ Branch name required")
                return False

            current = self._get_current_branch()
            if name == current:
                print("❌ Cannot delete current branch")
                return False

            code, _, stderr = self._git('branch', '-d', name)
            if code == 0:
                print(f"✅ Deleted branch: {name}")
                return True
            else:
                print(f"❌ Failed to delete branch: {stderr}")
                return False

        elif action == 'switch':
            if not name:
                print("❌ Branch name required")
                return False

            code, _, stderr = self._git('checkout', name)
            if code == 0:
                print(f"✅ Switched to branch: {name}")
                return True
            else:
                print(f"❌ Failed to switch branch: {stderr}")
                return False

        else:
            print(f"❌ Unknown action: {action}")
            print("   Use: list, new, delete, switch")
            return False

    def commit(self, message: str = None, amend: bool = False, fixup: bool = False):
        """Commit changes with smart formatting."""
        if not self._check_git_repo():
            print("❌ Not a git repository")
            return False

        config = self._read_config()
        pattern = config.get('commit_pattern', 'conventional')

        # Get commit message
        if not message:
            if fixup:
                # Find commit to fixup
                code, stdout, _ = self._git('log', '-5', '--format=%h %s')
                if code == 0:
                    print("📜 Recent commits:")
                    for line in stdout.strip().split('\n'):
                        print(f"  {line}")
                    return False
            else:
                print("❌ Commit message required")
                print("   Use: git-helper commit \"<message>\"")
                return False

        # Format commit message
        if pattern == 'conventional' and not fixup:
            # Check if already in conventional format
            conventional_pattern = r'^(feat|fix|docs|style|refactor|test|chore|ci|build|perf|revert)(\(.+\))?: .+'
            if not re.match(conventional_pattern, message):
                print(f"⚠️  Message doesn't follow conventional commits format")
                print(f"   Expected: type(scope): description")
                print(f"   Types: feat, fix, docs, style, refactor, test, chore, ci, build, perf, revert")
                print()
                response = input("Proceed anyway? (y/N): ")
                if response.lower() != 'y':
                    return False

        # Stage all changes
        code, _, _ = self._git('add', '-A')
        if code != 0:
            print("❌ Failed to stage changes")
            return False

        # Commit
        commit_args = []
        if amend:
            commit_args.append('--amend')
        elif fixup:
            commit_args.append('--fixup')
            # Find commit to fixup
            code, stdout, _ = self._git('log', '-1', '--format=%H')
            if code == 0:
                commit_args.append(stdout.strip())

        commit_args.append('-m')
        commit_args.append(message)

        code, _, stderr = self._git('commit', *commit_args)

        if code == 0:
            print(f"✅ Committed: {message}")

            # Auto-push if configured
            if config.get('auto_push', False) and not fixup and not amend:
                self.push()
            return True
        else:
            print(f"❌ Failed to commit: {stderr}")
            return False

    def push(self, remote: str = 'origin', set_upstream: bool = True):
        """Push to remote."""
        if not self._check_git_repo():
            print("❌ Not a git repository")
            return False

        current = self._get_current_branch()
        if not current:
            print("❌ Could not determine current branch")
            return False

        args = ['push', remote]
        if set_upstream:
            args.append('-u')
        args.append(current)

        code, _, stderr = self._git(*args)

        if code == 0:
            print(f"✅ Pushed to {remote}/{current}")
            return True
        else:
            print(f"❌ Failed to push: {stderr}")
            return False

    def pull(self, remote: str = 'origin'):
        """Pull from remote."""
        if not self._check_git_repo():
            print("❌ Not a git repository")
            return False

        args = ['pull', remote]
        current = self._get_current_branch()
        if current:
            args.append(current)

        code, _, stderr = self._git(*args)

        if code == 0:
            print(f"✅ Pulled from {remote}")
            return True
        else:
            print(f"❌ Failed to pull: {stderr}")
            return False

    def merge(self, source: str, strategy: str = None):
        """Merge branch."""
        if not self._check_git_repo():
            print("❌ Not a git repository")
            return False

        args = ['merge']
        if strategy:
            args.extend(['--strategy', strategy])
        args.append(source)

        code, _, stderr = self._git(*args)

        if code == 0:
            print(f"✅ Merged {source}")
            return True
        else:
            print(f"❌ Failed to merge: {stderr}")
            return False

    def config(self, key: str = None, value: str = None):
        """Manage configuration."""
        if not self._check_git_repo():
            print("❌ Not a git repository")
            return False

        config = self._read_config()

        if not key:
            # Show all config
            print("⚙️  Configuration:")
            for k, v in config.items():
                print(f"  • {k}: {v}")
            return True

        if value:
            # Set value
            config[key] = value
            self._write_config(config)
            print(f"✅ Set {key} = {value}")
            return True
        else:
            # Show value
            if key in config:
                print(f"  • {key}: {config[key]}")
            else:
                print(f"  • {key}: (not set)")
            return True


def main():
    parser = argparse.ArgumentParser(
        description='git-helper — Git Workflow Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  git-helper status
  git-helper branch new feature-name -p feature
  git-helper branch switch main
  git-helper commit "feat: Add new feature"
  git-helper push
  git-helper pull
  git-helper config auto_push true
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Status
    subparsers.add_parser('status', help='Show repository status')

    # Branch
    branch_parser = subparsers.add_parser('branch', help='Branch operations')
    branch_parser.add_argument('action', choices=['list', 'new', 'delete', 'switch'],
                             help='Action to perform')
    branch_parser.add_argument('name', nargs='?', help='Branch name')
    branch_parser.add_argument('-b', '--base', help='Base branch for new branch')
    branch_parser.add_argument('-p', '--pattern', help='Branch pattern (feature, bugfix, hotfix, release)')

    # Commit
    commit_parser = subparsers.add_parser('commit', help='Commit changes')
    commit_parser.add_argument('message', nargs='?', help='Commit message')
    commit_parser.add_argument('--amend', action='store_true', help='Amend last commit')
    commit_parser.add_argument('--fixup', action='store_true', help='Create fixup commit')

    # Push
    push_parser = subparsers.add_parser('push', help='Push to remote')
    push_parser.add_argument('-r', '--remote', default='origin', help='Remote name')
    push_parser.add_argument('--no-upstream', action='store_true', help='Don\'t set upstream')

    # Pull
    pull_parser = subparsers.add_parser('pull', help='Pull from remote')
    pull_parser.add_argument('-r', '--remote', default='origin', help='Remote name')

    # Merge
    merge_parser = subparsers.add_parser('merge', help='Merge branch')
    merge_parser.add_argument('source', help='Source branch')
    merge_parser.add_argument('-s', '--strategy', help='Merge strategy')

    # Config
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_parser.add_argument('key', nargs='?', help='Config key')
    config_parser.add_argument('value', nargs='?', help='Config value')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    helper = GitHelper()

    if args.command == 'status':
        helper.status()
    elif args.command == 'branch':
        helper.branch(args.action, args.name, args.base, args.pattern)
    elif args.command == 'commit':
        helper.commit(args.message, args.amend, args.fixup)
    elif args.command == 'push':
        helper.push(args.remote, not args.no_upstream)
    elif args.command == 'pull':
        helper.pull(args.remote)
    elif args.command == 'merge':
        helper.merge(args.source, args.strategy)
    elif args.command == 'config':
        helper.config(args.key, args.value)

    return 0


if __name__ == '__main__':
    sys.exit(main())
