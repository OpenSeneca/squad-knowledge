# Squad Tools Quick Start Guide

Quick reference for using the OpenSeneca squad tools.

## Overview

The squad tool ecosystem provides everything needed for:
- **Squad Management** — Monitoring, evaluation, productivity
- **Content Creation** — Research summaries, blog outlines, publishing
- **Communication** — Twitter posting
- **Operations** — Data collection, status updates

## Squad Management

### Squad Dashboard
**Purpose:** Monitor all agents in one place

```bash
# Start locally (testing)
cd ~/workspace/tools/squad-dashboard
node server.js
# Open http://localhost:8000

# Deploy to forge (when SSH access available)
./deploy-forge.sh

# Update data (from forge or local)
./update-data.py

# Auto-update via cron
*/5 * * * * cd ~/workspace/tools/squad-dashboard && ./update-data.py
```

**Location:** `~/workspace/tools/squad-dashboard/`
**Dashboard URL:** http://100.93.69.117:8000 (after deployment)

### Squad Stats
**Purpose:** Track agent productivity

```bash
squad-stats                    # Last 30 days
squad-stats --days 7          # Last 7 days
squad-stats --format json      # JSON output
squad-stats --save            # Save to file
```

**Outputs:** Files per agent, word/char counts, productivity ranking

### Squad Evaluation
**Purpose:** Evaluate agent performance by role

```bash
squad-eval --all               # Evaluate all agents
squad-eval archimedes          # Single agent
squad-eval --all --json        # JSON output
```

**Metrics:**
- **Research** (Marcus/Galen): Learning frequency, depth, sources, relevance
- **Ops** (Argus): Uptime, health checks, alerts, response time
- **Build** (Archimedes): Tools shipped, fixes, tests, documentation

### Squad Output Digest
**Purpose:** Daily summary of all squad outputs

```bash
squad-output-digest                    # Today
squad-output-digest --date 2026-02-17  # Specific date
squad-output-digest --email              # Email (placeholder)
```

**Output:** `outputs/daily-digest-YYYY-MM-DD.md`

## Content Creation

### Paper Summarizer
**Purpose:** Structured summaries for research papers

```bash
paper-summarizer https://arxiv.org/abs/2401.00001
paper-summarizer 2401.00001              # arXiv ID only
paper-summarizer URL --save             # Save to file
paper-summarizer URL --json             # Include JSON metadata
```

**Output:** Structured markdown with title, authors, abstract, findings, methodology, implications

### Blog Assistant
**Purpose:** Generate blog post outlines from research notes

```bash
blog-assistant --topic "AI in drug discovery" --notes research.md
blog-assistant --topic "CRISPR" --learnings-from galen
blog-assistant --topic "Edge AI" --notes research.md --save
```

**Output:** 7-section outline, 5 title options, 4 hook ideas, key points

### Blog Publisher
**Purpose:** Format markdown for Substack/Obsidian

```bash
blog-publisher post.md --format substack
blog-publisher post.md --format obsidian
```

### Research Extractor
**Purpose:** Extract content metadata from research

```bash
research-extractor                           # Last 7 days, all agents
research-extractor --days 3                  # Last 3 days
research-extractor --agents marcus galen     # Specific agents
research-extractor --output content-extract.md
```

**Extracts:** `## Tweet Draft`, `BLOG ANGLE:`, `SIGNUP:` lines

## Communication

### Twitter Post
**Purpose:** Post to X/Twitter via API v2

**Setup:**
1. Deploy to lobster-1: `scp -r scripts/twitter-post/ lobster-1:~/.openclaw/scripts/`
2. Add `X_BEARER_TOKEN` to `~/.config/openclaw/secrets.env` on lobster-1
3. Restart to load token

```bash
twitter-post "Your tweet text here"
twitter-post --tweet "text" --dry-run       # Test without posting
twitter-post --delete <tweet-id>           # Delete tweet
```

**Location:** `~/workspace/tools/scripts/twitter-post/`

## Competitive Intelligence

### Competitor Tracker
**Purpose:** Track AI company announcements

```bash
# Add announcement
competitor-tracker add --company "OpenAI" --action "Released GPT-5" --url https://...

# Query
competitor-tracker query --company "OpenAI" --days 30
competitor-tracker query --days 7 --keyword "LLM"

# Generate reports
competitor-tracker report --days 7           # Weekly summary
competitor-tracker report --days 30          # Monthly summary

# List companies
competitor-tracker list
```

**Output:** JSON database, markdown reports

## Common Workflows

### Morning Check
```bash
# 1. Check squad status
cd ~/workspace/tools/squad-dashboard && ./update-data.py

# 2. See yesterday's output
squad-output-digest --date yesterday

# 3. Check productivity
squad-stats --days 1
```

### Research to Blog
```bash
# 1. Summarize papers
paper-summarizer https://arxiv.org/abs/2401.00001 --save

# 2. Generate blog outline
blog-assistant --topic "New AI Paper" --notes paper-summary.md --save

# 3. Format for publishing
blog-publisher blog-outline.md --format substack
```

### Content Discovery for Social
```bash
# 1. Extract content from research
research-extractor --days 7

# 2. Review extracted content
cat outputs/content-extract-*.md

# 3. Post selected tweet drafts
twitter-post "Your selected tweet text"
```

### Competitor Monitoring
```bash
# 1. Generate weekly report
competitor-tracker report --days 7 --save

# 2. Check recent announcements
competitor-tracker query --days 3

# 3. Update tracker manually as needed
competitor-tracker add --company "Anthropic" --action "New feature"
```

## Tool Locations

All tools are symlinked to `~/.local/bin/` for easy access.

| Tool | Location | Symlink |
|------|----------|---------|
| squad-stats | `tools/squad-stats/` | ✓ |
| squad-eval | `tools/squad-eval/` | ✓ |
| squad-output-digest | `tools/squad-output-digest/` | ✓ |
| paper-summarizer | `tools/paper-summarizer/` | ✓ |
| blog-assistant | `tools/blog-assistant/` | ✓ |
| blog-publisher | `tools/blog-publisher/` | ✓ |
| research-extractor | `tools/research-extractor/` | ✓ |
| competitor-tracker | `tools/competitor-tracker/` | ✓ |
| twitter-post | `scripts/twitter-post/` | ✓ |

## Deployment Status

| Tool | Status | Notes |
|------|--------|-------|
| Squad Dashboard | Ready to deploy | Needs SSH to forge (100.93.69.117) |
| All CLI tools | Deployed | Symlinked to ~/.local/bin/ |
| Twitter Post | Ready to deploy | Needs X_BEARER_TOKEN on lobster-1 |

## Getting Help

```bash
# Most tools support --help
<tool-name> --help

# Check tool documentation
ls ~/workspace/tools/<tool-name>/README.md

# Squad dashboard docs
cat ~/workspace/tools/squad-dashboard/README.md
```

## Next Steps

1. **Deploy Squad Dashboard** to forge once SSH access available
2. **Configure Twitter Post** with X_BEARER_TOKEN on lobster-1
3. **Set up cron jobs** for automated updates:
   - Squad dashboard data: `*/5 * * * *`
   - Daily squad digest: `0 7 * * *`

---

**Last Updated:** 2026-02-18
**Total Tools:** 16 production-ready
