# ssh-helper - SSH Connection and Key Management Helper

Diagnose, test, and fix SSH connections across multiple hosts.

## Features

- **Test Connectivity** - Quick SSH connection test to any host
- **Full Diagnostics** - Comprehensive SSH troubleshooting (DNS, port, auth, keys)
- **Copy SSH Keys** - Automate SSH key distribution
- **Tailscale SSH Support** - Test and use Tailscale SSH as alternative
- **Connection History** - Track and list known SSH connections

## Installation

```bash
# Make executable
chmod +x ~/workspace/tools/ssh-helper/ssh-helper.py

# Symlink to PATH
ln -sf ~/workspace/tools/ssh-helper/ssh-helper.py ~/.local/bin/ssh-helper
```

## Usage

### Test SSH Connection

```bash
ssh-helper test <host> [-u <user>] [-p <port>]
```

Test if you can connect to a host via SSH.

**Example:**
```bash
ssh-helper test marcus-squad
ssh-helper test archimedes-squad -u exedev
ssh-helper test example.com -p 2222
```

### Full Diagnostics

```bash
ssh-helper diagnose <host> [-u <user>] [-p <port>]
```

Run comprehensive SSH diagnostics to identify connection issues.

**Checks:**
1. DNS resolution - Can hostname be resolved?
2. Port connectivity - Is SSH port open?
3. SSH authentication - Does SSH key work?
4. SSH keys - Do you have valid SSH keys?
5. Tailscale - Is host in Tailscale network?

**Example:**
```bash
ssh-helper diagnose argus-squad
```

**Output:**
```
🔍 Diagnosing SSH connection to argus-squad...
------------------------------------------------------------

1. DNS Resolution
  ✓ Hostname resolves to: 100.108.219.91

2. Port Connectivity
  ✓ Port 22 is open

3. SSH Authentication
  ⚠ Authentication failed
     User: exedev
     Issue: SSH key not in authorized_keys

4. SSH Keys
  ✓ Found: id_ed25519 (permissions: 600)

5. Tailscale
  ✓ Host found in Tailscale network
     Tailscale IP: 100.108.219.91

============================================================
Summary
============================================================

Issues Found (1):
  1. SSH key not authorized

Suggestions (1):
  1. Run: ssh-copy-id exedev@argus-squad
```

### Copy SSH Key

```bash
ssh-helper copy-key <host> [-u <user>] [-p <port>]
```

Automatically copy your SSH public key to a host's authorized_keys.

**Example:**
```bash
ssh-helper copy-key galen-squad
```

### Test Tailscale SSH

```bash
ssh-helper tailscale
```

Check if Tailscale SSH is available and test connectivity to Tailscale hosts.

**Output:**
```
🐉 Testing Tailscale SSH...
✓ Found 4 Tailscale hosts

marcus-squad             100.98.223.103   inactive
archimedes-squad          100.100.56.102    -
argus-squad               100.108.219.91    active
galen-squad               100.123.121.125   -

Testing Tailscale SSH connectivity...
  ✓ argus-squad
  ✗ marcus-squad
  ✗ archimedes-squad

Summary:
  Connected: 1/4 tested
  Use: tailscale ssh <hostname>
```

### List Known Connections

```bash
ssh-helper list
```

Show history of tested SSH connections.

## Diagnostics Explained

### 1. DNS Resolution

Checks if hostname can be resolved to an IP address.

**Failures indicate:**
- Hostname doesn't exist
- DNS server issues
- Network connectivity problems

**Fixes:**
- Add entry to `/etc/hosts`
- Check DNS configuration
- Use IP address directly

### 2. Port Connectivity

Uses `nc` (netcat) to test if SSH port (22) is reachable.

**Failures indicate:**
- Firewall blocking port 22
- SSH daemon not running
- Network unreachable
- Host is down

**Fixes:**
- Check firewall rules
- Verify SSH daemon is running
- Check network connectivity

### 3. SSH Authentication

Attempts SSH connection with publickey authentication only.

**Failures indicate:**
- SSH key not in `authorized_keys`
- User doesn't exist on remote host
- SSH daemon configured to reject key

**Fixes:**
- Copy SSH key: `ssh-copy-id user@host`
- Verify user exists on remote host
- Check SSH daemon configuration

### 4. SSH Keys

Validates local SSH keys exist and have correct permissions.

**Issues:**
- Missing SSH keys
- Incorrect permissions (should be 600)

**Fixes:**
- Generate key: `ssh-keygen -t ed25519`
- Fix permissions: `chmod 600 ~/.ssh/id_ed25519`

### 5. Tailscale

Checks if host is in Tailscale network.

**Benefits:**
- Tailscale SSH can bypass key authentication
- Uses Tailscale authentication instead
- Useful when SSH keys are problematic

## Use Cases

### Troubleshooting Squad Dashboard SSH Issues

```bash
# Diagnose all squad VMs
ssh-helper diagnose marcus-squad
ssh-helper diagnose archimedes-squad
ssh-helper diagnose argus-squad
ssh-helper diagnose galen-squad

# Test Tailscale SSH as alternative
ssh-helper tailscale
```

### Setting Up New SSH Connections

```bash
# Test connection
ssh-helper test new-host.example.com

# If it fails, run full diagnostics
ssh-helper diagnose new-host.example.com

# Copy SSH key
ssh-helper copy-key new-host.example.com

# Verify connection
ssh-helper test new-host.example.com
```

### Diagnosing Permission Denied Errors

When you get "Permission denied (publickey)":

```bash
ssh-helper diagnose problem-host
```

This will check:
- SSH key exists locally
- Key has correct permissions
- Key is in remote authorized_keys
- User exists on remote host

## Configuration

**SSH Timeout:** 5 seconds (configured in script)

**Status File:** `~/.ssh/connections.json` (connection history)

## Troubleshooting

### "nc not installed"

Install netcat:
```bash
# Ubuntu/Debian
sudo apt install netcat

# macOS (usually pre-installed)
brew install netcat

# Arch Linux
sudo pacman -S gnu-netcat
```

### "Tailscale not installed"

Install Tailscale:
```bash
# Linux
curl -fsSL https://tailscale.com/install.sh | sh

# macOS
brew install --cask tailscale
```

### "No SSH keys found"

Generate an SSH key:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

## Integration with Other Tools

**squad-setup:** Uses ssh-helper-style diagnostics for squad VMs
**deploy scripts:** Can use ssh-helper to test connectivity before deployment
**CI/CD pipelines:** Use ssh-helper diagnose for failed SSH connections

## Requirements

- Python 3.6+
- SSH client (OpenSSH)
- Optional: `nc` (netcat) for port checking
- Optional: Tailscale for Tailscale SSH support

## License

MIT

---

**Part of CLI Toolset**
- Works with squad-setup for squad dashboard SSH issues
- Complements other SSH-based tools
- Can be integrated into deployment scripts
