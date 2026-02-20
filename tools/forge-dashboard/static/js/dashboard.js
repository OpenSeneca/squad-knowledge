// Forge Dashboard JavaScript

// Configuration
const API_BASE = '/api';
const SSE_EVENTS = '/api/events';

// State
let squadData = null;
let tasks = [];
let sseSource = null;

// DOM Elements
function initDOM() {
    // Will be populated by page-specific init functions
}

// API Calls
async function fetchSquadStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        squadData = data;
        return data;
    } catch (error) {
        console.error('Error fetching squad status:', error);
        return null;
    }
}

async function fetchTasks(filters = {}) {
    const params = new URLSearchParams();

    if (filters.status) params.append('status', filters.status);
    if (filters.priority) params.append('priority', filters.priority);
    if (filters.assignedAgent) params.append('assigned_agent', filters.assignedAgent);

    try {
        const response = await fetch(`${API_BASE}/tasks?${params.toString()}`);
        const data = await response.json();
        tasks = data.tasks;
        return data.tasks;
    } catch (error) {
        console.error('Error fetching tasks:', error);
        return [];
    }
}

async function createTask(taskData) {
    try {
        const response = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create task');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error creating task:', error);
        throw error;
    }
}

async function updateTask(taskId, updates) {
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updates)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to update task');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error updating task:', error);
        throw error;
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to delete task');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error deleting task:', error);
        throw error;
    }
}

// Real-time Updates
function initSSE() {
    if (sseSource) {
        sseSource.close();
    }

    try {
        sseSource = new EventSource(SSE_EVENTS);

        sseSource.onopen = () => {
            console.log('SSE connection opened');
        };

        sseSource.onerror = (error) => {
            console.error('SSE error:', error);
            // Fallback to polling
            initPolling();
        };

        sseSource.addEventListener('squad-status', (event) => {
            const data = JSON.parse(event.data);
            squadData = data;
            onSquadStatusUpdate(data);
        });

        sseSource.addEventListener('task-count', (event) => {
            const data = JSON.parse(event.data);
            onTaskCountUpdate(data);
        });

    } catch (error) {
        console.error('Error initializing SSE:', error);
        // Fallback to polling
        initPolling();
    }
}

function initPolling() {
    console.log('Falling back to polling mode');
    setInterval(async () => {
        await fetchSquadStatus();
        await fetchTasks();
        if (squadData) onSquadStatusUpdate(squadData);
        onTaskCountUpdate({ 'in-progress': tasks.filter(t => t.status === 'in-progress').length });
    }, 30000); // Poll every 30 seconds
}

// UI Rendering Functions
function renderAgentStatusTable(agents) {
    if (!agents || agents.length === 0) {
        return '<p class="text-center">No agent data available</p>';
    }

    const rows = agents.map(agent => {
        const statusEmoji = agent.status === 'active' ? '🟢' : '🔴';
        const statusClass = agent.status === 'active' ? 'status-active' : 'status-inactive';

        return `
            <tr>
                <td>${agent.id}</td>
                <td>${agent.name}</td>
                <td>${agent.role}</td>
                <td><span class="${statusClass}">${statusEmoji} ${agent.status}</span></td>
                <td>${agent.uptime_hours?.toFixed(1) || 'N/A'}h</td>
                <td>${agent.activity_score || 0}</td>
                <td>${agent.last_output || 'N/A'}</td>
            </tr>
        `;
    }).join('');

    return `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Uptime</th>
                    <th>Activity</th>
                    <th>Last Output</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>
    `;
}

function renderTaskCard(task) {
    const priorityClass = `priority-${task.priority}`;
    const statusClass = `status-badge status-${task.status}`;

    const assignedBadge = task.assigned_agent && task.assigned_agent !== 'all'
        ? `<span class="badge badge-secondary">👤 ${task.assigned_agent}</span>`
        : '<span class="badge badge-secondary">👥 All</span>';

    const updatedAt = task.updated_at ? new Date(task.updated_at).toLocaleString() : 'N/A';

    return `
        <div class="task-card ${priorityClass}">
            <div class="card-header">
                <div>
                    <span class="${priorityClass}">${task.priority.toUpperCase()}</span>
                    <span class="${statusClass}">${task.status}</span>
                    ${assignedBadge}
                </div>
                <small>Updated: ${updatedAt}</small>
            </div>
            <h3>${task.title}</h3>
            <p>${task.description || 'No description'}</p>
            ${task.notes ? `<p class="notes"><strong>Notes:</strong> ${task.notes}</p>` : ''}
            <div class="flex mt-4">
                ${task.status === 'in-progress' ? `
                    <button class="btn btn-success btn-sm" onclick="completeTask(${task.id})">
                        ✅ Complete
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="blockTask(${task.id})">
                        🚫 Block
                    </button>
                ` : ''}
                ${task.status === 'blocked' ? `
                    <button class="btn btn-primary btn-sm" onclick="unblockTask(${task.id})">
                        🔄 Unblock
                    </button>
                ` : ''}
                <button class="btn btn-danger btn-sm" onclick="confirmDeleteTask(${task.id})">
                    🗑️ Delete
                </button>
            </div>
        </div>
    `;
}

function renderTasksList(taskList, containerId) {
    const container = document.getElementById(containerId);

    if (!taskList || taskList.length === 0) {
        container.innerHTML = '<p class="text-center">No tasks in this category</p>';
        return;
    }

    container.innerHTML = taskList.map(task => renderTaskCard(task)).join('');
}

// Task Actions
async function completeTask(taskId) {
    try {
        await updateTask(taskId, { status: 'completed' });
        await refreshTasks();
        showNotification('Task completed successfully', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function blockTask(taskId) {
    const notes = prompt('Enter reason for blocking this task:');
    if (!notes) return;

    try {
        await updateTask(taskId, { status: 'blocked', notes });
        await refreshTasks();
        showNotification('Task blocked', 'warning');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function unblockTask(taskId) {
    try {
        await updateTask(taskId, { status: 'in-progress' });
        await refreshTasks();
        showNotification('Task unblocked', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

function confirmDeleteTask(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        deleteTask(taskId);
    }
}

async function deleteTask(taskId) {
    try {
        await deleteTask(taskId);
        await refreshTasks();
        showNotification('Task deleted', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function refreshTasks() {
    await fetchTasks(currentFilters);
    renderTasks();
}

// Form Handling
async function handleCreateTask(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const taskData = {
        title: formData.get('title'),
        description: formData.get('description'),
        priority: formData.get('priority'),
        assigned_agent: formData.get('assigned_agent')
    };

    try {
        await createTask(taskData);
        form.reset();
        await refreshTasks();
        showNotification('Task created successfully', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

// Notifications
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Style
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : type === 'warning' ? '#ffc107' : '#17a2b8'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Event Handlers (to be overridden by page-specific code)
function onSquadStatusUpdate(data) {
    console.log('Squad status updated:', data);
}

function onTaskCountUpdate(data) {
    console.log('Task count updated:', data);
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    initDOM();
    initSSE();
});

// Animation keyframes (added via JS to avoid CSS complexity)
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);
