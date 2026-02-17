# Competitor Tracker — Track AI Company Announcements

Rolling log of AI company product launches, features, and announcements.

## What It Does

Track what AI companies ship:

- **Add announcements** — New product releases, features, partnerships
- **Query database** — Search by company, action, or keywords
- **Generate reports** — Summary of recent activity
- **List companies** — See all tracked companies

## Why This Matters

For Justin's blog posts:

- **Reference material** — What AI companies shipped recently
- **Competitive intelligence** — Who's launching what
- **Blog content** — Real examples for posts
- **Trends tracking** — What's happening in AI industry

## Installation

```bash
ln -s /path/to/competitor-tracker.py ~/.local/bin/competitor-tracker
chmod +x competitor-tracker.py
```

Already symlinked in this workspace: `~/.local/bin/competitor-tracker`

## Usage

### Add Announcement

```bash
competitor-tracker add --company "OpenAI" --action "Released GPT-5" --source "https://openai.com" --implication "Major LLM advancement"
```

### Query Announcements

```bash
# Query by company
competitor-tracker query --company "OpenAI" --days 30

# Query by keyword
competitor-tracker query --company "*" --days 7
```

### Generate Report

```bash
# Last 7 days
competitor-tracker report --days 7

# Last 30 days
competitor-tracker report --days 30
```

### List Companies

```bash
competitor-tracker list
```

## Examples

### Add New Announcement

```bash
$ competitor-tracker add --company "Anthropic" --action "Released Claude 4" --source "https://anthropic.com/claude4" --implication "Major GPT competitor, 200K context"

✓ Added announcement for Anthropic: Released Claude 4
```

### Query Recent Activity

```bash
$ competitor-tracker query --days 7

Recent announcements (last 7 days):
OpenAI: Released GPT-5
  Action: Released GPT-5
  Source: https://openai.com/gpt5
  Implication: Major advancement in LLMs
  Date: 2026-02-17

Anthropic: Released Claude 4
  Action: Released Claude 4
  Source: https://anthropic.com/claude4
  Implication: Major GPT competitor, 200K context
  Date: 2026-02-16
```

### Generate Weekly Report

```bash
$ competitor-tracker report --days 7

Weekly AI Competitor Report (Feb 11 - Feb 17, 2026)
======================================================

Companies tracked: 2
Announcements this week: 2

OpenAI:
- Released GPT-5 (Feb 17)
  Source: https://openai.com/gpt5
  Implication: Major advancement in LLMs

Anthropic:
- Released Claude 4 (Feb 16)
  Source: https://anthropic.com/claude4
  Implication: Major GPT competitor, 200K context

Top active companies: OpenAI (1), Anthropic (1)
```

### List All Companies

```bash
$ competitor-tracker list

Tracked companies:
- OpenAI
- Anthropic
- Google DeepMind
- Meta AI
- xAI
- Microsoft
- Amazon

Total: 7 companies
```

## Data Storage

Data stored in JSON file:

```
~/.openclaw/workspace/data/competitors.json
```

Format:

```json
{
  "metadata": {
    "created": "2026-02-17T...",
    "last_updated": "2026-02-17T...",
    "version": "1.0",
    "total_announcements": 10
  },
  "announcements": [
    {
      "id": "unique-id",
      "company": "OpenAI",
      "action": "Released GPT-5",
      "source": "https://openai.com",
      "implication": "Major LLM advancement",
      "date": "2026-02-17T..."
    }
  ]
}
```

## Features

- ✅ **Add announcements** — New product releases, features, partnerships
- ✅ **Query database** — Search by company, time period
- ✅ **Generate reports** — Weekly/monthly summaries
- ✅ **List companies** — See all tracked companies
- ✅ **Company tracking** — Normalizes company names
- ✅ **Source URLs** — Links to original announcements
- ✅ **Implications** — Track competitive impact
- ✅ **Time filtering** — Query by days/weeks/months
- ✅ **JSON storage** — Easy to backup and sync

## Use Cases

### For Justin (Blog Posts)

```bash
# Check what shipped this week
competitor-tracker report --days 7

# Search for specific company
competitor-tracker query --company "OpenAI" --days 30

# Get reference for blog post
competitor-tracker list
```

**Use in blog posts:**
- "OpenAI shipped GPT-5 last week..."
- "Anthropic's Claude 4 release shows..."
- "Here's what AI companies shipped in February..."

### For Competitive Intelligence

```bash
# Monitor competitor activity
competitor-tracker report --days 7

# Track specific company
competitor-tracker query --company "Anthropic" --days 90

# Identify trends
competitor-tracker report --days 180
```

### For Research Reference

```bash
# What shipped when researching GPT-5?
competitor-tracker query --company "OpenAI" --days 365

# Recent LLM releases
competitor-tracker report --days 30 | grep -i "llm"
```

## Integration with Other Tools

### Squad Output Digest

```bash
# Get squad activity
squad-output-digest

# Check what competitors shipped
competitor-tracker report --days 7

# Compare: squad insights vs competitive landscape
```

### Blog Assistant

```bash
# Get competitive announcements
competitor-tracker report --days 30

# Use in blog outline
blog-assistant --topic "AI Race" --notes competitive-report.md
```

## Best Practices

### Adding Announcements

**Be specific:**

```bash
# Good
competitor-tracker add --company "OpenAI" --action "Released GPT-5 with 1M context window and multimodal capabilities" --source "..." --implication "Major leap in LLM capabilities, competitive with Claude"

# Avoid
competitor-tracker add --company "OpenAI" --action "New model"
```

**Include implications:**

```bash
# Why does this matter?
competitor-tracker add --company "Anthropic" --action "Released Claude 4" --implication "200K context challenges GPT-5, Anthropic catching up in frontier models"
```

### Querying

**Use time filters:**

```bash
# Last week
competitor-tracker report --days 7

# Last month
competitor-tracker report --days 30

# Last quarter
competitor-tracker report --days 90
```

**Track specific companies:**

```bash
# OpenAI activity
competitor-tracker query --company "OpenAI" --days 180

# All LLM companies
for company in "OpenAI" "Anthropic" "Google" "Meta"; do
  competitor-tracker query --company "$company" --days 30
done
```

## Data Management

### Backup

```bash
# Backup JSON database
cp ~/.openclaw/workspace/data/competitors.json ~/backup/competitors-$(date +%Y%m%d).json
```

### Export

```bash
# Export to CSV
cat ~/.openclaw/workspace/data/competitors.json | jq -r '.announcements[] | [.company, .action, .date] | @csv' > competitors.csv
```

### Sync

```bash
# Sync with remote (optional)
rsync ~/.openclaw/workspace/data/competitors.json backup-server:/data/
```

## Common Company Names

The tool normalizes company names:

- `openai` → `OpenAI`
- `anthropic` → `Anthropic`
- `google deepmind` / `deepmind` → `Google DeepMind`
- `meta ai` → `Meta AI`
- `xai` → `xAI`

## Troubleshooting

### No Data Found

```bash
# Check if database exists
ls -la ~/.openclaw/workspace/data/competitors.json

# Initialize if missing
echo '{"metadata":{}, "announcements":[]}' > ~/.openclaw/workspace/data/competitors.json
```

### JSON Decode Error

```bash
# Check JSON syntax
cat ~/.openclaw/workspace/data/competitors.json | jq .

# Backup and recreate
cp ~/.openclaw/workspace/data/competitors.json competitors-backup.json
# Manually fix or recreate
```

### Command Not Found

```bash
# Check symlink
ls -la ~/.local/bin/competitor-tracker

# Recreate if needed
ln -s ~/.openclaw/workspace/tools/competitor-tracker/competitor-tracker.py ~/.local/bin/competitor-tracker
```

## Future Enhancements

- [ ] Export to markdown for blog posts
- [ ] Tag support (LLM, vision, multimodal, etc.)
- [ ] Graph output (activity over time)
- [ ] Email alerts (via Seneca)
- [ ] RSS feed import
- [ ] Company comparison view
- [ ] Integration with squad-dashboard

## Limitations

- **Manual entry** — Requires manual addition of announcements
- **No auto-import** — Doesn't automatically scrape company blogs
- **Single user** — No multi-user support or collaboration
- **Local only** — Stored locally, no cloud sync

## License

MIT License

## Author

OpenSeneca Squad Toolset

---

**Track what AI ships. Competitive intelligence.**

For Justin's blog posts and competitive analysis.
