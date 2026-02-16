# backup - Configuration and Key Backup Tool

Automate backups of SSH keys, workspace configs, and important data.

## Features

- **SSH Key Backup** - Backup all SSH keys from ~/.ssh/
- **Workspace Configs** - Back up MEMORY.md, USER.md, IDENTITY.md, HEARTBEAT.md
- **Tool Data** - Back up tick tasks, snip snippets, squad status
- **Automatic Backups** - Create timestamped backups automatically
- **Restore** - Restore from any previous backup
- **Status** - View backup system status and recent activity
- **Cleanup** - Remove old backups (keep configurable count)

## Installation

```bash
# Make executable
chmod +x ~/workspace/tools/backup/backup.py

# Symlink to PATH
ln -sf ~/workspace/tools/backup/backup.py ~/.local/bin/backup
```

## Usage

### Create Named Backup

```bash
backup create <name>
```

Create a backup with a descriptive name.

**Example:**
```bash
backup create before-ssh-fixes
backup create squad-dashboard-v1
backup create fresh-install
```

**What gets backed up:**
- SSH keys (id_ed25519, id_rsa, etc.)
- Workspace configs (MEMORY.md, USER.md, IDENTITY.md, HEARTBEAT.md)
- Tool data (tick tasks, snip snippets, squad status)

### Create Automatic Backup

```bash
backup auto
```

Create a backup with timestamp: `auto-20260216-014500`

### List Backups

```bash
backup list
```

Show all available backups with date, file count, and size.

**Example output:**
```
Name                           Date                Files      Size
------------------------------------------------------------
before-ssh-fixes                2026-02-15          12         45.2 KB
squad-dashboard-v1              2026-02-16          15         52.1 KB ⚠
auto-20260216-014500          2026-02-16          18         58.3 KB
```

### Restore Backup

```bash
backup restore <name>
```

Restore files from a previous backup.

**What gets restored:**
- SSH keys (to ~/.ssh/)
- Workspace configs (to ~/.openclaw/workspace/)
- Tool data (to ~/.tick/, ~/.snip/, ~/.squad/)

**Warning:** Overwrites existing files.

### Show Status

```bash
backup status
```

Display backup system information:
- Backup directory location
- Total size
- Number of backups
- Recent activity (last 5 operations)

### Clean Old Backups

```bash
backup cleanup [-k <count>]
```

Remove old backups, keeping specified count.

**Example:**
```bash
backup cleanup              # Keep last 10 backups
backup cleanup -k 5        # Keep last 5 backups
```

## Backup Structure

```
~/.backup/
├── index.json              # Backup registry (metadata)
├── backup.log              # Operation log
└── <backup-name>/
    ├── metadata.json        # Backup metadata (timestamp, files, errors)
    ├── ssh/               # SSH key backups
    │   ├── id_ed25519
    │   ├── id_ed25519.pub
    │   └── known_hosts
    ├── workspace/          # Workspace config backups
    │   ├── MEMORY.md
    │   ├── USER.md
    │   ├── IDENTITY.md
    │   └── HEARTBEAT.md
    └── tools/             # Tool data backups
        ├── tasks.json        # tick tasks
        ├── snippets.json     # snip data
        └── squad/
            └── status.json    # squad status
```

## Backup Metadata

Each backup includes metadata:

```json
{
  "name": "before-ssh-fixes",
  "timestamp": "2026-02-15T12:00:00",
  "files_backed": [
    ".ssh/id_ed25519",
    ".openclaw/workspace/MEMORY.md",
    ".tick/tasks.json",
    ...
  ],
  "errors": [],
  "size_bytes": 46328
}
```

## Use Cases

### Before Major Changes

```bash
# Before making SSH changes
backup create before-ssh-config-changes

# Before deploying squad dashboard
backup create pre-deployment-v1

# Before large workspace reorganization
backup create pre-restructure
```

### Regular Automated Backups

Set up a cron job for automatic backups:

```bash
# Daily backup at 2 AM
0 2 * * * backup auto >> ~/.backup/cron.log 2>&1

# Weekly cleanup (keep 10 backups)
0 3 * * 0 backup cleanup -k 10 >> ~/.backup/cron.log 2>&1
```

### After Loss or Corruption

```bash
# Check what backups are available
backup list

# Restore from known good state
backup restore before-ssh-fixes
```

### Migration to New Machine

```bash
# 1. Copy ~/.backup/ to new machine
# 2. Run restore
backup restore fresh-install

# All your SSH keys, configs, and tool data are restored
```

## Error Handling

If backup encounters errors:

- ⚠ Warning icon appears in `backup list`
- Errors are logged in backup metadata
- Partial backups still created (successful files)
- Error details shown in `backup status`

## Best Practices

### Backup Frequency

- **Before SSH key changes** - Always backup first
- **Before deployments** - Pre-deployment backup
- **Weekly** - Regular automatic backups
- **After major changes** - Post-change backup

### Backup Naming

Use descriptive names:
- `before-ssh-fixes` - Before SSH troubleshooting
- `pre-deployment-v1` - Before deployment
- `after-squad-v1-complete` - After milestone
- `fresh-install` - Clean slate state

### Verification

After backup, verify:
```bash
# Check backup was created
backup list

# Verify backup status
backup status

# Check specific files exist
ls -la ~/.backup/<backup-name>/
```

## Security

- SSH keys contain sensitive data
- Backup directory should be: `chmod 700 ~/.backup/`
- Consider encrypting backups if storing in cloud
- Backup logs contain file paths but not contents

## Recovery

### Lost SSH Keys

```bash
backup list
backup restore <backup-with-ssh-keys>
```

All SSH keys restored to ~/.ssh/

### Corrupted Config

```bash
backup list
backup restore <backup-with-good-configs>
```

MEMORY.md and other configs restored

### Lost Tool Data

```bash
backup list
backup restore <backup-with-tool-data>
```

tick tasks, snip snippets, squad status restored

## Troubleshooting

### "No backup directory found"

```bash
# The tool auto-creates it, but if manually deleted:
mkdir -p ~/.backup
```

### "Backup index corrupted"

```bash
# Remove and recreate (won't affect actual backups)
rm ~/.backup/index.json
backup status  # Will recreate
```

### "Restore overwrites files"

Restore always overwrites existing files. This is intentional:
- Create a backup before restoring: `backup create pre-restore`
- Review what will be restored: `backup list` shows files backed up
- Restore to a test location first if unsure

## Requirements

- Python 3.6+
- File permissions to read ~/.ssh/, ~/.openclaw/, ~/.tick/, ~/.snip/, ~/.squad/

## License

MIT

---

**Part of CLI Toolset**
- Works with all other tools (tick, snip, squad-setup)
- Automated backups before risky operations
- Quick recovery from problems
- Migration support between machines
