# Squad Dashboard - Production-Ready Monitoring

Production-ready dashboard for monitoring all 4 squad agents (marcus, archimedes, argus, galen) with status, last output, uptime, and activity tracking.

## Features

- **Multi-Agent Monitoring** - Monitors all 4 squad agents
- **Auto-Updates** - Refreshes every 5 minutes automatically
- **Production-Ready** - Error handling, logging, graceful shutdown
- **Systemd Service** - Auto-restart on failure
- **Web UI** - Clean, responsive interface
- **REST API** - Programmatic access to agent data
- **Squad-Output Integration** - Uses synced data from `~/.openclaw/squad-output/`

## Architecture

```
Squad-Output Base: ~/.openclaw/squad-output/
├── marcus/
│   ├── learnings/
│   ├── memory/
│   └── workspace/
├── archimedes/
│   ├── learnings/
│   ├── memory/
│   └── workspace/
├── argus/
│   ├── learnings/
│   ├── memory/
│   └── workspace/
└── galen/
    ├── learnings/
    ├── memory/
    └── workspace/
```

## Quick Start

### Development
```bash
cd /home/exedev/.openclaw/workspace/tools/squad-dashboard-prod
npm install
npm start
```
Dashboard available at: http://localhost:3000

### Production Deployment (Forge - 100.93.69.117)

**Prerequisites:**
- SSH access to forge (100.93.69.117)
- Node.js 16+ installed
- Systemd available

**Deployment Steps:**

1. **Copy dashboard to forge:**
```bash
ssh exedev@forge
cd /home/exedev/.openclaw/workspace/tools/
rsync -avz ./squad-dashboard-prod/ forge:/home/exedev/.openclaw/workspace/tools/
```

2. **Create log directories:**
```bash
ssh exedev@forge
sudo mkdir -p /var/log/squad-dashboard
sudo chown exedev:exedev /var/log/squad-dashboard
sudo chmod 755 /var/log/squad-dashboard
```

3. **Install dependencies:**
```bash
ssh exedev@forge
cd /home/exedev/.openclaw/workspace/tools/squad-dashboard-prod
npm install --production
```

4. **Create systemd service:**
```bash
ssh exedev@forge
sudo cp squad-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable squad-dashboard
sudo systemctl start squad-dashboard
```

5. **Verify deployment:**
```bash
ssh exedev@forge
sudo systemctl status squad-dashboard
curl http://localhost:3000/api/health
```

## API Endpoints

### Health Check
```bash
curl http://localhost:3000/api/health
```

Response:
```json
{
  "status": "healthy",
  "server": "squad-dashboard-prod",
  "version": "1.0.0",
  "uptime": "1h 23m",
  "lastUpdate": "2026-02-23T09:00:00.000Z",
  "agentsCount": 4
}
```

### Full Status
```bash
curl http://localhost:3000/api/status
```

Response:
```json
{
  "updated": "2026-02-23T09:00:00.000Z",
  "agents": [
    {
      "name": "marcus",
      "status": "active",
      "lastOutput": "Last 5 lines of output...",
      "lastUpdate": "2026-02-23T08:55:00.000Z",
      "uptime": "2.1 hours ago",
      "activity": [...]
    },
    ...
  ]
}
```

### Individual Agent
```bash
curl http://localhost:3000/api/agent/marcus
```

## Monitoring

### Systemd Service Status
```bash
# Check status
sudo systemctl status squad-dashboard

# View logs
sudo journalctl -u squad-dashboard -f

# Restart
sudo systemctl restart squad-dashboard

# Stop
sudo systemctl stop squad-dashboard
```

### Application Logs
```bash
# Access log
tail -f /var/log/squad-dashboard/access.log

# Error log
tail -f /var/log/squad-dashboard/error.log
```

## Configuration

### Environment Variables
- `PORT` - HTTP port (default: 3000)
- `NODE_ENV` - Environment (production/development)

### Update Interval
- Default: 5 minutes
- To change: Modify `UPDATE_INTERVAL` in `server.js`

### Squad Output Base
- Default: `/home/exedev/.openclaw/squad-output/`
- To change: Modify `SQUAD_OUTPUT_BASE` in `server.js`

## Troubleshooting

### Dashboard Not Starting

1. **Check systemd status:**
```bash
sudo systemctl status squad-dashboard
```

2. **Check logs:**
```bash
sudo journalctl -u squad-dashboard -n 50
```

3. **Verify Node.js:**
```bash
node --version  # Should be 16+
```

### Agent Data Not Loading

1. **Check squad-output directory:**
```bash
ls -la ~/.openclaw/squad-output/
ls -la ~/.openclaw/squad-output/marcus/learnings/
```

2. **Verify permissions:**
```bash
ls -ld ~/.openclaw/squad-output/
```

### Port Already in Use

1. **Find process:**
```bash
sudo lsof -i :3000
```

2. **Kill process:**
```bash
sudo kill -9 <PID>
```

## Production Best Practices

1. **Auto-Restart:** Configured in systemd (`Restart=on-failure`)
2. **Error Logging:** Separate error log for debugging
3. **Graceful Shutdown:** Handles SIGTERM and SIGINT
4. **Access Control:** Firewall rules to allow port 3000
5. **Monitoring:** Use systemd status and logs for health checks

## Deployment Script (Automated)

Save this as `deploy-to-forge.sh`:

```bash
#!/bin/bash
set -e

FORGE_HOST="exedev@100.93.69.117"
DASHBOARD_DIR="/home/exedev/.openclaw/workspace/tools/squad-dashboard-prod"
LOG_DIR="/var/log/squad-dashboard"

echo "Deploying squad-dashboard to forge..."

# Copy dashboard
echo "Copying dashboard files..."
rsync -avz ./ ${FORGE_HOST}:${DASHBOARD_DIR}/

# Create log directories
echo "Creating log directories..."
ssh ${FORGE_HOST} "sudo mkdir -p ${LOG_DIR}"
ssh ${FORGE_HOST} "sudo chown exedev:exedev ${LOG_DIR}"
ssh ${FORGE_HOST} "sudo chmod 755 ${LOG_DIR}"

# Install dependencies
echo "Installing dependencies..."
ssh ${FORGE_HOST} "cd ${DASHBOARD_DIR} && npm install --production"

# Deploy systemd service
echo "Deploying systemd service..."
scp squad-dashboard.service ${FORGE_HOST}:/tmp/
ssh ${FORGE_HOST} "sudo cp /tmp/squad-dashboard.service /etc/systemd/system/"
ssh ${FORGE_HOST} "sudo systemctl daemon-reload"

# Enable and start service
echo "Enabling and starting service..."
ssh ${FORGE_HOST} "sudo systemctl enable squad-dashboard"
ssh ${FORGE_HOST} "sudo systemctl start squad-dashboard"

# Verify
echo "Verifying deployment..."
ssh ${FORGE_HOST} "sudo systemctl status squad-dashboard"
ssh ${FORGE_HOST} "curl -s http://localhost:3000/api/health"

echo "Deployment complete!"
echo "Dashboard available at: http://forge:3000"
```

Usage:
```bash
chmod +x deploy-to-forge.sh
./deploy-to-forge.sh
```

## License

MIT

## Author

Archimedes - OpenSeneca squad

---

**Production-ready dashboard for squad monitoring!**
