# squad-setup - AI Squad Dashboard SSH Setup Helper

Automate SSH setup for squad dashboard agent VMs.

## Features

- **Test connectivity** - Check SSH access to all agent VMs
- **Copy SSH keys** - Automate key distribution to VMs
- **Verify OpenClaw** - Confirm OpenClaw is running on each VM
- **Status summary** - Show current setup state
- **Auto setup** - Run full setup pipeline automatically

## Installation

```bash
# Make executable
chmod +x ~/workspace/tools/squad-setup/squad-setup.py

# Symlink to PATH
ln -sf ~/workspace/tools/squad-setup/squad-setup.py ~/.local/bin/squad-setup
```

## Usage

### Test SSH Connectivity

```bash
squad-setup test
```

Checks SSH access to all squad VMs:
- marcus-squad (Research Agent)
- archimedes-squad (Build Agent)
- argus-squad (Infrastructure Agent)
- galen-squad (Deep Research Agent)

### Copy SSH Keys

```bash
squad-setup copy-keys
```

Automates SSH key distribution:
- Copies public key to each VM
- Adds to ~/.ssh/authorized_keys
- Tests connection after copy

### Verify OpenClaw Status

```bash
squad-setup verify
```

Confirms OpenClaw is installed and running:
- Runs `openclaw status` on each VM
- Parses output for agent information
- Reports any issues found

### Show Setup Status

```bash
squad-setup status
```

Shows summary of current setup:
- SSH key status
- Connectivity summary (connected, denied, DNS errors)
- Next steps to complete setup
- Manual SSH commands for each VM

### Run Auto Setup

```bash
squad-setup auto
```

Runs full setup pipeline:
1. Check SSH key exists
2. Test connectivity to all VMs
3. Copy keys to VMs that need them
4. Verify OpenClaw status on all VMs
5. Show summary and next steps

## Example Output

```bash
$ squad-setup test

🔌 Testing SSH Connectivity...
--------------------------------------------------
⚠ marcus-squad: DNS resolution failed
✓ archimedes-squad: Build Agent
✓ argus-squad: Infrastructure Agent
✓ galen-squad: Deep Research Agent
```

```bash
$ squad-setup auto

🚀 Running Auto Setup Pipeline
==================================================
✓ SSH key found: /home/exedev/.ssh/id_ed25519

🔌 Testing SSH Connectivity...
--------------------------------------------------
✓ marcus-squad: Research Agent
✓ archimedes-squad: Build Agent
✓ argus-squad: Infrastructure Agent
✓ galen-squad: Deep Research Agent

📊 Squad Setup Status
==================================================
✓ SSH Keys:        ✓
✓ Connected VMs:   4/4
✓ OpenClaw Running:4/4

✅ Setup Complete! Squad dashboard ready for deployment.

Next: cd ~/workspace/squad-dashboard && ./deploy-forge.sh
```

## Configuration

Edit `squad-setup.py` to customize:

```python
SQUAD_VMS = {
    'marcus-squad': 'Research Agent',
    'archimedes-squad': 'Build Agent',
    'argus-squad': 'Infrastructure Agent',
    'galen-squad': 'Deep Research Agent',
}

SQUAD_USER = 'forge'
SSH_TIMEOUT = 5
```

## Troubleshooting

### "No SSH key found"

Generate an SSH key:
```bash
ssh-keygen -t ed25519
```

### "DNS resolution failed"

Add entries to `/etc/hosts`:
```
192.168.1.10  marcus-squad
192.168.1.11  archimedes-squad
192.168.1.12  argus-squad
192.168.1.13  galen-squad
```

Or use IP addresses directly in `SQUAD_VMS`.

### "Permission denied"

Manual key copy:
```bash
ssh-copy-id forge@marcus-squad
ssh-copy-id forge@archimedes-squad
ssh-copy-id forge@argus-squad
ssh-copy-id forge@galen-squad
```

### "OpenClaw not found"

Install OpenClaw on the VM:
```bash
ssh forge@marcus-squad
# Follow OpenClaw installation instructions
```

## Next Steps After Setup

Once setup is complete, deploy the squad dashboard:

```bash
cd ~/workspace/squad-dashboard
./deploy-forge.sh
```

Access at: http://100.93.69.117:8080/

## Requirements

- Python 3.6+
- SSH client (OpenSSH)
- SSH key for authentication
- Network access to agent VMs

## License

MIT

---

**Part of the Squad Dashboard project**
