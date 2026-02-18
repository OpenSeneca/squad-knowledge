# Squad Dashboard — OpenSeneca Squad Monitoring

A simple, static dashboard for monitoring OpenSeneca squad agents.

## What It Does

- **Agent Status Cards** — Name, role, status, host, uptime, last output
- **Team Overview** — Total agents, active count, average activity
- **Activity Feed** — Recent updates from all agents
- **Auto-Refresh** — Updates every 60 seconds without page reload
- **Mobile-Friendly** — Responsive design for checking from phone

## Architecture

**No SSH Required.** The dashboard reads from `data.json` file. Argus (or another agent) is responsible for pushing status data to this file.

```
┌─────────────┐
│   Browser   │ ← Auto-refreshes every 60s via fetch()
│  /api/status │
└─────────────┘
       ↓
   data.json (static file)
       ↑
  Argus/Agent (writes updates via SSH/SCP)
```

## Installation

```bash
# Clone or copy to workspace
cd ~/workspace/tools/squad-dashboard/

# Make server executable
chmod +x server.js

# Test locally
node server.js
# Dashboard at: http://localhost:8000
# API endpoint: http://localhost:8000/api/status
```

## Usage

### Start Server

```bash
node server.js
```

The dashboard will be available at `http://localhost:8000`

### Update Agent Status

The `data.json` file is updated by:
- **Argus** (Ops agent) — Runs queries to all squad agents
- **Manual update** — SSH to agents and update data.json

**Example data.json:**

```json
{
  "updated": "2026-02-17T14:18:00Z",
  "agents": [
    {
      "name": "Seneca",
      "role": "Coordinator",
      "status": "active",
      "host": "lobster-1",
      "ip": "100.101.15.68",
      "last_output": "tinyseed-accelerator-analysis.md",
      "last_updated": "2026-02-17T14:18:00Z",
      "uptime": "11d",
      "activity": 85
    },
    {
      "name": "Marcus",
      "role": "Research",
      "status": "active",
      "host": "marcus-squad",
      "ip": "100.98.223.103",
      "last_output": "2026-02-16-summary.md",
      "last_updated": "2026-02-16T23:59:00Z",
      "uptime": "0d",
      "activity": 78
    }
  ]
}
```

### Data Update Flow

**Argus (Ops Agent) responsibilities:**

1. **Query agents every 5 minutes** via SSH/commands:
   ```bash
   ssh marcus-squad 'ls -t ~/.openclaw/learnings/ | head -1'
   ssh galen-squad 'ls -t ~/.openclaw/learnings/ | head -1'
   ssh archimedes-squad 'ls -t ~/.openclaw/learnings/ | head -1'
   ```

2. **Update data.json:**
   ```bash
   scp data.json forge:~/dashboard/data.json
   ```

3. **Or write directly:**
   ```bash
   ssh forge 'cat > ~/dashboard/data.json << EOF
   { ... updated JSON ... }
   EOF
   ```

## Deployment to Forge

### Using the Deployment Script (Recommended)

```bash
# From the squad-dashboard directory
cd ~/workspace/tools/squad-dashboard/

# Run deployment script
./deploy-forge.sh

# Or with custom settings
./deploy-forge.sh --host 100.93.69.117 --user exedev --dir ~/dashboard --port 8000
```

The deployment script will:
- ✓ Check SSH connectivity to forge
- ✓ Copy all files to the remote directory
- ✓ Install PM2 if not present
- ✓ Start/restart the dashboard service
- ✓ Display service status and URL
- ✓ Optionally set up auto-start on boot

### Manual Deployment

```bash
# Copy to forge
scp -r squad-dashboard/ exedev@100.93.69.117:~/dashboard/

# SSH to forge
ssh exedev@100.93.69.117

# Navigate to dashboard
cd ~/dashboard

# Test locally
node server.js

# Run in background with PM2
pm2 start server.js --name squad-dashboard

# Set to auto-start on boot
pm2 save
pm2 startup

# Check logs
pm2 logs squad-dashboard
```

Access at: **http://100.93.69.117:8000** (or forge:8000 on Tailscale)

## Features

- ✅ Single-page dashboard (no build step)
- ✅ Auto-refresh every 60 seconds
- ✅ Mobile-friendly responsive design
- ✅ Color-coded status (green/yellow/red)
- ✅ Team overview metrics
- ✅ Activity feed with timestamps
- ✅ Simple Node.js HTTP server
- ✅ No SSH required from dashboard

## Status Colors

- **Green (#10b981)**: Active in last 2 hours
- **Yellow (#f59e0b)**: Active 2-6 hours ago
- **Red (#ef4444)**: Active 6+ hours ago or down

## Tech Stack

- **Frontend**: Vanilla HTML + CSS + JavaScript
- **Backend**: Node.js HTTP server
- **Data**: Static JSON file (data.json)
- **Refresh**: Client-side fetch() every 60s

## API Endpoint

### GET /api/status

Returns current agent status from data.json.

**Response:**
```json
{
  "updated": "2026-02-17T14:18:00Z",
  "agents": [...]
}
```

## Troubleshooting

### Server Won't Start

```bash
# Check port availability
lsof -i :8000

# Kill process using port
kill -9 <PID>

# Try different port
PORT=9000 node server.js
```

### Data Not Loading

```bash
# Check data.json exists
ls -la data.json

# Validate JSON syntax
cat data.json | python3 -m json.tool

# Check file permissions
chmod 644 data.json
```

### Auto-Refresh Not Working

Check browser console:
- Open DevTools (F12)
- Check Network tab for failed /api/status requests
- Check Console for JavaScript errors

### Access from Other Devices

```bash
# Ensure firewall allows port 8000
sudo ufw allow 8000/tcp

# Check Node.js is accessible
curl http://100.93.69.117:8000
```

## Production Deployment with PM2

```bash
# Install PM2
npm install -g pm2

# Start dashboard
pm2 start server.js --name squad-dashboard

# Check status
pm2 status

# View logs
pm2 logs squad-dashboard

# Restart
pm2 restart squad-dashboard

# Stop
pm2 stop squad-dashboard

# Remove
pm2 delete squad-dashboard
```

## Future Enhancements

- [ ] Add authentication (optional, Tailscale-only access)
- [ ] Real-time WebSocket updates (SSE)
- [ ] Historical activity charts
- [ ] Agent-specific pages (detailed metrics)
- [ ] Configuration UI (add/remove agents)
- [ ] Alert notifications (email/webhook)

## Files

- `index.html` — Main dashboard page
- `style.css` — Responsive styles (dark theme)
- `server.js` — Simple HTTP server
- `data.json` — Agent status data (updated by Argus)
- `README.md` — This file

## License

MIT License

---

**Simple. Fast. Works.**

No SSH connection issues. No complex infrastructure. Just a dashboard that reads a JSON file.
