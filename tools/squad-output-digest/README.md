# squad-output-digest — Daily Squad Output Digest

Generates a daily digest of all squad agent outputs for Justin.

## What It Does

The squad-output-digest tool:

- **SSHs to all squad agents** (Seneca, Marcus, Galen, Archimedes, Argus)
- **Collects learnings** from today (last 10)
- **Collects outputs** from today (last 5)
- **Gets daily summaries** from memory directory
- **Produces markdown digest** with all findings
- **Saves to outputs directory** for easy access

## Installation

```bash
ln -s /path/to/squad-output-digest.py ~/.local/bin/squad-output-digest
chmod +x squad-output-digest.py
```

Already symlinked in this workspace: `~/.local/bin/squad-output-digest`

## Usage

### Generate Today's Digest

```bash
squad-output-digest
```

### Generate for Specific Date

```bash
squad-output-digest --date 2026-02-17
```

### Email to Justin

```bash
squad-output-digest --email
```

## Examples

### Today's Digest

```bash
$ squad-output-digest

📊 Squad Output Digest - 2026-02-17

# Squad Output Digest - February 17, 2026

## Seneca (Coordinator)

**Learnings:** None

**Outputs:** None

**Daily Summary:** None

## Marcus (Research)

**Learnings:**
  1. 2026-02-17-mcp-ecosystem-growth-2026.md
  2. 2026-02-17-tinyfish-accelerator-agentic-web-ecosystem.md
  3. 2026-02-17-claude-sonnet-5-fennec.md

**Outputs:** None

**Daily Summary:** 2026-02-17-session12.md

## Galen (Research)

**Learnings:** None

**Outputs:** None

**Daily Summary:** None

## Archimedes (Build)

**Learnings:** None

**Outputs:** None

**Daily Summary:** None

## Argus (Ops)

**Learnings:** None

**Outputs:** None

**Daily Summary:** None

---

**Generated:** 16:22 UTC on 2026-02-17
**Total Agents Queried:** 5

✅ Saved: /home/exedev/.openclaw/workspace/outputs/daily-digest-2026-02-17.md
```

### Specific Date

```bash
$ squad-output-digest --date 2026-02-16

📊 Squad Output Digest - 2026-02-16
...
```

## Features

- ✅ Queries all 5 squad agents via SSH
- ✅ Collects recent learnings (last 10)
- ✅ Collects recent outputs (last 5)
- ✅ Gets daily summary from memory
- ✅ Produces formatted markdown digest
- ✅ Saves to outputs directory
- ✅ Date-specific queries
- ✅ Email placeholder for Seneca integration

## Output Format

The digest is saved as markdown with sections for each agent:

```markdown
# Squad Output Digest - February 17, 2026

## Agent Name (Role)

**Learnings:**
  1. learning-file.md
  2. another-learning.md
  ...

**Outputs:**
  1. output-file.txt
  2. another-output.txt
  ...

**Daily Summary:** 2026-02-17.md

---

**Generated:** 16:22 UTC on 2026-02-17
**Total Agents Queried:** 5
```

## Scheduling

You can schedule this to run daily at 7 AM EST:

```bash
# Add to crontab
crontab -e

0 7 * * * squad-output-digest

# Or use systemd timer
systemctl --user edit squad-output-digest.timer
```

## Troubleshooting

### SSH Connection Failed

```bash
# Test SSH connection to each agent
ssh lobster-1 echo "test"
ssh marcus-squad echo "test"
ssh galen-squad echo "test"
ssh archimedes-squad echo "test"
ssh argus-squad echo "test"
```

### No Learnings Found

```bash
# Check if learnings directory exists
ssh marcus-squad 'ls -la ~/.openclaw/learnings/'

# Check permissions
ssh marcus-squad 'ls -ld ~/.openclaw/learnings/'
```

### Permissions Error

```bash
# Make script executable
chmod +x ~/.local/bin/squad-output-digest

# Check SSH key
ls -la ~/.ssh/id_rsa
```

## Future Enhancements

- [ ] Email integration (Seneca agentmail)
- [ ] Filter by agent type (research vs build vs ops)
- [ ] Aggregate trends over time
- [ ] Export to different formats (JSON, CSV)
- [ ] Web dashboard for viewing digests

## License

MIT License

## Author

OpenSeneca Squad Toolset

---

**Daily digest. One command.**

Justin can see everything your squad produced today.
