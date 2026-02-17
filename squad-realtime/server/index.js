const express = require('express');
const WebSocket = require('ws');
const { SSH } = require('node-ssh-client');
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

// Squad configuration
const SQUAD_AGENTS = [
  { id: 'marcus', name: 'Marcus', host: '100.98.223.103', user: 'exedev' },
  { id: 'galen', name: 'Galen', host: '100.123.121.125', user: 'exedev' },
  { id: 'archimedes', name: 'Archimedes', host: '100.100.56.102', user: 'exedev' },
  { id: 'argus', name: 'Argus', host: '100.108.219.91', user: 'exedev' },
];

// Obsidian vault paths
const VAULT_PATHS = [
  { name: 'Main Vault', path: '/home/exedev/Obsidian/Main' },
  { name: 'Research Vault', path: '/home/exedev/Obsidian/Research' },
  { name: 'Daily Notes', path: '/home/exedev/Obsidian/Daily' },
];

// Database setup
const dbPath = path.join(__dirname, 'squad.db');
const db = new Database(dbPath);

// Initialize database
db.prepare(`
  CREATE TABLE IF NOT EXISTS agent_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    status TEXT NOT NULL,
    response_time INTEGER,
    activity TEXT,
    timestamp INTEGER NOT NULL,
    error_rate REAL
  )
`).run();

db.prepare(`
  CREATE TABLE IF NOT EXISTS vault_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vault_name TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    timestamp INTEGER NOT NULL
  )
`).run();

// Express setup
const app = express();
const PORT = 3000;

// Serve static files
app.use(express.static(path.join(__dirname, 'client/build')));

app.use(express.json());

// SSE clients
const clients = new Set();

// Broadcast function
function broadcast(data) {
  clients.forEach(client => {
    try {
      client.send(JSON.stringify(data));
    } catch (error) {
      console.error('Error sending to client:', error);
      clients.delete(client);
    }
  });
}

// SSH check function
async function checkAgent(agent) {
  const startTime = Date.now();

  try {
    const ssh = new SSH();
    await ssh.connect({
      host: agent.host,
      username: agent.user,
      privateKey: fs.readFileSync('/home/exedev/.ssh/id_rsa'),
    });

    // Get uptime and last command
    const uptime = await ssh.execCommand('uptime');
    const lastCommand = await ssh.execCommand('tail -1 ~/.bash_history');

    await ssh.disconnect();

    const responseTime = Date.now() - startTime;

    // Store in database
    const statement = db.prepare(`
      INSERT INTO agent_status (agent_id, status, response_time, activity, timestamp, error_rate)
      VALUES (?, ?, ?, ?, ?, ?)
    `);

    statement.run(
      agent.id,
      'online',
      responseTime,
      lastCommand.stdout.trim(),
      Date.now(),
      0
    );

    return {
      agentId: agent.id,
      status: 'online',
      responseTime,
      activity: lastCommand.stdout.trim(),
      errorRate: 0,
    };
  } catch (error) {
    const responseTime = Date.now() - startTime;

    // Get recent error rate from database
    const recentErrors = db.prepare(`
      SELECT COUNT(*) as errors FROM agent_status
      WHERE agent_id = ? AND status = 'offline' AND timestamp > ?
    `).get(agent.id, Date.now() - 3600000);

    const errorRate = recentErrors.errors / 120; // 120 checks per hour

    const statement = db.prepare(`
      INSERT INTO agent_status (agent_id, status, response_time, activity, timestamp, error_rate)
      VALUES (?, ?, ?, ?, ?, ?)
    `);

    statement.run(
      agent.id,
      'offline',
      responseTime,
      `Connection failed: ${error.message}`,
      Date.now(),
      errorRate
    );

    return {
      agentId: agent.id,
      status: 'offline',
      responseTime,
      activity: `Connection failed`,
      errorRate,
    };
  }
}

// Check vault status
function checkVault(vaultPath) {
  try {
    const files = fs.readdirSync(vaultPath.vaultPath);
    const mdFiles = files.filter(f => f.endsWith('.md'));

    // Get recent files
    const recentFiles = mdFiles
      .map(file => ({
        name: file,
        path: path.join(vaultPath.vaultPath, file),
        mtime: fs.statSync(path.join(vaultPath.vaultPath, file)).mtime.getTime(),
      }))
      .sort((a, b) => b.mtime - a.mtime)
      .slice(0, 10);

    // Store recent updates in database
    recentFiles.forEach(file => {
      const statement = db.prepare(`
        INSERT INTO vault_updates (vault_name, file_name, file_type, timestamp)
        VALUES (?, ?, ?, ?)
      `);

      statement.run(
        vaultPath.name,
        file.name,
        file.mtime > Date.now() - 86400000 ? 'recent' : 'old',
        file.mtime
      );
    });

    return {
      vaultName: vaultPath.name,
      status: 'synced',
      fileCount: mdFiles.length,
      recentFiles: recentFiles.map(f => ({
        name: f.name,
        timestamp: f.mtime,
      })),
    };
  } catch (error) {
    return {
      vaultName: vaultPath.name,
      status: 'error',
      error: error.message,
      fileCount: 0,
      recentFiles: [],
    };
  }
}

// Get activity feed
function getActivityFeed(limit = 10) {
  const feed = db.prepare(`
    SELECT 'agent' as source, agent_id as source_id, activity as message, timestamp
    FROM agent_status
    UNION ALL
    SELECT 'vault' as source, vault_name as source_id, file_name as message, timestamp
    FROM vault_updates
    ORDER BY timestamp DESC
    LIMIT ?
  `).all(limit);

  return feed.map(item => ({
    ...item,
    agentName: SQUAD_AGENTS.find(a => a.id === item.source_id)?.name || item.source_id,
  }));
}

// Get metrics
function getMetrics(agentId) {
  const metrics = db.prepare(`
    SELECT
      AVG(response_time) as avgResponseTime,
      AVG(error_rate) as avgErrorRate,
      COUNT(*) as totalChecks
    FROM agent_status
    WHERE agent_id = ? AND timestamp > ?
  `).get(agentId, Date.now() - 3600000);

  return {
    agentId,
    avgResponseTime: metrics.avgResponseTime || 0,
    avgErrorRate: metrics.avgErrorRate || 0,
    totalChecks: metrics.totalChecks || 0,
  };
}

// API routes
app.get('/api/status', async (req, res) => {
  const statusPromises = SQUAD_AGENTS.map(checkAgent);
  const statuses = await Promise.all(statusPromises);

  res.json({
    agents: statuses,
    vaults: VAULT_PATHS.map(checkVault),
  });
});

app.get('/api/agents/:id', async (req, res) => {
  const agent = SQUAD_AGENTS.find(a => a.id === req.params.id);
  if (!agent) {
    return res.status(404).json({ error: 'Agent not found' });
  }

  const status = await checkAgent(agent);
  const metrics = getMetrics(agent.id);

  res.json({ ...status, metrics });
});

app.get('/api/activity', (req, res) => {
  const limit = parseInt(req.query.limit) || 10;
  const feed = getActivityFeed(limit);

  res.json(feed);
});

app.get('/api/vaults', (req, res) => {
  const vaults = VAULT_PATHS.map(checkVault);
  res.json(vaults);
});

app.get('/api/metrics', (req, res) => {
  const metrics = SQUAD_AGENTS.map(agent => ({
    ...getMetrics(agent.id),
    name: agent.name,
  }));

  res.json(metrics);
});

// SSE endpoint
app.get('/api/events', (req, res) => {
  const headers = {
    'Content-Type': 'text/event-stream',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
  };

  res.writeHead(200, headers);

  // Send initial data
  const statusPromises = SQUAD_AGENTS.map(checkAgent);
  const statuses = await Promise.all(statusPromises);

  res.write(`data: ${JSON.stringify({ type: 'status', data: statuses })}\n\n`);
  res.write(`data: ${JSON.stringify({ type: 'vaults', data: VAULT_PATHS.map(checkVault) })}\n\n`);

  // Add client
  clients.push(res);

  // Remove client on disconnect
  req.on('close', () => {
    clients.delete(res);
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: Date.now() });
});

// Start server
const server = app.listen(PORT, () => {
  console.log(`Squad Dashboard running on http://localhost:${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});

// Periodic checks (every 30 seconds)
setInterval(async () => {
  console.log('Running periodic checks...');

  const statusPromises = SQUAD_AGENTS.map(checkAgent);
  const statuses = await Promise.all(statusPromises);

  broadcast({ type: 'status', data: statuses });

  // Check vaults
  const vaults = VAULT_PATHS.map(checkVault);
  broadcast({ type: 'vaults', data: vaults });

}, 30000);

module.exports = app;
