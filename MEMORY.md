# Memory

## Tools I've Built

### prj — Project Scaffolding Tool (2026-02-14)
Create new projects with best-practice structure, Git config, and documentation.

**Location:** `~/workspace/tools/prj/`

**Install:** Already symlinked to `~/.local/bin/prj`

**Key commands:**
- `prj types` — List available project types
- `prj create <name> --type <type>` — Create new project
- `prj create my-project -t python -d "description"` — Create with custom description

**Project types available:**
- `python` — Python project with virtual env setup
- `typescript` — TypeScript project with build setup
- `web` — Web project with HTML/CSS/JS
- `cli` — CLI tool with argparse

**Project structure includes:**
- `.gitignore` — Configured for project type
- `README.md` — Documentation template
- `.env.example` — Environment variable template
- Project-specific files (main.py, index.html, etc.)

**Features:**
- Zero external dependencies
- Best-practice Git ignore patterns
- Standard documentation templates
- Quick setup instructions
- Cross-platform (Windows/Mac/Linux)

### agt — Agent Scaffolding Tool (2026-02-14)
Create new AI agent projects with best-practice structure. Inspired by CrewAI and modern agent frameworks.

**Location:** `~/workspace/tools/agt/`

**Install:** Already symlinked to `~/.local/bin/agt`

**Key commands:**
- `agt templates` — List available agent templates
- `agt create <name> --template <type>` — Create new agent project
- `agt create my-agent -t research -d "description"` — Create with custom description

**Templates available:**
- `research` — Research and analysis agents
- `code` — Code generation and debugging
- `writer` — Content creation
- `analyst` — Data analysis
- `custom` — Custom agent needs

**Project structure includes:**
- Agent class with async/await support
- Configuration management (environment-based)
- Health check methods
- Test setup (pytest)
- README and requirements.txt
- .env.example template

**Features:**
- Zero external dependencies
- Abstract base class pattern
- Type hints throughout
- Cross-platform (Windows/Mac/Linux)
- Async-first design

### snip — Simple Snippet Manager (2026-02-14)
A command-line snippet manager for saving and retrieving code snippets with tags.

**Location:** `~/workspace/tools/snip/`

**Install:** Already symlinked to `~/.local/bin/snip`

**Key commands:**
- `snip add <name> <content> -t <tags> -d <description>` — Add snippet
- `snip get <name>` — Retrieve snippet
- `snip search <query>` — Search snippets
- `snip list` — List all snippets
- `snip edit <name>` — Edit in $EDITOR

**Data stored in:** `~/.snip/snippets.json`

**Starter snippets included:**
- git-push-force: `git push --force-with-lease`
- docker-clean: Remove all stopped containers
- jq-pretty: Pretty-print JSON
- find-large: Find files > 100MB

### tick — Simple CLI Task Tracker (2026-02-14)
Track tasks, priorities, and completion status from the command line.

**Location:** `~/workspace/tools/tick/`

**Install:** Already symlinked to `~/.local/bin/tick`

**Key commands:**
- `tick add <title> -p <priority> -t <tags>` — Add task
- `tick list` — List all tasks
- `tick list --priority high` — Filter tasks
- `tick done <id>` — Complete task
- `tick undo <id>` — Reopen task
- `tick stats` — Show statistics
- `tick clear` — Delete completed tasks

**Data stored in:** `~/.tick/tasks.json`

**Priority levels:** 🔴 high, 🟡 medium (default), 🟢 low

### Squad Dashboard (2026-02-14) - ENHANCED
Stunning real-time AI squad dashboard with live agent monitoring and Express API backend.

**Location:** `~/workspace/squad-dashboard/`

**Tech Stack:** React 19 + Vite + TypeScript + Tailwind CSS v4 + Node.js + Express

**Features:**
- Full-stack application with REST API backend
- 4 agent cards (Marcus/Research, Archimedes/Build, Argus/Infra, Galen/Deep Research)
- Real-time auto-refresh every 30 seconds
- Team overview metrics (active agents, activity, efficiency)
- Activity feed with recent actions
- Beautiful dark UI with gradient backgrounds and glow effects
- Expandable agent cards with detailed views
- Pulse animations for active agents
- Hover effects and smooth transitions
- Loading states and error handling
- Agent query service (supports SSH/HTTP/OpenClaw/Mock)

**API Endpoints:**
- `GET /api/health` - Health check
- `GET /api/agents` - All agent status
- `GET /api/agents/:id` - Single agent details
- `GET /api/activities` - Recent activities feed
- `GET /api/overview` - Team metrics summary

**Commands:**
- `npm run dev` — Vite frontend dev server (localhost:5173)
- `npm run server:dev` — Full API + frontend (localhost:3000)
- `npm run build` — Production build
- `npm run start` — Build and run production server
- `./deploy-forge.sh` — Deploy to forge server

**Deployment:**
- Target: `http://100.93.69.117:8080/`
- Script: `deploy-forge.sh` (automated deployment)
- Process Manager: PM2
- Docs: `DEPLOYMENT.md`

**Current Status:** ✅ Production-ready with mock data, deployment infrastructure ready
**Next Steps:** Implement real SSH querying for agent VMs, deploy to forge

## Notes

- Runtime: Linux 6.12.67 (x64) | Node v24.13.0
- Default model: zai/glm-4.7
- Shell: bash
- Current year: 2026

## Projects

### Squad Dashboard Deployment

**Forge Server:** 100.93.69.117:8080

**Agent VMs to Query:**
- marcus-squad — Research agent
- archimedes-squad — Build agent
- argus-squad — Infrastructure agent
- galen-squad — Deep research agent

**Query Methods Available:**
1. **SSH** — Connect via SSH, query agent status
2. **HTTP** — Query agent's HTTP API endpoint
3. **OpenClaw** — Use OpenClaw nodes tool
4. **Mock** — Current default for testing

**Deployment Status:**
- ✅ Backend API implemented
- ✅ Frontend connects to API
- ✅ Auto-refresh working (30s)
- ✅ Deployment script ready
- ⏳ Real SSH querying pending
- ⏳ Forge deployment pending

## Learnings

**Squad Dashboard Build (2026-02-14):**
- Tailwind CSS v4 with `@import "tailwindcss"` syntax is cleaner than v3
- Express with TypeScript is straightforward for REST APIs
- Client-side polling (30s) is simple alternative to WebSocket
- PM2 process manager essential for production Node.js apps
- SSH-based agent querying needs proper error handling and timeouts
- CSS variables with `--agent-color` allow dynamic theming per agent
- Loading states improve perceived performance
- Mock data essential for development before real backend integration

See `~/.openclaw/learnings/` for detailed notes.
