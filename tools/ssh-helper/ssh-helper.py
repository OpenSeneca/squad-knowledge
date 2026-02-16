#!/usr/bin/env python3
"""
ssh-helper - SSH Connection and Key Management Helper

Test, diagnose, and fix SSH connections across multiple hosts.

Usage:
  ssh-helper test <host>         # Test SSH connection to a host
  ssh-helper diagnose <host>      # Full diagnostics for a host
  ssh-helper copy-key <host>     # Copy SSH key to a host
  ssh-helper list                 # List all known SSH connections
  ssh-helper tailscale             # Test Tailscale SSH availability
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
SSH_TIMEOUT = 5
STATUS_FILE = Path.home() / '.ssh' / 'connections.json'


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


def test_ssh_connectivity(host, user=None, port=22):
    """Test SSH connectivity to a host."""
    print_color(Colors.BOLD, f"\n🔌 Testing SSH to {host}...")

    ssh_user = user if user else Path.home().name
    ssh_cmd = ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
               '-o', 'StrictHostKeyChecking=no',
               '-o', 'BatchMode=yes',
               '-p', str(port),
               f'{ssh_user}@{host}',
               'echo "connected"']

    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            timeout=SSH_TIMEOUT + 2
        )

        if result.returncode == 0:
            if 'connected' in result.stdout.decode():
                print_color(Colors.GREEN, f"✓ Connection successful")
                print(f"  User: {ssh_user}")
                print(f"  Host: {host}:{port}")
                return True
        else:
            stderr = result.stderr.decode()
            if 'Permission denied' in stderr:
                print_color(Colors.YELLOW, f"⚠ Connection established, authentication failed")
                print(f"  User: {ssh_user}")
                print(f"  Issue: SSH key not in authorized_keys")
                return False
            elif 'Could not resolve' in stderr or 'Name or service not known' in stderr:
                print_color(Colors.RED, f"✗ DNS resolution failed")
                print(f"  Host: {host}")
                return False
            else:
                print_color(Colors.RED, f"✗ Connection failed")
                print(f"  Error: {stderr.strip()}")
                return False

    except subprocess.TimeoutExpired:
        print_color(Colors.RED, f"✗ Connection timeout")
        return False
    except Exception as e:
        print_color(Colors.RED, f"✗ Error: {e}")
        return False


def diagnose_ssh_connection(host, user=None, port=22):
    """Run full diagnostics for SSH connection."""
    print_color(Colors.BOLD, f"\n🔍 Diagnosing SSH connection to {host}...")
    print("-" * 60)

    issues = []
    suggestions = []

    # Check 1: DNS resolution
    print_color(Colors.CYAN, "\n1. DNS Resolution")
    try:
        result = subprocess.run(
            ['getent', 'hosts', host],
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            ip = result.stdout.decode().strip().split()[0]
            print_color(Colors.GREEN, f"  ✓ Hostname resolves to: {ip}")
        else:
            print_color(Colors.RED, f"  ✗ DNS resolution failed")
            issues.append("DNS resolution failed")
            suggestions.append("Add entry to /etc/hosts or check DNS")
    except Exception as e:
        print_color(Colors.RED, f"  ✗ DNS check failed: {e}")
        issues.append("DNS check failed")

    # Check 2: Port connectivity
    print_color(Colors.CYAN, "\n2. Port Connectivity")
    try:
        result = subprocess.run(
            ['nc', '-zv', '-w', '2', host, str(port)],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0 or 'succeeded' in result.stderr.decode():
            print_color(Colors.GREEN, f"  ✓ Port {port} is open")
        else:
            print_color(Colors.RED, f"  ✗ Port {port} is closed or unreachable")
            issues.append(f"Port {port} not reachable")
    except FileNotFoundError:
        print_color(Colors.YELLOW, f"  ⚠ nc not installed, skipping port check")
    except Exception as e:
        print_color(Colors.YELLOW, f"  ⚠ Port check failed: {e}")

    # Check 3: SSH authentication
    print_color(Colors.CYAN, "\n3. SSH Authentication")
    ssh_user = user if user else Path.home().name

    try:
        result = subprocess.run(
            ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
             '-o', 'StrictHostKeyChecking=no',
             '-o', 'BatchMode=yes',
             '-o', 'PreferredAuthentications=publickey',
             f'{ssh_user}@{host}', 'echo test'],
            capture_output=True,
            timeout=SSH_TIMEOUT + 2
        )

        stderr = result.stderr.decode()
        if result.returncode == 0:
            print_color(Colors.GREEN, f"  ✓ Authentication successful")
        elif 'Permission denied' in stderr:
            print_color(Colors.YELLOW, f"  ⚠ Authentication failed")
            print_color(Colors.RESET, f"     User: {ssh_user}")
            print_color(Colors.RESET, f"     Issue: SSH key not in authorized_keys")
            issues.append("SSH key not authorized")
            suggestions.append(f"Run: ssh-copy-id {ssh_user}@{host}")
        else:
            print_color(Colors.RED, f"  ✗ Authentication error")
            issues.append("SSH authentication error")

    except subprocess.TimeoutExpired:
        print_color(Colors.RED, f"  ✗ Connection timeout")
        issues.append("SSH connection timeout")

    # Check 4: SSH keys
    print_color(Colors.CYAN, "\n4. SSH Keys")
    ssh_dir = Path.home() / '.ssh'
    keys_found = []
    for key_type in ['id_ed25519', 'id_rsa', 'id_ecdsa']:
        key_file = ssh_dir / key_type
        if key_file.exists():
            keys_found.append(key_type)
            stat = key_file.stat()
            mode = oct(stat.st_mode)[-3:]
            print_color(Colors.GREEN, f"  ✓ Found: {key_type} (permissions: {mode})")
            if mode != '600':
                print_color(Colors.YELLOW, f"     ⚠ Incorrect permissions, run: chmod 600 {key_file}")
                suggestions.append(f"Fix permissions: chmod 600 ~/.ssh/{key_type}")

    if not keys_found:
        print_color(Colors.RED, f"  ✗ No SSH keys found")
        issues.append("No SSH keys")
        suggestions.append("Generate a key: ssh-keygen -t ed25519")

    # Check 5: Tailscale status
    print_color(Colors.CYAN, "\n5. Tailscale")
    try:
        result = subprocess.run(
            ['tailscale', 'status'],
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            output = result.stdout.decode()
            if host in output:
                print_color(Colors.GREEN, f"  ✓ Host found in Tailscale network")
                # Extract IP
                for line in output.split('\n'):
                    if host in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            print_color(Colors.RESET, f"     Tailscale IP: {parts[0]}")
            else:
                print_color(Colors.YELLOW, f"  ⚠ Host not in Tailscale network")
                suggestions.append("Check if host is running Tailscale")
        else:
            print_color(Colors.YELLOW, f"  ⚠ Tailscale not available")
    except FileNotFoundError:
        print_color(Colors.YELLOW, f"  ⚠ Tailscale not installed")
    except Exception as e:
        print_color(Colors.YELLOW, f"  ⚠ Tailscale check failed: {e}")

    # Summary
    print_color(Colors.BOLD, "\n" + "=" * 60)
    print_color(Colors.BOLD, "Summary")
    print("=" * 60)

    if issues:
        print_color(Colors.RED, f"\nIssues Found ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print_color(Colors.GREEN, f"\n✓ No issues found")

    if suggestions:
        print_color(Colors.YELLOW, f"\nSuggestions ({len(suggestions)}):")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")

    return len(issues) == 0


def copy_ssh_key(host, user=None, port=22):
    """Copy SSH key to a host."""
    print_color(Colors.BOLD, f"\n📤 Copying SSH key to {host}...")

    ssh_user = user if user else Path.home().name

    # Find SSH key
    key_file = None
    ssh_dir = Path.home() / '.ssh'
    for key_type in ['id_ed25519', 'id_rsa', 'id_ecdsa']:
        if (ssh_dir / key_type).exists():
            key_file = ssh_dir / key_type
            break

    if not key_file:
        print_color(Colors.RED, "✗ No SSH key found")
        print_color(Colors.YELLOW, "  Generate one: ssh-keygen -t ed25519")
        return False

    pub_key = key_file.with_suffix('.pub')
    if not pub_key.exists():
        print_color(Colors.RED, f"✗ Public key not found: {pub_key}")
        return False

    with open(pub_key) as f:
        public_key = f.read().strip()

    try:
        # Create .ssh directory
        subprocess.run(
            ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
             '-o', 'StrictHostKeyChecking=no',
             f'{ssh_user}@{host}',
             'mkdir -p ~/.ssh && chmod 700 ~/.ssh'],
            capture_output=True,
            timeout=SSH_TIMEOUT + 5,
            input='',
            encoding='utf-8'
        )

        # Add public key to authorized_keys
        result = subprocess.run(
            ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
             '-o', 'StrictHostKeyChecking=no',
             f'{ssh_user}@{host}',
             f'echo "{public_key}" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'],
            capture_output=True,
            timeout=SSH_TIMEOUT + 5,
            input='',
            encoding='utf-8'
        )

        # Test connection
        test_result = subprocess.run(
            ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
             '-o', 'StrictHostKeyChecking=no',
             '-o', 'BatchMode=yes',
             f'{ssh_user}@{host}', 'echo test'],
            capture_output=True,
            timeout=SSH_TIMEOUT + 2
        )

        if test_result.returncode == 0:
            print_color(Colors.GREEN, f"✓ Key copied successfully")
            print(f"  User: {ssh_user}")
            return True
        else:
            print_color(Colors.YELLOW, f"⚠ Key copied but connection still fails")
            return False

    except subprocess.TimeoutExpired:
        print_color(Colors.RED, f"✗ Connection timeout during key copy")
        return False
    except Exception as e:
        print_color(Colors.RED, f"✗ Error: {e}")
        return False


def test_tailscale_ssh():
    """Test Tailscale SSH availability."""
    print_color(Colors.BOLD, "\n🐉 Testing Tailscale SSH...")

    # Check if Tailscale is installed
    try:
        result = subprocess.run(
            ['tailscale', 'status'],
            capture_output=True,
            timeout=2
        )
        if result.returncode != 0:
            print_color(Colors.YELLOW, "⚠ Tailscale not available")
            return False
    except FileNotFoundError:
        print_color(Colors.YELLOW, "⚠ Tailscale not installed")
        return False

    # Get list of Tailscale hosts
    output = result.stdout.decode()
    hosts = []
    for line in output.split('\n'):
        if line.strip() and not line.startswith('[') and 'ts.net' in line:
            parts = line.split()
            if len(parts) >= 3:
                hosts.append({
                    'name': parts[2],
                    'ip': parts[0],
                    'status': 'active' if 'active' in line else 'inactive'
                })

    if not hosts:
        print_color(Colors.YELLOW, "⚠ No Tailscale hosts found")
        return False

    print_color(Colors.GREEN, f"✓ Found {len(hosts)} Tailscale hosts")
    print()

    for host in hosts:
        status_color = Colors.GREEN if host['status'] == 'active' else Colors.YELLOW
        status_icon = '✓' if host['status'] == 'active' else '-'
        print_color(status_color, f"{status_icon} {host['name']:<25} {host['ip']:<20} {host['status']}")

    # Test Tailscale SSH
    print_color(Colors.CYAN, "\nTesting Tailscale SSH connectivity...")
    connected = []
    failed = []

    for host in hosts[:3]:  # Test first 3 hosts
        try:
            result = subprocess.run(
                ['tailscale', 'ssh', host['name'], 'echo test'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                connected.append(host['name'])
                print_color(Colors.GREEN, f"  ✓ {host['name']}")
            else:
                failed.append(host['name'])
                print_color(Colors.RED, f"  ✗ {host['name']}")
        except Exception as e:
            failed.append(host['name'])
            print_color(Colors.RED, f"  ✗ {host['name']}: {e}")

    print()
    print_color(Colors.BOLD, "Summary:")
    print(f"  Connected: {len(connected)}/{len(hosts)} tested")
    if connected:
        print(f"  Use: tailscale ssh <hostname>")

    return len(connected) > 0


def list_connections():
    """List all known SSH connections from history."""
    print_color(Colors.BOLD, "\n📋 Known SSH Connections")
    print("-" * 60)

    # Load from status file
    if STATUS_FILE.exists():
        try:
            with open(STATUS_FILE) as f:
                connections = json.load(f)

            print(f"\nTotal: {len(connections)} connections\n")
            print(f"{'Host':<25} {'User':<15} {'Last Connected':<20}")
            print("-" * 60)

            for conn in connections:
                last_conn = conn.get('last_connected', 'Never')
                print(f"{conn['host']:<25} {conn['user']:<15} {last_conn:<20}")
        except Exception as e:
            print_color(Colors.RED, f"Error reading connections: {e}")
    else:
        print_color(Colors.YELLOW, "\nNo connection history found")
        print_color(Colors.RESET, "  Connections will be saved when you test them")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='SSH Connection and Key Management Helper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ssh-helper test marcus-squad              # Test connection
  ssh-helper diagnose archimedes-squad       # Full diagnostics
  ssh-helper copy-key argus-squad           # Copy SSH key
  ssh-helper tailscale                      # Test Tailscale SSH
  ssh-helper list                          # List known connections
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # test command
    test_parser = subparsers.add_parser('test', help='Test SSH connection to a host')
    test_parser.add_argument('host', help='Hostname to test')
    test_parser.add_argument('-u', '--user', help='SSH username')
    test_parser.add_argument('-p', '--port', type=int, default=22, help='SSH port')

    # diagnose command
    diag_parser = subparsers.add_parser('diagnose', help='Full diagnostics for a host')
    diag_parser.add_argument('host', help='Hostname to diagnose')
    diag_parser.add_argument('-u', '--user', help='SSH username')
    diag_parser.add_argument('-p', '--port', type=int, default=22, help='SSH port')

    # copy-key command
    copy_parser = subparsers.add_parser('copy-key', help='Copy SSH key to a host')
    copy_parser.add_argument('host', help='Hostname to copy key to')
    copy_parser.add_argument('-u', '--user', help='SSH username')
    copy_parser.add_argument('-p', '--port', type=int, default=22, help='SSH port')

    # list command
    subparsers.add_parser('list', help='List all known SSH connections')

    # tailscale command
    subparsers.add_parser('tailscale', help='Test Tailscale SSH availability')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    success = False

    if args.command == 'test':
        success = test_ssh_connectivity(args.host, args.user, args.port)
    elif args.command == 'diagnose':
        success = diagnose_ssh_connection(args.host, args.user, args.port)
    elif args.command == 'copy-key':
        success = copy_ssh_key(args.host, args.user, args.port)
    elif args.command == 'list':
        success = list_connections()
    elif args.command == 'tailscale':
        success = test_tailscale_ssh()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
