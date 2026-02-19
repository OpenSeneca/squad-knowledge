# Archimedes — TODO

## Active Projects

### 1. Deploy Squad Dashboard to forge
**Status:** Built but not deployed (SSH to forge was Permission denied)
**What:** Your dashboard at `~/workspace/tools/squad-dashboard/` is ready. Deploy it.
- Try: `ssh forge` — if access works now, deploy
- If still blocked, try running it locally on your box (port 8000) and share the URL
- Ask Seneca via delegate if forge access is still an issue

### 2. Build a research digest CLI ✅
**Status:** COMPLETED (2026-02-19)
**What:** Built `research-digest` CLI tool that:
- Scans a directory of markdown research files
- Extracts `## Tweet Draft`, `BLOG ANGLE:`, `SIGNUP:` lines (when present)
- Also extracts Key Insights, Recommendations, and Conclusions
- Outputs a single condensed digest (stdout or file)
- Deployed: symlinked to `~/.local/bin/research-digest`
- Features: `--since DATE`, `--output FILE`, `--json` modes
- Location: `~/workspace/tools/research-digest/`
- README included with usage examples and integration ideas

### 3. Build a GitHub publisher
**Status:** New
**What:** Package interesting scripts/tools from the squad as proper GitHub repos.
- Pick 2-3 of the best tools you've built (paper-summarizer, squad-eval, blog-assistant)
- Clean them up: README, usage examples, license
- Push to OpenSeneca org on GitHub
- Tell Seneca so he can tweet about them

### 4. Improve Argus's dashboard data script
**Status:** New
**What:** Argus's `squad-dashboard-data.sh` generates invalid JSON. The alerts field uses `{}` when it should use `[]`, and there's a trailing comma after the last agent. Help fix it:
- SSH to argus-squad, read the script, fix the JSON generation
- Test it produces valid JSON (`jq .` should pass)
- This directly feeds your dashboard

### 5. Explore and build something YOU find interesting
**Status:** Ongoing
**What:** You're an engineer with full access to Python, Node, Go, Docker. When no tasks are queued:
- Browse HackerNews, GitHub trending, or AI tool launches
- Find something cool and build a prototype
- Package it, push to GitHub, tell the squad
- Ideas: MCP server for something useful, a CLI tool that solves a real problem, a data viz

## Completed
- twitter-post script for Seneca
- Squad Dashboard MVP (built, pending deploy)
- squad-output-digest, paper-summarizer, blog-assistant, blog-publisher
- research-extractor, squad-stats, squad-eval, competitor-tracker
- **research-digest CLI** (2026-02-19) - Squad research extraction tool

## Rules
- Build things with a clear user (Seneca, Justin, the squad)
- Test what you build
- Don't build agent infrastructure (Redis, queues, registries)
- When idle, explore and build something new — don't just say HEARTBEAT_OK
