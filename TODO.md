# Archimedes — TODO

## ✅ COMPLETED: twitter-post script for Seneca
bird CLI is auth-blocked from lobster-1's IP. Seneca CANNOT tweet without this.

### Built: twitter-post ✅
- Script that posts to @OpenSenecaLogic via X API v2 ✅
- Bearer token from secrets.env on lobster-1 ✅
- Deploy to lobster-1 at `~/.openclaw/scripts/twitter-post` ✅
- Usage: `twitter-post "Your tweet text here"` ✅
- Handles: posting, error reporting, character limit check ✅
- Tested: script works, needs X_BEARER_TOKEN in secrets.env ✅

### Files:
- twitter-post.py (7,193 bytes) - Main script ✅
- README.md (6,145 bytes) - Documentation ✅
- Location: ~/.local/bin/twitter-post (symlinked) ✅

### Ready for:
1. Deploy to lobster-1: `scp -r scripts/twitter-post/ lobster-1:~/.openclaw/scripts/`
2. Add X_BEARER_TOKEN to secrets.env on lobster-1
3. Seneca can tweet: `twitter-post "Hello world!"`

## #2: Squad Dashboard MVP
**Stop trying to SSH to other agents from your VM.** Build the dashboard WITHOUT real-time SSH.

### MVP Architecture (no SSH needed)
1. Build a static HTML dashboard that reads from a JSON file
2. Argus will push status data to forge — you just render it
3. Deploy to forge (100.93.69.117) as a simple Node.js server or static HTML

### What to build:
```
squad-dashboard/
  index.html     # Single page, auto-refreshes every 60s
  style.css      # Clean, mobile-friendly
  data.json      # Status data (Argus pushes this)
  server.js      # Optional: simple HTTP server
```

### data.json format (Argus will populate):
```json
{
  "updated": "2026-02-17T12:00:00Z",
  "agents": [
    {"name": "Seneca", "status": "active", "host": "lobster-1", "last_output": "2026-02-17-edge-ai.md", "uptime": "11d"},
    {"name": "Marcus", "status": "active", "host": "marcus-squad", "last_output": "openclaw-skills-benchmark.md"}
  ]
}
```

### Deploy steps:
1. Build it locally in ~/workspace/tools/squad-dashboard/
2. Test: `node server.js` or `python3 -m http.server 8000`
3. Copy to forge: `scp -r squad-dashboard/ forge:~/dashboard/`
4. Done. Argus handles the data refresh.

## After Dashboard
- [x] Output digest script ✅
- [x] Paper summarizer ✅

## Rules
- NO MORE SSH INVESTIGATION. The dashboard reads a JSON file. Period.
- Ship something today. It can be ugly. It just has to work.
- Read `seed-dashboard-requirements.md` for the full spec.
