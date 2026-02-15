#!/usr/bin/env python3
"""
squad-setup - AI Squad Dashboard SSH Setup Helper

Automate SSH setup for squad dashboard agent VMs.
Tests connectivity, copies keys, verifies OpenClaw status.

Usage:
  squad-setup test           # Test connectivity to all VMs
  squad-setup copy-keys      # Copy SSH keys to VMs
  squad-setup verify         # Verify OpenClaw status on all VMs
  squad-setup status         # Show current setup status
  squad-setup auto           # Run full setup pipeline
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
SQUAD_VMS = {
    'marcus-squad': 'Research Agent',
    'archimedes-squad': 'Build Agent',
    'argus-squad': 'Infrastructure Agent',
    'galen-squad': 'Deep Research Agent',
}

SQUAD_USER = 'forge'
SSH_TIMEOUT = 5
STATUS_FILE = Path.home() / '.squad' / 'status.json'


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def print_color(color, text):
    """Print colored text."""
    print(f"{color}{text}{Colors.RESET}")


def check_ssh_key():
    """Check if SSH key exists."""
    for key_type in ['id_ed25519', 'id_rsa']:
        key_path = Path.home() / '.ssh' / key_type
        if key_path.exists():
            print_color(Colors.GREEN, f"✓ SSH key found: {key_path}")
            return True

    print_color(Colors.RED, "✗ No SSH key found")
    print_color(Colors.YELLOW, "  Run: ssh-keygen -t ed25519")
    return False


def test_ssh_connectivity():
    """Test SSH connectivity to all squad VMs."""
    print_color(Colors.BOLD, "\n🔌 Testing SSH Connectivity...")
    print("-" * 50)

    results = {}
    for vm, description in SQUAD_VMS.items():
        try:
            result = subprocess.run(
                ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
                 '-o', 'BatchMode=yes',
                 '-o', 'StrictHostKeyChecking=no',
                 f'{SQUAD_USER}@{vm}', 'echo connected'],
                capture_output=True,
                timeout=SSH_TIMEOUT + 2
            )

            if result.returncode == 0:
                print_color(Colors.GREEN, f"✓ {vm}: {description}")
                results[vm] = 'connected'
            else:
                if 'Permission denied' in result.stderr.decode():
                    print_color(Colors.YELLOW, f"⚠ {vm}: Permission denied (key needed)")
                    results[vm] = 'permission_denied'
                elif 'Could not resolve' in result.stderr.decode():
                    print_color(Colors.RED, f"✗ {vm}: DNS resolution failed")
                    results[vm] = 'dns_error'
                else:
                    print_color(Colors.RED, f"✗ {vm}: {result.stderr.decode().strip()}")
                    results[vm] = 'error'

        except subprocess.TimeoutExpired:
            print_color(Colors.RED, f"✗ {vm}: Connection timeout")
            results[vm] = 'timeout'
        except Exception as e:
            print_color(Colors.RED, f"✗ {vm}: {e}")
            results[vm] = 'error'

    return results


def copy_ssh_keys():
    """Copy SSH keys to VMs that need them."""
    print_color(Colors.BOLD, "\n📤 Copying SSH Keys...")
    print("-" * 50)

    # Find SSH key
    key_path = None
    for key_type in ['id_ed25519', 'id_rsa']:
        key_file = Path.home() / '.ssh' / key_type
        if key_file.exists():
            key_path = key_file
            break

    if not key_path:
        print_color(Colors.RED, "✗ No SSH key found. Run: ssh-keygen -t ed25519")
        return {}

    # Read public key
    pub_key_path = key_path.with_suffix('.pub')
    with open(pub_key_path) as f:
        public_key = f.read().strip()

    results = {}

    for vm, description in SQUAD_VMS.items():
        # First, check if we can connect
        try:
            result = subprocess.run(
                ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
                 '-o', 'BatchMode=yes',
                 f'{SQUAD_USER}@{vm}', 'echo test'],
                capture_output=True,
                timeout=SSH_TIMEOUT + 2
            )

            if result.returncode == 0:
                print_color(Colors.GREEN, f"✓ {vm}: Already accessible")
                results[vm] = 'already_accessible'
                continue

        except:
            pass

        # Try to copy key
        try:
            # Create .ssh directory
            subprocess.run(
                ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
                 f'{SQUAD_USER}@{vm}', 'mkdir -p ~/.ssh && chmod 700 ~/.ssh'],
                capture_output=True,
                timeout=SSH_TIMEOUT + 5,
                input='',
                encoding='utf-8'
            )

            # Add public key to authorized_keys
            subprocess.run(
                ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
                 f'{SQUAD_USER}@{vm}', f'echo "{public_key}" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'],
                capture_output=True,
                timeout=SSH_TIMEOUT + 5,
                input='',
                encoding='utf-8'
            )

            # Test connection again
            result = subprocess.run(
                ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
                 '-o', 'BatchMode=yes',
                 f'{SQUAD_USER}@{vm}', 'echo test'],
                capture_output=True,
                timeout=SSH_TIMEOUT + 2
            )

            if result.returncode == 0:
                print_color(Colors.GREEN, f"✓ {vm}: Key copied successfully")
                results[vm] = 'key_copied'
            else:
                print_color(Colors.YELLOW, f"⚠ {vm}: Key copied but still can't connect")
                results[vm] = 'key_copied_failed_connect'

        except subprocess.TimeoutExpired:
            print_color(Colors.RED, f"✗ {vm}: Connection timeout during key copy")
            results[vm] = 'timeout'
        except Exception as e:
            print_color(Colors.RED, f"✗ {vm}: {e}")
            results[vm] = 'error'

    return results


def verify_openclaw_status():
    """Verify OpenClaw is installed and working on each VM."""
    print_color(Colors.BOLD, "\n🤖 Verifying OpenClaw Status...")
    print("-" * 50)

    results = {}

    for vm, description in SQUAD_VMS.items():
        try:
            result = subprocess.run(
                ['ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
                 f'{SQUAD_USER}@{vm}', 'openclaw status'],
                capture_output=True,
                timeout=SSH_TIMEOUT + 5
            )

            if result.returncode == 0:
                status = result.stdout.decode().strip()
                # Extract agent name from status
                if 'agent=' in status:
                    agent = status.split('agent=')[1].split()[0]
                    print_color(Colors.GREEN, f"✓ {vm}: OpenClaw running (agent={agent})")
                    results[vm] = 'openclaw_running'
                else:
                    print_color(Colors.YELLOW, f"⚠ {vm}: OpenClaw installed but no agent info")
                    results[vm] = 'openclaw_no_agent'

            else:
                stderr = result.stderr.decode()
                if 'not found' in stderr or 'command not found' in stderr:
                    print_color(Colors.RED, f"✗ {vm}: OpenClaw not found")
                    results[vm] = 'openclaw_not_found'
                elif 'Permission denied' in stderr:
                    print_color(Colors.YELLOW, f"⚠ {vm}: SSH access denied")
                    results[vm] = 'ssh_denied'
                else:
                    print_color(Colors.RED, f"✗ {vm}: {stderr.strip()}")
                    results[vm] = 'error'

        except subprocess.TimeoutExpired:
            print_color(Colors.RED, f"✗ {vm}: Connection timeout")
            results[vm] = 'timeout'
        except Exception as e:
            print_color(Colors.RED, f"✗ {vm}: {e}")
            results[vm] = 'error'

    return results


def show_setup_status():
    """Show current setup status summary."""
    print_color(Colors.BOLD, "\n📊 Squad Setup Status")
    print("=" * 50)

    # Check SSH key
    has_key = check_ssh_key()

    # Test connectivity
    connectivity = test_ssh_connectivity()

    # Count results
    connected = sum(1 for v in connectivity.values() if v == 'connected')
    permission_denied = sum(1 for v in connectivity.values() if v == 'permission_denied')
    dns_errors = sum(1 for v in connectivity.values() if v == 'dns_error')

    print_color(Colors.BOLD, "\nConnectivity Summary:")
    print(f"  Connected:        {connected}/{len(SQUAD_VMS)}")
    print(f"  Permission Denied:{permission_denied}/{len(SQUAD_VMS)}")
    print(f"  DNS Errors:       {dns_errors}/{len(SQUAD_VMS)}")

    print_color(Colors.BOLD, "\nNext Steps:")
    if dns_errors > 0:
        print_color(Colors.YELLOW, "  1. Fix DNS: Add host entries to /etc/hosts or use IP addresses")

    if permission_denied > 0:
        print_color(Colors.YELLOW, "  2. Run: squad-setup copy-keys")
        print_color(Colors.YELLOW, "  3. Or manually: ssh-copy-id forge@<vm-name>")

    if connected == len(SQUAD_VMS):
        print_color(Colors.GREEN, "  ✓ All VMs accessible! Run: squad-setup verify")

    print_color(Colors.BOLD, "\nManual Commands:")
    for vm in SQUAD_VMS.keys():
        print(f"  ssh {SQUAD_USER}@{vm}")

    return {
        'has_ssh_key': has_key,
        'connectivity': connectivity,
        'connected': connected,
        'permission_denied': permission_denied,
        'dns_errors': dns_errors,
    }


def run_auto_setup():
    """Run full setup pipeline."""
    print_color(Colors.BOLD, "🚀 Running Auto Setup Pipeline")
    print("=" * 50)

    # Step 1: Check SSH key
    if not check_ssh_key():
        print_color(Colors.RED, "\n✗ Setup failed: No SSH key found")
        return False

    # Step 2: Test connectivity
    connectivity = test_ssh_connectivity()
    connected = sum(1 for v in connectivity.values() if v == 'connected')

    if connected == len(SQUAD_VMS):
        print_color(Colors.GREEN, "\n✓ All VMs already accessible!")
    else:
        # Step 3: Copy keys
        copy_results = copy_ssh_keys()

        # Test again
        connectivity = test_ssh_connectivity()
        connected = sum(1 for v in connectivity.values() if v == 'connected')

        if connected < len(SQUAD_VMS):
            print_color(Colors.YELLOW, "\n⚠ Some VMs still not accessible")
            print_color(Colors.YELLOW, "  Manual setup may be required")

    # Step 4: Verify OpenClaw
    openclaw_results = verify_openclaw_status()
    openclaw_running = sum(1 for v in openclaw_results.values() if v == 'openclaw_running')

    # Summary
    print_color(Colors.BOLD, "\n📋 Setup Summary:")
    print_color(Colors.GREEN, f"  SSH Keys:        ✓")
    print_color(Colors.GREEN, f"  Connected VMs:   {connected}/{len(SQUAD_VMS)}")
    print_color(Colors.GREEN, f"  OpenClaw Running:{openclaw_running}/{len(SQUAD_VMS)}")

    if connected == len(SQUAD_VMS) and openclaw_running == len(SQUAD_VMS):
        print_color(Colors.GREEN, "\n✅ Setup Complete! Squad dashboard ready for deployment.")
        print_color(Colors.BLUE, "\nNext: cd ~/workspace/squad-dashboard && ./deploy-forge.sh")
        return True
    else:
        print_color(Colors.YELLOW, "\n⚠ Setup partially complete. See issues above.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='AI Squad Dashboard SSH Setup Helper'
    )
    parser.add_argument(
        'action',
        choices=['test', 'copy-keys', 'verify', 'status', 'auto'],
        help='Action to perform'
    )

    args = parser.parse_args()

    if args.action == 'test':
        test_ssh_connectivity()

    elif args.action == 'copy-keys':
        copy_ssh_keys()

    elif args.action == 'verify':
        verify_openclaw_status()

    elif args.action == 'status':
        show_setup_status()

    elif args.action == 'auto':
        run_auto_setup()


if __name__ == '__main__':
    main()
