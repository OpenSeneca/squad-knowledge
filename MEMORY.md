# Archimedes — Memory

Concise operational state. Detailed notes in `learnings/`.

## Identity
- **Role**: Engineering Lead (build tools, dashboard, prototypes)
- **Principal**: Justin Johnson (builds AI tools, writes about AI + biopharma)
- **Model**: GLM-4.7 on exe.dev (archimedes-squad), has Codex (GPT-5.3)

## Current Projects
- **Squad Dashboard** — Running locally on archimedes-squad (http://100.100.56.102:8080), needs SSH to deploy to forge
- CLI tools and utilities (25 tools deployed, see workspace/tools/)
- GitHub: OpenSeneca org (8 tools published)

## GitHub Published Tools (OpenSeneca Org)
1. **paper-summarizer** - https://github.com/OpenSeneca/paper-summarizer
   - Summarize arXiv papers and articles (305 lines, MIT)
2. **squad-eval** - https://github.com/OpenSeneca/squad-eval
   - Role-specific agent evaluation metrics (452 lines, MIT)
3. **blog-assistant** - https://github.com/OpenSeneca/blog-assistant
   - Generate blog outlines in Run Data Run style (358 lines, MIT)
4. **gh-agentics-helper** - https://github.com/OpenSeneca/gh-agentics-helper
   - GitHub Agentic Workflows setup CLI with 4 templates (4,630 lines, MIT)
5. **squad-learnings** - https://github.com/OpenSeneca/squad-learnings
   - Aggregate learnings from all squad agents into unified digest (440 lines, MIT)
6. **research-digest** - https://github.com/OpenSeneca/research-digest
   - Extract key content from squad research files (~360 lines, MIT)
7. **gh-release-monitor** - https://github.com/OpenSeneca/gh-release-monitor
   - Monitor GitHub releases from multiple repos without notification noise (~440 lines, MIT)
8. **squad-overview** - https://github.com/OpenSeneca/squad-overview
   - Complete picture of squad status, learnings, and productivity (~260 lines, MIT)

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
7. **dupe-finder** (2026-02-19) — Duplicate file detection and cleanup CLI
8. **gh-agentics-helper** (2026-02-19) — GitHub Agentic Workflows setup CLI with 4 templates
9. **squad-learnings** (2026-02-19) — Squad learnings aggregation CLI
10. **squad-overview** (2026-02-19) — Squad overview CLI (status, tools, learnings, metrics)
11. **squad-alerts** (2026-02-19) — Squad monitoring and alerting system
12. **squad-alerting-dashboard** (2026-02-19) — Squad alerting visual UI

**Total:** 25 tools, 2 dashboards (MVP + Local + Alerting), 8 published to GitHub, 50+ commits, ~400KB+ of code/docs

**Squad Dashboard Enhancements (2026-02-18):**
- deploy-forge.sh — Automated deployment script with PM2 integration
- update-data.py — Automated data collection from all agents
- Quick start guide — Comprehensive reference for all 16 tools

**Deployment Status:**
- ✅ All 25 CLI tools deployed (symlinked to ~/.local/bin/)
- ✅ Squad Dashboard running locally on archimedes-squad (http://100.100.56.102:8080)
- ✅ squad-alerting-dashboard ready (Squad alerting visual UI)
- ✅ squad-overview ready (Complete squad picture in one command)
- ✅ gh-agentics-helper ready (GitHub Agentic Workflows setup for all repos)
- ✅ squad-learnings ready (Squad learnings aggregation)
- ✅ research-digest ready (Research content extraction)
- ✅ gh-release-monitor ready (GitHub release tracking)
- ✅ tools/README.md ready (Central index of all tools)
- ⏳ Squad Dashboard deployment to forge blocked (SSH access issues)
- ⏳ Twitter-post ready (needs X_BEARER_TOKEN on lobster-1)

**SSH Access Issues (2026-02-19):**
- SSH to forge (100.93.69.117) - Permission denied
- SSH to argus-squad (100.108.219.91) - Permission denied/Host key verification
- Need to resolve SSH keys or use alternative deployment method
