# focus - Work Session and Focus Tracker

Track work sessions, take notes during sessions, and manage focus time.

## Features

- **Start Sessions** - Begin a focused work session with a task
- **Add Notes** - Take notes during active session with timestamps
- **End Sessions** - Complete session with duration calculation
- **List History** - View all past sessions with details
- **Today's Sessions** - Show focus work for the current day
- **Statistics** - Overview of productivity (total time, averages, best day)
- **Current Session** - Show active session status and notes

## Installation

```bash
# Make executable
chmod +x ~/workspace/tools/focus/focus.py

# Symlink to PATH
ln -sf ~/workspace/tools/focus/focus.py ~/.local/bin/focus
```

## Usage

### Start a Session

```bash
focus start <task>
```

Begin a new focus session.

**Example:**
```bash
focus start "Build squad dashboard"
focus start "Review pull requests"
focus start "Write documentation"
```

**What happens:**
- Creates active session
- Records start time
- Ready to accept notes
- Prevents multiple concurrent sessions

### Add Notes During Session

```bash
focus note <text>
```

Add a timestamped note to the current session.

**Example:**
```bash
focus note "Remember to add error handling"
focus note "Bug: SSH timeout needs increase"
focus note "Design decision: use polling over WebSocket"
focus note "Good progress on API"
```

**What happens:**
- Adds note with timestamp to current session
- Shows all notes in session
- Helps capture thoughts during focused work

### End Session

```bash
focus end
```

Complete the current focus session.

**What happens:**
- Records end time
- Calculates session duration
- Saves session to history
- Shows summary (task, duration, notes count)
- Clears active session

### List All Sessions

```bash
focus list
```

Show all past sessions with details.

**Output:**
```
Task                                    Date       Duration   Notes    Status
------------------------------------------------------------
Build squad dashboard                  2026-02-15  2h 15m    3        completed
Review pull requests                   2026-02-15  45m       1        completed
Write documentation                    2026-02-16  1h 30m    5        completed
Analyze SSH issues                     2026-02-16  30m       2        completed
```

### Show Today's Sessions

```bash
focus today
```

Display focus work for the current day.

**Output:**
```
📅 Today's Sessions
------------------------------------------------------------

✓ 3 session(s) today
  Total focus time: 4h 30m

Task                                    Duration
------------------------------------------------------------
Build squad dashboard                      2h 15m
Review pull requests                       1h 45m
Analyze SSH issues                        30m
```

### Show Statistics

```bash
focus stats
```

Display productivity statistics.

**Output:**
```
📊 Focus Statistics
------------------------------------------------------------

Total sessions: 25
Completed: 24
Total notes: 87
Total focus time: 42h 15m
Average duration: 1h 45m

Most productive day: 2026-02-15 (6h 30m)
```

### Show Current Session

```bash
focus current
```

Display the currently active session (if any).

**Output:**
```
🎯 Current Session
------------------------------------------------------------

  Task: Build squad dashboard
  Started: 2026-02-16T10:30:00
  Duration: 1h 15m
  Notes: 3

📝 Notes:
  1. [10:35:22] Remember to add error handling
  2. [11:02:45] Good progress on API
  3. [11:15:33] Need to handle timeouts
```

## Data Storage

Sessions are stored in `~/.focus/`:

```
~/.focus/
├── current.json      # Active session (if any)
└── sessions.json     # Session history
```

**Session Structure:**
```json
{
  "task": "Build squad dashboard",
  "start_time": "2026-02-16T10:30:00.000000",
  "end_time": "2026-02-16T12:15:00.000000",
  "duration_seconds": 6300,
  "duration_human": "1h 45m",
  "notes": [
    {
      "text": "Remember to add error handling",
      "time": "2026-02-16T10:35:22.000000"
    }
  ],
  "status": "completed"
}
```

**Status values:**
- `active` - Currently in progress
- `completed` - Finished normally
- `interrupted` - Could add this in future

## Use Cases

### Deep Work Sessions

Track focused coding or research sessions:

```bash
focus start "Implement SSH querying"
# ... work ...
focus note "Use child_process.exec()"
focus note "Add timeout handling"
# ... more work ...
focus end
```

### Meeting Notes

Take quick notes during meetings:

```bash
focus start "Team sync"
focus note "Decided to use polling not WebSocket"
focus note "Archimedes will handle build"
focus note "Timeline: 2 weeks for MVP"
focus end
```

### Time Tracking

Track how long you spend on different tasks:

```bash
# Morning
focus start "Email triage"
focus end

focus start "Code review"
focus end

# Afternoon
focus start "Feature development"
focus end

# Check daily summary
focus today
# Total: 4h 15m across 4 sessions
```

### Session Review

Review what you accomplished:

```bash
# Yesterday's work
focus list | grep "2026-02-15"

# What did I work on?
# How long did I spend?
# What notes did I take?
```

## Best Practices

### Starting Sessions
- Be specific with task names (e.g., "Build squad dashboard API" not just "Work")
- Start session when beginning focused work
- Don't track breaks/lunch (those dilute focus data)

### Taking Notes
- Take notes for important decisions, bugs, ideas
- Note things you might forget later
- Don't over-note (major points only)

### Ending Sessions
- End session when switching contexts (e.g., moving to different task)
- End session when taking extended break
- End session at natural stopping points

### Review
- Check `focus stats` weekly to understand productivity
- Review `focus today` to see daily progress
- Use `focus list` to understand patterns over time

## Integration with Other Tools

**With tick (task tracker):**
```bash
# Before starting work, list tasks
tick list

# Start session with highest priority task
focus start "$(tick list | grep high | head -1)"

# After session, mark task done
tick done <task_id>
```

**With snip (snippet manager):**
```bash
# During work, save code snippets
snip add "ssh-exec" "exec = require('child_process')"

# After session, review notes for snippets to save
focus list | grep today
# Extract useful code snippets from notes
```

## Productivity Tips

### Pomodoro Technique

```bash
# 25-minute focused session
focus start "Deep work session"
# Work for 25 minutes...
focus end

# 5-minute break
# Repeat
```

### Time Boxing

```bash
# Assign specific time to a task
focus start "Write documentation (1h limit)"
# ... focus on the task ...
focus end after 1 hour
```

### Deep Work Blocks

```bash
# Morning deep work
focus start "Build feature (3h)"
focus end

# Afternoon deep work
focus start "Review code (2h)"
focus end
```

## Troubleshooting

### "No active session"

If you get this error:
```bash
# No active session
# Use: focus start <task> to begin
```

Start a new session with `focus start <task>`.

### "A session is already active"

If you get this error when trying to start a new session:
```bash
# Use: focus current to see active session
# Use: focus end to finish it first
```

### Missing Data

If sessions.json is corrupted:

```bash
# Reset (WARNING: loses all history)
rm ~/.focus/sessions.json

# Or backup first
cp ~/.focus/sessions.json ~/.focus/sessions.json.backup
```

## Requirements

- Python 3.6+
- No external dependencies
- Storage: ~/.focus/ (auto-created)

## License

MIT

---

**Simple. Focused. Productive.**

Track what you work on and for how long. Perfect for deep work sessions, meetings with notes, and understanding your productivity patterns.
