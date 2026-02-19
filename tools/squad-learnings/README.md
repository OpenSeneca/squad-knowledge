# Squad Learnings Aggregator

CLI tool to aggregate learnings from all OpenSeneca squad agents into a unified digest.

## What It Does

- Queries all squad agents for recent learnings
- Extracts key insights, tools, tweet drafts, and recommendations
- Creates a unified markdown digest organized by agent
- Supports SSH to remote agents with graceful fallback
- Filter by date range or specific agents

## Why This Tool

Justin has 5 agents producing learnings daily. Seeing everything in one place is hard. This tool:
- One command to see what everyone learned
- Structured extraction of key points
- Tweet drafts ready for posting
- Tools mentioned for reference

## Usage

```bash
# All agents, learnings from last 24 hours
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

## Output Format

The digest is organized by agent:

```markdown
# Squad Learnings - 2026-02-19

## Seneca (Coordinator)

### 2026-02-19-deepseek-v4-launch.md
_Date: 2026-02-19_

**Key Points:**
- DeepSeek V4 launched with 1T parameters
- Beats GPT-4 on benchmarks
- Open weights available

**Tools Mentioned:** paper-summarizer, squad-eval

**Tweet Draft:**
> DeepSeek V4 just launched with 1T parameters...

**Recommendations:**
- Evaluate for squad use
- Compare with Claude and GPT-4

---

## Marcus (Research (AI))
...
```

## What Gets Extracted

- **Key Points** - Bullet points from learning content
- **Tools Mentioned** - CLI tools, services, libraries referenced
- **Tweet Drafts** - Draft tweets ready for posting
- **Recommendations** - Actionable items for the squad

## Agent Configuration

The tool knows about all 5 squad agents:

| Agent | Role | Host | Tailscale IP |
|--------|-------|--------|---------------|
| Seneca | Coordinator | lobster-1 | 100.101.15.68 |
| Marcus | Research (AI) | marcus-squad | 100.98.223.103 |
| Archimedes | Build | archimedes-squad | 100.100.56.102 |
| Argus | Ops | argus-squad | 100.108.219.91 |
| Galen | Research (Biotech) | galen-squad | 100.123.121.125 |

## SSH vs Local

- **SSH preferred** - Queries remote agents via SSH for their learnings
- **Local fallback** - For archimedes-squad, reads local `~/.openclaw/learnings/`
- **Graceful degradation** - If SSH fails, marks agent as unavailable

## Error Handling

- SSH timeout: 5 seconds per agent
- Missing learnings directory: Shows "No learnings"
- Permission denied: Falls back gracefully
- Invalid learnings: Skipped, continues with other agents

## Integration Ideas

1. **Daily cron** - Run at 8 AM EST, email digest to Justin
2. **Dashboard integration** - Show recent learnings in Squad Dashboard
3. **Tweet automation** - Extract tweets and post via Seneca
4. **Slack/Signal** - Push digest to chat for team visibility

## Requirements

- Python 3.8+
- SSH access to remote agents (optional but recommended)
- Local `~/.openclaw/learnings/` directory for fallback

## Files

- `squad-learnings.py` - Main script (10,620 bytes)
- `README.md` - This file

## License

MIT

## Author

Archimedes (Build Agent) - OpenSeneca Squad
