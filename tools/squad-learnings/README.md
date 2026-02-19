# Squad Learnings Aggregator

Aggregate learnings from all OpenSeneca squad agents into a unified digest.

## What It Does

- Queries all 5 squad agents (Seneca, Marcus, Archimedes, Argus, Galen)
- Extracts structured insights from learning files:
  - Key Points - Bullet points from content
  - Tools Mentioned - CLI tools, services, libraries
  - Tweet Drafts - Ready-to-post tweets
  - Recommendations - Actionable items
- Organizes by agent in unified markdown digest
- Filter by date range (YYYY-MM-DD-*.md pattern)
- SSH to remote agents with graceful fallback

## Why This Tool

Justin has 5 agents producing learnings daily. Seeing everything in one place is hard. This tool:
- One command to see what everyone learned
- Structured extraction of key insights
- Tweet drafts ready for posting
- Tools mentioned for reference

## Installation

```bash
# Clone to workspace
cd ~/.openclaw/workspace/tools/squad-learnings

# Symlink to PATH
ln -sf "$(pwd)/squad-learnings.py" ~/.local/bin/squad-learnings

# Make executable
chmod +x ~/.local/bin/squad-learnings
```

## Usage

```bash
# All agents, last 24 hours
squad-learnings

# Last 7 days
squad-learnings --days 7

# Specific agents only
squad-learnings --agents marcus galen

# Save to file
squad-learnings --output squad-digest.md

# Combine filters
squad-learnings --days 3 --agents marcus galen --output digest.md
```

## Requirements

- Python 3.8+
- SSH access to remote agents (optional but recommended)
- Local `~/.openclaw/learnings/` directory for fallback

## Agent Configuration

The tool knows about all 5 squad agents:

| Agent | Role | Host | Tailscale IP |
|--------|-------|--------|---------------|
| Seneca | Coordinator | lobster-1 | 100.101.15.68 |
| Marcus | Research (AI) | marcus-squad | 100.98.223.103 |
| Archimedes | Build | archimedes-squad | 100.100.56.102 |
| Argus | Ops | argus-squad | 100.108.219.91 |
| Galen | Research (Biotech) | galen-squad | 100.123.121.125 |

## Output Format

```markdown
# Squad Learnings - 2026-02-19

**Generated:** 2026-02-19 05:56 UTC
**Total Learnings:** 4

## Seneca (Coordinator)

### 2026-02-19-deepseek-v4-launch.md
_Date: 2026-02-19_

**Key Points:**
- DeepSeek V4 launched with 1T parameters
- Beats GPT-4 on benchmarks
- Open weights available

**Tools:** paper-summarizer, squad-eval

**Tweet Draft:**
> DeepSeek V4 just launched with 1T parameters...

**Recommendations:**
- Evaluate for squad use
- Compare with Claude and GPT-4

---

## Summary

**Tools Mentioned:** paper-summarizer, squad-eval, blog-assistant
**Tweet Drafts:** 2 ready
**Recommendations:** 5 items
```

## Error Handling

- SSH timeout: 5 seconds per agent
- SSH failure: Falls back gracefully, marks agent unavailable
- Missing learnings directory: Shows "No learnings"
- Invalid learning files: Skipped, continues with other agents

## Integration Ideas

1. **Daily cron** - Run at 8 AM EST, email digest to Justin via Seneca
2. **Dashboard integration** - Show recent learnings in Squad Dashboard
3. **Tweet automation** - Extract tweets and post via Seneca
4. **Slack/Signal** - Push digest to chat for team visibility

## Files

- `squad-learnings.py` - Main script (440 lines)
- `README.md` - This file
- `test-digest.md` - Example output (included for reference)

## License

MIT

## Author

Archimedes (Build Agent) - OpenSeneca Squad
