# GitHub Release Monitor CLI

Monitor GitHub repositories for new releases and generate digests.

**Purpose:** Track releases from AI companies, tools, and libraries you care about without the noise of GitHub notifications. Get a clean, filtered digest of what's new.

## Installation

Symlink from workspace:

```bash
ln -s /path/to/gh-release-monitor.py ~/.local/bin/gh-release-monitor
chmod +x ~/.local/bin/gh-release-monitor
```

Already deployed: `~/.local/bin/gh-release-monitor`

## Usage

### Monitor specific repositories

```bash
gh-release-monitor --repos openai/openai-python langchain-ai/langchain
```

### Use a config file

```bash
# Create repos.txt
echo "openai/openai-python" > repos.txt
echo "langchain-ai/langchain" >> repos.txt
echo "microsoft/semantic-kernel" >> repos.txt

# Use config
gh-release-monitor --config repos.txt
```

### Filter by date

```bash
# Only releases since Feb 15, 2026
gh-release-monitor --config repos.txt --since 2026-02-15
```

### Filter by keywords

```bash
# Only releases mentioning specific keywords
gh-release-monitor --repos openai/openai-python --keywords "api gpt"
```

### JSON output (for automation)

```bash
gh-release-monitor --repos openai/openai-python --json > releases.json
```

### Markdown output (for blog posts)

```bash
gh-release-monitor --repos openai/openai-python --markdown > releases.md
```

### Include release notes

```bash
gh-release-monitor --repos openai/openai-python --show-body
gh-release-monitor --config repos.txt --markdown --show-body
```

### Save to file

```bash
gh-release-monitor --config repos.txt --output digest.md
```

## Examples

### Check for new releases

```bash
$ gh-release-monitor --repos openai/openai-python

📡 Monitoring 1 repository(ies)...
  Fetching openai/openai-python...

======================================================================
GITHUB RELEASE MONITOR
Found 3 release(s)
======================================================================

## openai-python/releases

📦 v2.21.0
   Name: v2.21.0
   Published: 2026-02-14 00:11 UTC
   By: @stainless-app[bot]
   URL: https://github.com/openai/openai-python/releases/tag/v2.21.0

----------------------------------------------------------------------

📦 v2.20.0
   Name: v2.20.0
   Published: 2026-02-10 19:02 UTC
   By: @stainless-app[bot]
   URL: https://github.com/openai-python/releases/tag/v2.20.0

----------------------------------------------------------------------
```

### Filter by date and keywords

```bash
$ gh-release-monitor --config repos.txt --since 2026-02-15 --keywords "feature api"

📡 Monitoring 3 repository(ies)...
  Fetching openai/openai-python...
  Fetching langchain-ai/langchain...
  Fetching microsoft/semantic-kernel...
  Filtered to 2 release(s) since 2026-02-15
  Filtered to 1 release(s) by keywords

📦 v2.21.0
   Name: v2.21.0
   Published: 2026-02-14 00:11 UTC
   URL: https://github.com/openai/openai-python/releases/tag/v2.21.0
----------------------------------------------------------------------
```

### Markdown output for blog

```bash
$ gh-release-monitor --repos openai/openai-python --markdown --show-body

# GitHub Releases

## openai-python/releases

### v2.21.0

**Name:** v2.21.0
**Published:** 2026-02-14 00:11 UTC
**By:** @stainless-app[bot]
**URL:** [https://github.com/openai/openai-python/releases/tag/v2.21.0](https://github.com/openai/openai-python/releases/tag/v2.21.0)

**Notes:**

## 2.21.0 (2026-02-13)

### Features
* **api:** container network_policy and skills

### Bug Fixes
* **structured outputs:** resolve memory leak in parse methods

---

```

## Config File Format

Create a plain text file with one repository per line:

```text
# AI SDKs
openai/openai-python
anthropic/anthropic-sdk-python

# Frameworks
langchain-ai/langchain
microsoft/semantic-kernel

# Tools
huggingface/transformers
openai/whisper
```

Lines starting with `#` are ignored as comments.

## Features

- ✅ Monitor multiple repositories
- ✅ Config file support (one repo per line)
- ✅ Date filtering (since YYYY-MM-DD)
- ✅ Keyword filtering (name + body)
- ✅ Multiple output formats (text, JSON, Markdown)
- ✅ Include release notes (truncated)
- ✅ 5-minute caching (reduces API calls)
- ✅ Prerelease/Draft badges
- ✅ Uses `gh` CLI for authentication

## Caching

The tool caches releases for 5 minutes to reduce API calls:

```
~/.cache/gh-release-monitor/
  ├── owner_repo1.json
  ├── owner_repo2.json
  └── ...
```

Cache is automatically updated when expired.

## Use Cases

### For Justin (Blog Writing)

Track AI tool releases for blog posts:

```bash
# Check daily for new releases
gh-release-monitor --config ai-tools.txt --since 2026-02-19

# Generate markdown for blog
gh-release-monitor --config ai-tools.txt --markdown --show-body > blog-content.md
```

### For Research (Marcus/Galen)

Monitor specific research repos:

```bash
gh-release-monitor --repos huggingface/transformers stanfordnlp/stanza
```

### For Ops (Argus)

Monitor tooling updates:

```bash
gh-release-monitor --repos tailscale/tailscale kubernetes/kubernetes
```

### For Alerts

Set up daily cron:

```bash
# Add to crontab
crontab -e

0 9 * * * gh-release-monitor --config repos.txt --since yesterday > ~/releases-digest.txt
```

## Output Formats

### Text (default)
Human-readable, grouped by repository, shows release metadata.

### JSON
Machine-readable, includes full release body. Good for automation.

### Markdown
Blog-friendly, formatted with headers and links. Great for Run Data Run posts.

## Authentication

The tool uses `gh` CLI for authentication:

```bash
# Login (if not already)
gh auth login

# Check auth status
gh auth status
```

Or set `GITHUB_TOKEN` environment variable.

## Troubleshooting

### "gh: Not Found (HTTP 404)"

Repository doesn't exist or is misspelled:

```bash
# Wrong
gh-release-monitor --repos openai/python

# Right
gh-release-monitor --repos openai/openai-python
```

### No releases found

Some repos don't have releases (only tags):

```bash
# Check tags instead
gh release list -R owner/repo --limit 10
```

### "gh: command not found"

Install GitHub CLI:

```bash
# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Or via brew
brew install gh
```

## Integration Ideas

1. **Daily Digest** - Cron job runs daily, emails digest to Justin
2. **Blog Content** - Feed markdown output to blog-assistant
3. **Slack/Discord** - Post to squad channels when important releases drop
4. **Dashboard** - Integrate into Squad Dashboard

## Tips

1. **Use config files** for lists of repos
2. **Add comments** to config files for organization
3. **Filter by date** to only see recent releases
4. **Use keywords** to find specific features
5. **Markdown output** is great for blog posts

## Limitations

- Requires `gh` CLI or `GITHUB_TOKEN`
- 5-minute cache (not real-time)
- No webhooks (polling only)
- Pagination limited to 10 releases per repo (configurable)

## Future Enhancements

- [ ] Webhook support (push notifications)
- [ ] Tag filtering (e.g., only v1.x.x)
- [ ] Release comparison (diff between versions)
- [ ] Email/SMS notifications
- [ ] Squad Dashboard integration

## License

MIT License

## Author

OpenSeneca Squad Toolset

---

**Track releases. Stay informed. Never miss an update.**
