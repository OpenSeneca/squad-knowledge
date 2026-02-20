# Forge Dashboard

Centralized squad dashboard on forge1:3000 - Single place for Justin to check squad status, assign tasks, and manage files.

## Features

- **Squad Status** - Real-time view of all 5 agents (status, uptime, activity)
- **Task Management** - Create, update, delete tasks with priority assignment
- **Priority Levels** - Critical, High, Medium, Low
- **Task Tracking** - In-progress, Completed, Blocked states
- **Persistent Storage** - SQLite database survives agent restarts
- **Real-time Updates** - Server-Sent Events (SSE) or polling fallback
- **File Uploads** - Vault for storing notes and documents
- **Responsive Design** - Works on mobile + desktop

## Tech Stack

**Backend:**
- Flask 3.0 (Python web framework)
- SQLite (persistent database, no external deps)
- Server-Sent Events (SSE) for real-time updates

**Frontend:**
- HTML5 + Vanilla JavaScript (no build required)
- CSS3 with CSS variables for theming
- Responsive design (mobile + desktop)

**Data:**
- Squad data: squad-export CLI output (JSON)
- Tasks: SQLite database (persistent storage)
- Files: Local filesystem (uploads directory)

## Quick Start

### Local Development

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Run the server:**
```bash
python app.py
```

**3. Access dashboard:**
- Squad Status: http://localhost:3000
- Task Board: http://localhost:3000/tasks
- Vault: http://localhost:3000/vault

### Deployment to forge1:3000

**1. Copy files to forge1:**
```bash
rsync -avz forge-dashboard/ forge1:~/forge-dashboard/
```

**2. Install dependencies on forge1:**
```bash
ssh forge1 "cd forge-dashboard && pip install -r requirements.txt"
```

**3. Start the server:**
```bash
ssh forge1 "cd forge-dashboard && nohup python app.py > server.log 2>&1 &"
```

**4. Access from external network:**
- http://forge1:3000

**5. Set up cron for squad-export:**
```bash
# Add to crontab for squad-data updates
# Update every 5 minutes
*/5 * * * * squad-export --include-learnings > /tmp/squad-export.json

# Or add to forge1's crontab
ssh forge1 "crontab -l | grep -v 'squad-export' | {cat; echo '*/5 * * * * squad-export --include-learnings > /tmp/squad-export.json'; } | crontab -"
```

## API Endpoints

### Squad Status

**GET /api/status**
- Returns squad data (agents, learnings, tools)
- Data source: squad-export CLI output
- Response: { "timestamp": "...", "squad": { "agents": [...], "learnings": [...], "tools": [...] } }

### Task Management

**POST /api/tasks** - Create task
- Body: { "title": "...", "description": "...", "priority": "...", "assigned_agent": "..." }
- Priority: critical, high, medium, low
- Assigned agent: all, archimedes, marcus, galen, argus, seneca
- Response: { "id": 1, "message": "Task created successfully" }

**GET /api/tasks** - List tasks
- Query params: status, priority, assigned_agent
- Response: { "tasks": [...] }

**PUT /api/tasks/:id** - Update task
- Body: { "status": "...", "notes": "..." }
- Status: in-progress, completed, blocked
- Response: { "id": 1, "message": "Task updated successfully" }

**DELETE /api/tasks/:id** - Delete task
- Response: { "id": 1, "message": "Task deleted successfully" }

### File Uploads

**POST /api/upload** - Upload file to vault
- Multipart form data
- Response: { "filename": "...", "path": "...", "size": 12345, "uploaded_at": "..." }

### Real-time Updates

**GET /api/events** - Server-Sent Events
- Stream of real-time updates
- Event types: squad-status, task-count
- Fallback: Polling every 30 seconds

## Database Schema

**Tasks Table:**
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    assigned_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    notes TEXT
);
```

**Indexes:**
- CREATE INDEX idx_tasks_status ON tasks(status);
- CREATE INDEX idx_tasks_priority ON tasks(priority);
- CREATE INDEX idx_tasks_assigned ON tasks(assigned_agent);

## File Structure

```
forge-dashboard/
├── app.py                    # Flask application
├── requirements.txt            # Python dependencies
├── static/
│   ├── css/
│   │   └── dashboard.css  # Styles
│   └── js/
│       └── dashboard.js   # Frontend logic
├── templates/
│   ├── index.html           # Squad status page
│   ├── tasks.html          # Task board page
│   └── vault.html          # Vault page
├── data/
│   └── dashboard.db         # SQLite database
├── uploads/                   # Uploaded files directory
└── README.md                 # This file
```

## Priority Levels

| Priority | Description | Use Case |
|----------|-------------|-----------|
| **Critical** | 🔴 Urgent, blockers | "Fix server down", "Fix broken dashboard" |
| **High** | 🟠 Important, high impact | "Deploy dashboard to forge1", "Build squad-export" |
| **Medium** | 🟡 Normal tasks | "Update documentation", "Fix minor bug" |
| **Low** | 🟢 Nice to have | "Research new tool", "Improve UI" |

## Task States

| State | Description | Use Case |
|-------|-------------|-----------|
| **In-progress** | 🔄 Currently being worked on | "Building forge dashboard", "Researching AionUi" |
| **Completed** | ✅ Finished | "Squad-export tool built", "GitHub repos published" |
| **Blocked** | 🚫 Waiting for something | "Waiting for SSH access", "Waiting for API key" |

## Usage Examples

### Create a Critical Task

1. Go to http://localhost:3000/tasks
2. Fill in form:
   - Title: "Deploy dashboard to forge1"
   - Description: "SSH access is blocked, need to resolve"
   - Priority: Critical
   - Assigned To: Archimedes
3. Click "Create Task"

### View Squad Status

1. Go to http://localhost:3000
2. See:
   - Agent status table (ID, name, role, status, uptime, activity)
   - Recent learnings from all agents
   - Tools inventory

### Upload a File

1. Go to http://localhost:3000/vault
2. Click "Choose File"
3. Select file and click "Upload"

## Development

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Access at http://localhost:3000
```

### Testing

```bash
# Test API endpoints
curl http://localhost:3000/api/status

# Test task creation
curl -X POST http://localhost:3000/api/tasks \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Test task", "priority": "high"}'

# Test SSE
curl -N http://localhost:3000/api/events
```

## Deployment

### Automated Deployment Script

```bash
#!/bin/bash
# deploy.sh - Deploy to forge1:3000

FORGE_HOST="forge1"
APP_DIR="forge-dashboard"
REMOTE_DIR="~/forge-dashboard"

# Copy files to forge1
echo "Copying files to ${FORGE_HOST}..."
rsync -avz --exclude '*.pyc' --exclude '__pycache__' \\
  ${APP_DIR}/ ${FORGE_HOST}:${REMOTE_DIR}/

# Install dependencies
echo "Installing dependencies on ${FORGE_HOST}..."
ssh ${FORGE_HOST} "cd ${REMOTE_DIR} && pip install -r requirements.txt"

# Start server (stop existing first)
echo "Starting server on ${FORGE_HOST}..."
ssh ${FORGE_HOST} "cd ${REMOTE_DIR} && pkill -f 'python app.py' || true"
ssh ${FORGE_HOST} "cd ${REMOTE_DIR} && nohup python app.py > server.log 2>&1 &"

echo "Deployment complete!"
echo "Access at: http://${FORGE_HOST}:3000"
echo "Server logs: ssh ${FORGE_HOST} 'tail -f ${REMOTE_DIR}/server.log'"
```

### Manual Deployment Steps

1. **Copy application:**
```bash
scp -r forge-dashboard/ forge1:~/
```

2. **SSH to forge1:**
```bash
ssh forge1
cd forge-dashboard
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize database:**
```bash
python -c "from app import db; print('Database initialized')"
```

5. **Start server:**
```bash
# Run in foreground for testing
python app.py

# Run in background for production
nohup python app.py > server.log 2>&1 &
```

6. **Set up cron for squad data:**
```bash
# Edit crontab
crontab -e

# Add line for squad-export updates
*/5 * * * * /home/exedev/.local/bin/squad-export --include-learnings > /tmp/squad-export.json
```

## Real-time Updates

### Server-Sent Events (SSE)

**Client-side:**
```javascript
const eventSource = new EventSource('/api/events');

eventSource.addEventListener('squad-status', (event) => {
    const data = JSON.parse(event.data);
    // Update UI with squad status
    updateSquadStatus(data);
});

eventSource.addEventListener('task-count', (event) => {
    const data = JSON.parse(event.data);
    // Update task count badge
    updateTaskCount(data['in-progress']);
});
```

**Polling Fallback:**

If SSE fails, dashboard automatically falls back to polling every 30 seconds.

## Security

- **SQL Injection Protection:** Parameterized queries in SQLite
- **XSS Protection:** Proper escaping in templates
- **File Upload Validation:** Filename sanitization with `secure_filename()`
- **CSRF Protection:** Future enhancement (token-based validation)

## Troubleshooting

**Issue: Can't access forge1:3000**
- Check if server is running: `ssh forge1 "ps aux | grep 'python app.py'"`
- Check logs: `ssh forge1 "tail -f forge-dashboard/server.log"`
- Check firewall: Ensure port 3000 is open

**Issue: Squad data not loading**
- Check squad-export: Run `squad-export --include-learnings > /tmp/squad-export.json`
- Check file permissions: Ensure `/tmp/squad-export.json` is readable
- Check cron: Ensure squad-export runs periodically

**Issue: Tasks not saving**
- Check database: `sqlite3 data/dashboard.db "SELECT * FROM tasks"`
- Check permissions: Ensure `data/` directory is writable
- Restart server: `python app.py`

## Future Enhancements

- [ ] User authentication (login for Justin, squad members)
- [ ] Task comments/discussion
- [ ] Task assignment notifications
- [ ] Email notifications for high-priority tasks
- [ ] Task templates (common tasks)
- [ ] Task due dates
- [ ] Search and filtering improvements
- [ ] Export tasks to CSV/JSON
- [ ] Backup and restore database

## Success Metrics

**Before Deployment:**
- [x] Squad status API returns correct data
- [x] Task API creates, updates, deletes tasks
- [x] Frontend displays squad status correctly
- [x] Frontend displays task board correctly
- [x] Priority assignment form works
- [x] Real-time updates work (SSE or polling)
- [ ] File uploads work (needs testing)

**After Deployment:**
- [ ] Accessible at http://forge1:3000
- [ ] Squad status loads with current state of all 5 agents
- [ ] Priority assignment form working
- [ ] Task list shows active/completed/blocked
- [ ] Data persists even if agents go offline
- [ ] Accessible from external network

## License

MIT

---

**Application:** Forge Dashboard
**Version:** 1.0
**Author:** Archimedes (OpenSeneca squad)
**Date:** 2026-02-20
