# Research Digest CLI

Extract key content from markdown research files for quick consumption.

**Purpose:** Scan Marcus and Galen's research files (`~/.openclaw/learnings/`) and extract tweet drafts, blog angles, key insights, recommendations, and conclusions. Seneca can quickly scan the squad's output without reading full files.

## Installation

Already deployed: symlinked to `~/.local/bin/research-digest`

```bash
# Verify installation
which research-digest

# Test it
research-digest
```

## Usage

```bash
# Scan default directory (~/.openclaw/learnings)
research-digest

# Scan specific directory
research-digest --dir ~/research

# Only recent files (since date)
research-digest --since 2026-02-15

# Save to file
research-digest --output digest.md

# JSON output (for programmatic use)
research-digest --json

# Combine options
research-digest --since 2026-02-18 --output recent-digest.md
```

## Extracted Patterns

The tool looks for these patterns in markdown files:

### High Priority (for quick scanning)
- `## Tweet Draft:` - Draft tweets for Seneca to post
- `BLOG ANGLE:` - Blog post angles/topics
- `SIGNUP:` - Newsletter signup CTAs

### Sections
- `## Key Insights` / `## Key Learnings` - Bullet points of insights
- `## Recommendations` - Actionable recommendations
- `## Conclusion` / `## Summary` - Main takeaways (truncated to 300 chars)

### Bullet Formats Supported
- `- Item` - Standard markdown bullet
- `• Item` - Unicode bullet
- `1. Item` - Numbered list
- `**Title** - Description` - Bold title with description

## Example Output

```
======================================================================
RESEARCH DIGEST
Found 3 files with extractable content
======================================================================

📄 2026-02-18 — Learning: CLI Tool Pattern Application
   Date: 2026-02-18

📌 The update-data.py script now follows best practices from squad-setup tool development:
   - Color-coded output - Visual hierarchy - Status command - Summary statistics - Better error handling
   **Impact:** - Better UX for Justin - Quick visibility into squad health - Reusable pattern for other tools ...

----------------------------------------------------------------------

📄 2026-02-18 — Learning: Google DeepMind Intelligent AI Delegation Framework
   Date: 2026-02-18

💡 Key Insights:
   • **Clear Roles** - HEARTBEAT.md and MEMORY.md define each agent's scope
   • **Specialization** - Agents have distinct capabilities (research, build, ops)
   • **Logging** - learnings/, outputs/, git provide audit trail
   • **Hub-and-Spoke** - Seneca coordinates, others execute

----------------------------------------------------------------------

📊 Summary:
   Tweet drafts: 0
   Blog angles: 0
   Total insights: 4
```

## JSON Mode

For programmatic use (e.g., feeding into other tools):

```bash
research-digest --json > digest.json
```

Output structure:
```json
[
  {
    "filename": "2026-02-18-learning.md",
    "title": "2026-02-18 — Learning: CLI Tool Pattern Application",
    "date": "2026-02-18",
    "tweet_draft": null,
    "blog_angle": null,
    "signup": null,
    "key_insights": ["Insight 1", "Insight 2"],
    "recommendations": ["Recommendation 1"],
    "conclusion": "The script now follows best practices..."
  }
]
```

## Development

**Author:** Archimedes
**Date:** 2026-02-19
**Language:** Python 3
**Location:** `~/workspace/tools/research-digest/`

### Adding New Patterns

Edit `research-digest.py` and add to the `PATTERNS` dictionary:

```python
PATTERNS = {
    'your_pattern': re.compile(r'^##\s+Your Pattern\s*$(.+?)(?=^##|\Z)', re.MULTILINE | re.IGNORECASE | re.DOTALL),
}
```

Then extract in `extract_from_file()` method.

## Integration Ideas

1. **Daily Cron** - Run at 7 AM EST, email digest to Justin via Seneca
2. **Squad Dashboard** - Display recent digest in dashboard
3. **Twitter Bot** - Auto-post extracted tweet drafts
4. **Blog Pipeline** - Feed blog angles into blog-publisher tool

## Notes

- Skips files in `archive/` subdirectory and `seed-*.md` files
- Limits to 10 insights/recommendations per file to keep digest manageable
- Conclusions truncated to 300 characters
- Supports standard markdown and custom bullet formats
