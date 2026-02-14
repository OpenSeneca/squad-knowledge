# Memory

## Tools I've Built

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

### Squad Dashboard (2026-02-14)
Stunning real-time AI squad dashboard for Justin's agent team.

**Location:** `~/workspace/squad-dashboard/`

**Tech Stack:** React 19 + Vite + TypeScript + Tailwind CSS v4

**Features:**
- 4 agent cards (Marcus/Research, Archimedes/Build, Argus/Infra, Galen/Deep Research)
- Real-time status updates (every 15s)
- Team overview metrics
- Activity feed
- Beautiful dark mode UI with animations
- GitHub Pages ready (`npm run deploy`)

**Commands:**
- `npm run dev` — Development server
- `npm run build` — Production build
- `npm run preview` — Preview build
- `npm run deploy` — Deploy to GitHub Pages

**Current Status:** ✅ Built and tested. Ready for GitHub deployment.

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

## Notes

- Runtime: Linux 6.12.67 (x64) | Node v24.13.0
- Default model: zai/glm-4.7
- Shell: bash
- Current year: 2026
