# Squad Export Tool

Export squad data (status, learnings, tools) in unified formats for integration with multi-agent platforms like AionUi.

## What This Tool Does

**Squad Export** consolidates squad data from multiple sources into a single, unified format:

- **Agent Status** - From squad-dashboard data.json
- **Learnings** - From all agents' learning files
- **Tools Inventory** - From workspace/tools/ directory

Output formats: **JSON** (machine-readable) or **Markdown** (human-readable)

## Why This Tool

After researching **AionUi** (open-source multi-agent Cowork platform), I identified a gap:

**Current Squad Challenges:**
- Fragmented data sources (dashboard data, learnings files, tool directories)
- No unified export for external tools
- Manual aggregation required

**Squad Export Solutions:**
- Single command to export all squad data
- JSON format for AionUi/web integration
- Markdown format for documentation/sharing
- Filterable by agent, date, days

## Usage

### Export All Data (JSON)

```bash
squad-export --include-learnings --include-tools
```

### Export Specific Agents

```bash
squad-export --agents archimedes,marcus
```

### Export Recent Learnings

```bash
# Last 7 days
squad-export --include-learnings --days 7

# Since specific date
squad-export --include-learnings --since 2026-02-15
```

### Export as Markdown

```bash
squad-export --format markdown --output squad-export.md
```

### Combined Example

```bash
# Export all data for archimedes agent (last 7 days)
squad-export \
  --agents archimedes \
  --days 7 \
  --include-learnings \
  --include-tools \
  --format json \
  --output squad-export.json
```

## Options

| Option | Description | Default |
|---------|-------------|----------|
| `--format` | Output format: json, markdown | json |
| `--output, -o` | Output file path | stdout |
| `--since` | Filter learnings by date (YYYY-MM-DD) | None |
| `--days` | Include learnings from last N days | None |
| `--agents` | Comma-separated agent names | All agents |
| `--include-learnings` | Include learnings in export | False |
| `--include-tools` | Include tool inventory in export | False |
| `--workspace` | Path to workspace directory | ~/.openclaw/workspace |
| `--learnings` | Path to learnings directory | ~/.openclaw/learnings |

## Output Format

### JSON

```json
{
  "timestamp": "2026-02-20T01:35:00",
  "squad": {
    "agents": [
      {
        "id": "archimedes-squad",
        "name": "Archimedes",
        "role": "build",
        "status": "active",
        "last_output": "2026-02-19T12:35:00",
        "uptime_hours": 24.5,
        "activity_score": 85
      }
    ],
    "learnings": [
      {
        "filename": "2026-02-19-final-day-summary.md",
        "date": "2026-02-19",
        "agent": "archimedes",
        "preview": "Exceptionally productive day - 7 tools built...",
        "lines": 150
      }
    ],
    "tools": [
      {
        "name": "squad-overview",
        "path": "/path/to/squad-overview",
        "has_readme": true,
        "python_count": 1,
        "bash_count": 0,
        "deps_files": []
      }
    ]
  }
}
```

### Markdown

```markdown
# Squad Export

**Generated:** 2026-02-20T01:35:00

## Agent Status

| ID | Name | Role | Status | Uptime | Activity |
|----|------|------|--------|--------|----------|
| archimedes-squad | Archimedes | build | 🟢 active | 24.5h | 85 |

## Recent Learnings

### 2026-02-19 [archimedes]

**File:** `2026-02-19-final-day-summary.md`

Exceptionally productive day - 7 tools built, 8 GitHub repos published...

## Tools Inventory

### squad-overview

- **Language:** Python
- **README:** ✅
- **Files:** 1
```

## Integration with AionUi

AionUi is a free, open-source multi-agent Cowork platform that supports OpenClaw and provides:

- Unified interface for all agents
- Visual dashboard
- Scheduled automation
- Remote access (WebUI + Telegram)

**Using Squad Export with AionUi:**

1. **Export squad data:**
   ```bash
   squad-export --include-learnings --include-tools > squad.json
   ```

2. **Configure AionUi:**
   - Import squad.json into AionUi
   - Set up agents for each squad member
   - Configure scheduled tasks for periodic exports

3. **Automated monitoring:**
   ```bash
   # Add to crontab for daily exports
   0 9 * * * squad-export --days 1 --include-learnings > /tmp/squad-daily.json
   ```

## Use Cases

### 1. Daily Squad Status Reports

```bash
# Export recent data for daily report
squad-export --days 1 --format markdown > /tmp/squad-status.md
```

### 2. Integration with External Tools

```bash
# Export JSON for web dashboards
squad-export --include-learnings --include-tools --format json > api/squad-data.json
```

### 3. Agent-Specific Views

```bash
# View only research agents
squad-export --agents marcus,galen --include-learnings
```

### 4. Periodic Backups

```bash
# Cron job for weekly exports
0 0 * * 0 squad-export --days 7 --include-learnings --output backups/squad-weekly-$(date +\%Y\%m\%d).json
```

### 5. Documentation Generation

```bash
# Generate documentation from squad data
squad-export --format markdown --include-learnings --include-tools > docs/squad-overview.md
```

## Data Sources

| Data | Source | Format |
|-------|---------|---------|
| Agent Status | squad-dashboard/data.json | JSON |
| Learnings | ~/.openclaw/learnings/*.md | Markdown |
| Tools Inventory | workspace/tools/ | Directory scan |

## Technical Details

- **Language:** Python 3
- **Dependencies:** Standard library only (no external deps)
- **Output formats:** JSON, Markdown
- **File size detection:** Automatic preview generation

## Deployment

```bash
# Symlink to ~/.local/bin
cd ~/workspace/tools/squad-export
chmod +x squad-export.py
ln -s $(pwd)/squad-export.py ~/.local/bin/squad-export

# Verify installation
squad-export --help
```

## Testing

```bash
# Test JSON export
squad-export --format json | jq .

# Test Markdown export
squad-export --format markdown --include-learnings --days 1

# Test specific agents
squad-export --agents archimedes --include-tools
```

## Research Context

This tool was built after researching **AionUi** (https://github.com/iOfficeAI/AionUi), an open-source multi-agent Cowork platform that integrates with OpenClaw.

**Research findings:**
- Squad's data is fragmented across multiple sources
- No unified export for external integration
- AionUi provides unified interface, scheduled automation, remote access

**Squad Export solution:**
- Consolidates squad data into single export
- JSON format for AionUi integration
- Markdown format for documentation
- Filterable for specific use cases

See full research: `learnings/2026-02-20-aionui-research.md`

## Value for Squad

**For Justin:**
- One command to export all squad data
- JSON for AionUi/web dashboard integration
- Markdown for documentation/sharing
- Filterable views (agent-specific, date-filtered)

**For AionUi Integration:**
- Prepares squad data for unified interface
- Enables multi-agent parallel execution
- Supports scheduled automation
- Provides data for visual dashboard

**For Documentation:**
- Generates squad status reports
- Creates tool inventory documentation
- Aggregates learnings for sharing

## Future Enhancements

- [ ] Add web server mode for real-time data serving
- [ ] Include squad-alerts history in export
- [ ] Add Git commit history for each tool
- [ ] Export in additional formats (CSV, HTML)
- [ ] Add GraphQL API for external tools
- [ ] Include test results from squad-eval

## License

MIT

---

**Tool:** squad-export
**Version:** 1.0
**Author:** Archimedes (OpenSeneca squad)
**Date:** 2026-02-20
