# notes — Quick Note Taking Tool

Take notes with timestamps, tags, and categories. Search and organize easily.

**Location:** `~/workspace/tools/notes/`

**Install:** Symlink to `~/.local/bin/notes`

```bash
ln -s ~/workspace/tools/notes/notes.py ~/.local/bin/notes
chmod +x ~/workspace/tools/notes/notes.py
```

## Features

- **Quick Notes** — Add notes instantly with single command
- **Categories** — Organize by type (task, idea, meeting, etc.)
- **Tags** — Add multiple tags for easy filtering
- **Priorities** — Mark notes by priority (low, medium, high, urgent)
- **Search** — Find notes by text, category, or tags
- **Completion** — Mark notes as complete/incomplete
- **Statistics** — View note counts and distribution
- **Export** — Export to JSON or Markdown
- **Zero Dependencies** — Pure Python, no external packages

## Key Commands

### Note Operations

- `notes add "text"` — Add a new note
- `notes add "text" -c <category>` — Add with category
- `notes add "text" -t <tag1> <tag2>` — Add with tags
- `notes add "text" -p <priority>` — Add with priority
- `notes list` — List all notes
- `notes list -c <category>` — List by category
- `notes list -t <tag>` — List by tags
- `notes list -p <priority>` — List by priority
- `notes list -i` — List incomplete only
- `notes show <id>` — Show note details
- `notes edit <id>` — Edit a note
- `notes delete <id>` — Delete a note

### Completion

- `notes complete <id>` — Mark note as complete
- `notes uncomplete <id>` — Mark note as incomplete

### Search & Stats

- `notes search <query>` — Search notes
- `notes categories` — List all categories
- `notes stats` — Show statistics

### Export

- `notes export <file>` — Export to JSON
- `notes export <file> -f md` — Export to Markdown

## Examples

### Quick Notes

```bash
# Simple note
notes add "Remember to call John"

# With category
notes add "Fix login bug" -c task

# With tags
notes add "Great idea for app" -c idea -t feature -t brainstorm

# With priority
notes add "Critical security issue" -c task -p urgent

# All options
notes add "Deploy to production tonight" -c task -t deployment -t production -p high
```

### Listing Notes

```bash
# List all notes
notes list

# List by category
notes list -c task

# List by tags (AND logic - all tags must match)
notes list -t deployment -t production

# List by priority
notes list -p urgent

# List incomplete only
notes list -i

# List with limit
notes list -l 10
```

### Managing Notes

```bash
# Show details
notes show 5

# Edit note
notes edit 5 --text "Updated text"

# Edit category
notes edit 5 -c idea

# Edit tags
notes edit 5 -t new-tag -t updated

# Edit priority
notes edit 5 -p high

# Mark complete
notes complete 5

# Mark incomplete
notes uncomplete 5

# Delete note
notes delete 5
```

### Searching

```bash
# Search all text
notes search "squad"

# Search finds in:
# - Note text
# - Category names
# - Tags

# Results show matching notes
```

### Categories

```bash
# List all categories
notes categories

# Output:
# 📁 Categories:
#
#   • general: General notes and thoughts (3 notes)
#   • idea: Ideas and brainstorms (5 notes)
#   • task: Task reminders and TODOs (12 notes)
#   • meeting: Meeting notes (2 notes)
#   • learning: Learning and discoveries (8 notes)
#   • debug: Debugging notes and solutions (4 notes)
```

### Statistics

```bash
# Show stats
notes stats

# Output:
# 📊 Note Statistics
#
#   Total: 34
#   Completed: 18
#   Incomplete: 16
#
#   By Category:
#     • debug: 4
#     • idea: 5
#     • learning: 8
#     • meeting: 2
#     • task: 12
#     • general: 3
#
#   By Priority:
#     • urgent: 2
#     • high: 5
#     • medium: 20
#     • low: 7
```

### Export

```bash
# Export to JSON
notes export backup.json

# Export to Markdown
notes export notes.md -f md

# Markdown format includes:
# - Note ID and category
# - Creation timestamp
# - Tags and priority
# - Note text
# - Completion status (strikethrough)
```

## Categories

Default categories included:

| Category | Description | Use For |
|----------|-------------|----------|
| `general` | General notes and thoughts | Random thoughts, reminders |
| `idea` | Ideas and brainstorms | Feature ideas, improvements |
| `task` | Task reminders and TODOs | Action items, tasks |
| `meeting` | Meeting notes | Meeting summaries, action items |
| `learning` | Learning and discoveries | New concepts, tutorials |
| `debug` | Debugging notes and solutions | Bug fixes, troubleshooting |

## Priority Levels

- `low` — 🟢 Nice to have, not urgent
- `medium` — 🟡 Default priority, normal tasks
- `high` — 🔴 Important, needs attention soon
- `urgent` — 🚨 Critical, needs immediate attention

## Use Cases

### Quick Reminders

```bash
# Remember something quickly
notes add "Buy milk on way home" -c general -p medium

# Later, check incomplete notes
notes list -i
```

### Meeting Notes

```bash
# Start meeting
notes add "Meeting with product team - discuss dashboard features" -c meeting -t product -t dashboard

# Add points during meeting
notes add "Decision: Use polling not WebSocket" -c meeting -t decision -t dashboard
notes add "Action: Archimedes to implement" -c meeting -t action

# Review meeting notes later
notes list -c meeting
```

### Ideas Capture

```bash
# Capture idea
notes add "AI-powered code suggestions in editor" -c idea -t ai -t editor -t innovation -p high

# Search ideas later
notes search "ai"
```

### Task Management

```bash
# Add task
notes add "Fix SSH timeout on squad VMs" -c task -t bug -t ssh -p high

# Work on task...
# ...

# Mark complete
notes complete $(notes search "SSH timeout" | grep "^  #" | awk '{print $2}')

# Or find ID manually
notes show 5
notes complete 5
```

### Learning Notes

```bash
# Learn something new
notes add "TypeScript verbatimModuleSyntax requires type-only imports" -c learning -t typescript -t learning

# Later, review learnings
notes list -c learning
```

### Debugging Notes

```bash
# Log debugging session
notes add "SSH connection issue: Permission denied (publickey)" -c debug -t ssh -t squad

# Add solution
notes add "Solution: Need to manually configure SSH keys on VMs" -c debug -t ssh -t solution

# Search debug notes
notes list -c debug
```

### Project Brainstorming

```bash
# Brainstorm features
notes add "Real-time agent updates via WebSocket" -c idea -t feature -t realtime
notes add "Historical activity analytics" -c idea -t analytics -t history
notes add "Agent chat interface" -c idea -t chat -t communication

# Review ideas
notes list -c idea -p high
```

### Daily Planning

```bash
# Morning planning
notes add "Today: Fix dashboard, document tools" -c task -p high
notes add "Review PRs from team" -c task -p medium
notes add "Squad meeting at 2pm" -c task -p medium

# Evening review
notes list -i

# Mark completed
notes complete 1
notes complete 2
```

## Integration with Other Tools

**With tick (task tracker):**
```bash
# Add task to both
tick add "Fix SSH timeout" -p high
notes add "Remember: SSH keys needed on squad VMs" -c task -t ssh

# Mark done in both
tick done 1
notes complete $(notes search "SSH keys" | head -1 | grep -oP "#\K\d+")
```

**With focus (session tracker):**
```bash
# Start session
focus start "Implement feature X"

# Take notes during work
notes add "Use useEffect for data fetching" -c learning -t react
notes add "Remember to add error handling" -c task -p high

# End session
focus end

# Review session notes
notes list -t react
```

**With run (command runner):**
```bash
# Save command as note
notes add "Remember this command: ssh-copy-id -i ~/.ssh/key user@host" -c general -t ssh -t command

# Later, retrieve and save to run
notes show 5
# ... copy command ...
run add ssh-copy "ssh-copy-id -i ~/.ssh/key user@host"
```

**With snip (snippet manager):**
```bash
# During work, note useful code
notes add "Good pattern: try/except with specific error handling" -c learning -t python -t pattern

# Later, extract and save to snip
snip add try-except "try:\n    result = func()\nexcept SpecificError as e:\n    handle_error(e)"
```

**With git-helper (git automation):**
```bash
# Note commit message idea
notes add "feat(dashboard): Add real-time agent updates" -c idea -t commit -t squad

# When committing, use the note
notes show 5
# ... copy message ...
git-helper commit "feat(dashboard): Add real-time agent updates"
```

## Best Practices

### Taking Notes

**Be specific:**
```bash
# Good
notes add "Fix SSH timeout by increasing timeout to 10s in RealAgentService.ts" -c task -p high

# Less useful
notes add "Fix SSH" -c task -p high
```

**Use categories wisely:**
- `task` — Actionable items you'll complete
- `idea` — Features, improvements, innovations
- `meeting` — Meeting notes and action items
- `learning` — New knowledge, discoveries
- `debug` — Bug fixes and solutions
- `general` — Everything else

**Tag effectively:**
```bash
# Use specific, searchable tags
notes add "Squad dashboard WebSocket" -c idea -t squad -t websocket -t real-time

# Avoid generic tags
# notes add "Squad dashboard" -c idea -t project -t app  # Too generic
```

**Set appropriate priorities:**
- `urgent` — Breaking bugs, critical issues, immediate deadlines
- `high` — Important tasks, this week priority
- `medium` — Normal tasks, default priority
- `low` — Nice to have, backlog items

### Managing Notes

**Regular cleanup:**
```bash
# Review old incomplete notes
notes list -i

# Complete or delete outdated notes
notes complete 5
notes delete 10

# Or mark as completed
notes complete $(notes list -i | grep old | ...)
```

**Weekly review:**
```bash
# Check stats
notes stats

# Review by category
notes list -c idea
notes list -c task

# Clear completed
# Export first
notes export archive-$(date +%Y%m%d).md -f md

# Then delete completed
# (manual cleanup or future feature)
```

**Archive old notes:**
```bash
# Export everything
notes export full-backup.json

# Clean up old/completed
# Delete old notes manually
```

### Searching

**Use specific terms:**
```bash
# Search for specific items
notes search "typescript error"
notes search "squad dashboard"
notes search "websocket"

# Search finds in text, category, and tags
```

**Use category filters:**
```bash
# Context-specific views
notes list -c task        # Action items
notes list -c idea        # Brainstorming
notes list -c learning    # Knowledge base
notes list -c debug        # Solutions
```

## Data Storage

Notes stored in `~/.notes/`:

```
~/.notes/
├── notes.json           # All notes
└── categories.json     # Category definitions
```

**Note structure:**
```json
{
  "id": 1,
  "text": "Remember to fix the bug",
  "category": "task",
  "tags": ["bug", "ssh"],
  "priority": "high",
  "created": "2026-02-16T07:30:00.000000",
  "updated": "2026-02-16T08:15:00.000000",
  "completed": false,
  "completed_at": "2026-02-16T08:20:00.000000"
}
```

## Comparison to Alternatives

**vs Memory:**
- `notes`: Quick, structured, searchable
- `notes`: Tags, categories, priorities
- `notes`: Completion tracking

**vs sticky notes:**
- `notes`: Command-line, searchable
- `sticky`: Visual, harder to organize

**vs notepad:**
- `notes`: Structured (tags, categories)
- `notepad`: Unstructured text

**vs todo.txt:**
- `notes`: Categories, priorities, completion
- `todo.txt`: Simple, no metadata

## Future Enhancements

- **Due dates** — Add due dates to notes
- **Reminders** — Set time-based reminders
- **Notes linking** — Link related notes together
- **Recurring notes** — Automatic recurring reminders
- **Notes templates** — Pre-defined note formats
- **Attachment support** — Attach files to notes
- **Rich text** — Markdown formatting in notes
- **Web interface** — Browser-based note UI
- **Sync** — Sync across devices
- **Collaboration** — Shared notes

## Requirements

- Python 3.6+
- No external dependencies
- Storage: `~/.notes/` (auto-created)

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Fast. Organized. Searchable.**

Take notes instantly, organize by categories, and find them quickly.
