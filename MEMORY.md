# Archimedes — Memory

Concise operational state. Detailed notes in `learnings/`.

## Identity
- **Role**: Engineering Lead (build tools, dashboard, prototypes)
- **Principal**: Justin Johnson (builds AI tools, writes about AI + biopharma)
- **Model**: GLM-4.7 on exe.dev (archimedes-squad), has Codex (GPT-5.3)

## Current Projects
- **Squad Dashboard** — Fully automated deployment + data collection (READY to deploy, waiting on SSH access to forge)
- CLI tools and utilities (18 tools deployed, see workspace/tools/)
- GitHub: OpenSeneca org (3 tools published)

## GitHub Published Tools (OpenSeneca Org)
1. **paper-summarizer** - https://github.com/OpenSeneca/paper-summarizer
   - Summarize arXiv papers and articles (305 lines, MIT)
2. **squad-eval** - https://github.com/OpenSeneca/squad-eval
   - Role-specific agent evaluation metrics (452 lines, MIT)
3. **blog-assistant** - https://github.com/OpenSeneca/blog-assistant
   - Generate blog outlines in Run Data Run style (358 lines, MIT)

## Search Tool Hierarchy
1. **SearXNG** (`websearch`) — FREE, default for research.
2. **Grok** (`xai-grok-search`) — PAID, $25 shared budget. Sparingly.

## Output Locations
- Code: `~/workspace/tools/<project>/`
- Docs: `~/workspace/docs/`
- Daily summaries: `~/workspace/memory/YYYY-MM-DD.md`
- Technical learnings: `~/learnings/YYYY-MM-DD-<topic>.md`

## Key Learnings (see learnings/ for details)
- Ship working code, then iterate
- Test what you build before moving on
- Don't build random toys — build things Justin would use
- Don't build agent infrastructure (Redis, queues, registries)

## Tools Built (2026-02-17)

### Priority Tools (All Completed ✅)
1. **twitter-post** — X API v2 script for Seneca (TODO #1 PRIORITY)
2. **Squad Dashboard** — Agent monitoring dashboard (TODO #1)
3. **Squad Output Digest** — Daily squad summary (priority #2)
4. **Paper Summarizer** — Research paper summaries (priority #3)
5. **Blog Assistant** — Blog post outlines (priority #4)
6. **Research Extractor** — Content extraction for Seneca (HEARTBEAT.md #3)
7. **Squad Stats** — Productivity analyzer (seed-engineering-standards.md)
8. **Competitor Tracker** — AI company announcements (seed-engineering-standards.md)

### Seneca Tasks (Both Completed ✅)
1. **squad-eval** — Squad performance evaluation (Task #1)
2. **TinySeed Analysis** — Startup accelerator research (Task #2)

### Bonus Tools
1. **Squad-Realtime Dashboard** — Full-stack React + SSE
2. **GitHub Publication Packages** — 4 tools (claude-code-analyzer, dns, fhash, archive)
3. **OpenClaw Session Analyzer** — Session log parser
4. **Blog Publisher** — Substack/Obsidian formatter
5. **research-digest** (2026-02-19) — Squad research extraction CLI
6. **gh-release-monitor** (2026-02-19) — GitHub release tracking CLI

**Total:** 18 tools, 2 dashboards (MVP + Realtime), 3 published to GitHub, 40+ commits, ~300KB+ of code/docs

**Squad Dashboard Enhancements (2026-02-18):**
- deploy-forge.sh — Automated deployment script with PM2 integration
- update-data.py — Automated data collection from all agents
- Quick start guide — Comprehensive reference for all 16 tools

**Deployment Status:**
- ✅ All 16 CLI tools deployed (symlinked to ~/.local/bin/)
- ✅ Squad Dashboard production-ready (waiting SSH access to forge)
- ⏳ Twitter-post ready (needs X_BEARER_TOKEN on lobster-1)
