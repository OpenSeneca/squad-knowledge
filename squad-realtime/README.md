# Squad Dashboard

Real-time monitoring dashboard for squad agents (Marcus, Galen, Archimedes, Argus).

## Features

- **Real-time Agent Status**
  - Online/offline status
  - Response time monitoring
  - Error rate tracking
  - Last activity display

- **Activity Feed**
  - Last 10 actions across all agents
  - Agent activities and vault updates
  - Timestamped events

- **Obsidian Vault Integration**
  - Vault sync status
  - Recent file updates
  - Quick links to vault directories

- **Health Metrics**
  - Average response time per agent
  - Success/failure rate
  - Total checks per hour
  - Historical data stored

## Tech Stack

- **Backend:** Node.js + Express + WebSocket
- **Frontend:** React + Tailwind CSS
- **Database:** SQLite (persistent storage)
- **Real-time:** Server-Sent Events (SSE)
- **Monitoring:** SSH connections to squad boxes

## Installation

```bash
# Install backend dependencies
npm install

# Install client dependencies
cd client && npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
```

## Usage

### Development

```bash
# Start backend (auto-reloads)
npm run dev

# Start client (auto-reloads)
cd client && npm start
```

### Production

```bash
# Build client
npm run build

# Start server
npm start
```

## Configuration

### Squad Agents

Edit `server/index.js` to configure agents:

```javascript
const SQUAD_AGENTS = [
  { id: 'marcus', name: 'Marcus', host: '100.98.223.103', user: 'exedev' },
  { id: 'galen', name: 'Galen', host: '100.123.121.125', user: 'exedev' },
  { id: 'archimedes', name: 'Archimedes', host: '100.100.56.102', user: 'exedev' },
  { id: 'argus', name: 'Argus', host: '100.108.219.91', user: 'exedev' },
];
```

### Obsidian Vaults

Edit `server/index.js` to configure vault paths:

```javascript
const VAULT_PATHS = [
  { name: 'Main Vault', path: '/home/exedev/Obsidian/Main' },
  { name: 'Research Vault', path: '/home/exedev/Obsidian/Research' },
  { name: 'Daily Notes', path: '/home/exedev/Obsidian/Daily' },
];
```

## API Endpoints

### GET /api/status
Get all agent statuses and vault status.

**Response:**
```json
{
  "agents": [
    {
      "agentId": "marcus",
      "status": "online",
      "responseTime": 123,
      "activity": "git push",
      "errorRate": 0
    }
  ],
  "vaults": [
    {
      "vaultName": "Main Vault",
      "status": "synced",
      "fileCount": 42,
      "recentFiles": [...]
    }
  ]
}
```

### GET /api/agents/:id
Get detailed status for a specific agent.

### GET /api/activity?limit=10
Get activity feed with optional limit.

### GET /api/vaults
Get all vault statuses.

### GET /api/metrics
Get health metrics for all agents.

### GET /api/events
Server-Sent Events endpoint for real-time updates.

**Events:**
```json
{
  "type": "status",
  "data": [...]
}
```

## Real-time Updates

The dashboard uses Server-Sent Events (SSE) for real-time updates:

1. Connect to `/api/events`
2. Receive `status` events every 30s
3. Receive `vaults` events every 30s
4. UI updates automatically

## Data Storage

### SQLite Database

- **Path:** `server/squad.db`
- **Tables:**
  - `agent_status` - Agent check history
  - `vault_updates` - Vault update history

### Metrics Retention

- Agent status: All history (can be cleaned manually)
- Vault updates: All history (can be cleaned manually)
- Statistics calculated on last hour of data

## Deployment

### Local

```bash
npm start
# Dashboard at: http://localhost:3000
```

### Forge (100.93.69.117)

```bash
# Clone to forge
scp -r squad-realtime exedev@100.93.69.117:/home/exedev/

# SSH to forge
ssh exedev@100.93.69.117

# Install dependencies
cd squad-realtime
npm install
cd client && npm install && cd ..

# Build client
npm run build

# Start server (use PM2 for production)
npm start
# or
pm2 start server/index.js --name squad-dashboard
```

### Using PM2

```bash
# Install PM2
npm install -g pm2

# Start dashboard
pm2 start server/index.js --name squad-dashboard

# Check status
pm2 status

# View logs
pm2 logs squad-dashboard

# Restart
pm2 restart squad-dashboard

# Stop
pm2 stop squad-dashboard
```

## Troubleshooting

### Agent Status Shows "offline"

1. Check SSH access: `ssh exedev@<agent-host>`
2. Verify SSH key: `ls -la ~/.ssh/id_rsa`
3. Check network connectivity to agent box

### Vault Status Shows "error"

1. Check vault path exists: `ls -la <vault-path>`
2. Verify file permissions
3. Check Syncthing sync status

### Dashboard Not Updating

1. Check SSE connection (browser console)
2. Verify server is running: `curl http://localhost:3000/health`
3. Check for network issues

## Features Roadmap

- [ ] Token usage tracking (requires OpenClaw API)
- [ ] Disk space monitoring
- [ ] Historical metrics charts
- [ ] Custom alerts (email/webhook)
- [ ] Agent comparison view
- [ ] Export activity logs
- [ ] Mobile responsive design

## License

MIT License
