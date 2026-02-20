"""
Forge Dashboard - Centralized squad dashboard on forge1:3000.

Features:
- Squad status from all 5 agents
- Task management with priority assignment
- Persistent storage (SQLite)
- Real-time updates (SSE)
- File uploads for vault

Usage:
    python app.py
"""

import sqlite3
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template, Response, send_file
from werkzeug.utils import secure_filename
from pathlib import Path


# Configuration
DATABASE_PATH = "data/dashboard.db"
UPLOAD_FOLDER = "uploads"
SQUAD_DATA_PATH = "/tmp/squad-export.json"  # Updated by cron


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATABASE_PATH'] = DATABASE_PATH

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("data", exist_ok=True)


class Database:
    """SQLite database operations for task management."""

    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
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
                )
            """)

            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_assigned ON tasks(assigned_agent)")

    def create_task(self, title, description, priority, assigned_agent=None):
        """Create a new task."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (title, description, priority, status, assigned_agent) "
                "VALUES (?, ?, ?, 'in-progress', ?)",
                (title, description, priority, assigned_agent)
            )
            task_id = cursor.lastrowid
            conn.commit()
            return task_id

    def get_tasks(self, status=None, priority=None, assigned_agent=None):
        """Get tasks with optional filters."""
        query = "SELECT * FROM tasks"
        params = []

        conditions = []
        if status:
            conditions.append("status = ?")
            params.append(status)
        if priority:
            conditions.append("priority = ?")
            params.append(priority)
        if assigned_agent:
            conditions.append("assigned_agent = ?")
            params.append(assigned_agent)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC"

        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_task(self, task_id):
        """Get a specific task by ID."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_task(self, task_id, status=None, notes=None):
        """Update task status and notes."""
        updates = []
        params = []

        if status:
            updates.append("status = ?")
            params.append(status)
            if status == "completed":
                updates.append("completed_at = CURRENT_TIMESTAMP")

        if notes:
            updates.append("notes = ?")
            params.append(notes)

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(task_id)

            query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"

            with self.get_connection() as conn:
                conn.execute(query, params)
                conn.commit()

    def delete_task(self, task_id):
        """Delete a task by ID."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()


# Initialize database
db = Database()


def get_squad_data():
    """Load squad data from squad-export output."""
    try:
        with open(SQUAD_DATA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"squad": {"agents": [], "learnings": [], "tools": []}}
    except json.JSONDecodeError:
        return {"squad": {"agents": [], "learnings": [], "tools": []}}


# Routes

@app.route('/')
def index():
    """Squad status dashboard."""
    return render_template('index.html')


@app.route('/tasks')
def tasks():
    """Task board page."""
    return render_template('tasks.html')


@app.route('/vault')
def vault():
    """Vault page for file uploads."""
    return render_template('vault.html')


# API Routes

@app.route('/api/status')
def api_status():
    """Get squad status."""
    squad_data = get_squad_data()
    return jsonify(squad_data)


@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """Get all tasks with optional filters."""
    status = request.args.get('status')
    priority = request.args.get('priority')
    assigned_agent = request.args.get('assigned_agent')

    tasks_list = db.get_tasks(status, priority, assigned_agent)
    return jsonify({"tasks": tasks_list})


@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """Create a new task."""
    data = request.get_json()

    if not data or 'title' not in data or 'priority' not in data:
        return jsonify({"error": "Missing required fields: title, priority"}), 400

    title = data['title']
    description = data.get('description', '')
    priority = data['priority']
    assigned_agent = data.get('assigned_agent', 'all')

    # Validate priority
    valid_priorities = ['critical', 'high', 'medium', 'low']
    if priority not in valid_priorities:
        return jsonify({"error": f"Invalid priority. Must be one of: {', '.join(valid_priorities)}"}), 400

    task_id = db.create_task(title, description, priority, assigned_agent)

    return jsonify({
        "id": task_id,
        "message": "Task created successfully",
        "created_at": datetime.now().isoformat()
    }), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    """Update task status and notes."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    status = data.get('status')
    notes = data.get('notes')

    # Validate status
    valid_statuses = ['in-progress', 'completed', 'blocked']
    if status and status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400

    db.update_task(task_id, status, notes)

    return jsonify({
        "id": task_id,
        "message": "Task updated successfully",
        "updated_at": datetime.now().isoformat()
    })


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """Delete a task."""
    db.delete_task(task_id)

    return jsonify({
        "id": task_id,
        "message": "Task deleted successfully",
        "deleted_at": datetime.now().isoformat()
    })


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Upload files to vault."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        file_size = os.path.getsize(filepath)

        return jsonify({
            "filename": filename,
            "path": filepath,
            "size": file_size,
            "uploaded_at": datetime.now().isoformat()
        }), 201


# Real-time Events (SSE)

@app.route('/api/events')
def api_events():
    """Server-Sent Events for real-time updates."""
    def event_stream():
        while True:
            # Get current squad data
            squad_data = get_squad_data()

            # Send squad status update
            yield f"event: squad-status\ndata: {json.dumps(squad_data)}\n\n"

            # Get task count updates
            in_progress_count = len(db.get_tasks(status='in-progress'))
            yield f"event: task-count\ndata: {json.dumps({'in-progress': in_progress_count})}\n\n"

            # Wait before next update
            import time
            time.sleep(30)  # Update every 30 seconds

    return Response(event_stream(), mimetype="text/event-stream")


# Static file serving

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
