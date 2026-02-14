# tick — Simple CLI Task Tracker

Track tasks, priorities, and completion status from the command line. Stop forgetting what you need to do.

## Installation

```bash
# Make it executable
chmod +x ~/workspace/tools/tick/tick.py

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$HOME/workspace/tools/tick"

# Or create a symlink
ln -s ~/workspace/tools/tick/tick.py ~/.local/bin/tick
```

## Usage

### Add a task

```bash
# Basic task
tick add "Fix the bug"

# With priority
tick add "Deploy to production" -p high

# With description and tags
tick add "Review PR #123" -p high -t work github -d "Security fix, needs attention"
```

### List tasks

```bash
# List all tasks
tick list

# Filter by status
tick list --status todo
tick list --status done

# Filter by priority
tick list --priority high

# Filter by tag
tick list --tag github
```

### Complete / Reopen tasks

```bash
# Mark task as done
tick done 5

# Reopen a completed task
tick undo 5
```

### Update a task

```bash
# Update title
tick update 3 -t "New title"

# Update priority
tick update 3 -p high

# Update description
tick update 3 -d "Updated description"
```

### Show task details

```bash
tick show 5
```

### Delete tasks

```bash
# Delete specific task
tick delete 3

# Delete all completed tasks
tick clear
```

### Statistics

```bash
tick stats
```

Output:
```
📊 Task Statistics
   Total: 12
   Done: 7
   Todo: 5

   By Priority (todo):
   🔴 High: 2
   🟡 Medium: 2
   🟢 Low: 1
```

## Data Location

Tasks are stored in `~/.tick/tasks.json` (JSON format, easy to edit manually if needed).

## Priority Levels

- 🔴 **High** - Urgent, needs attention soon
- 🟡 **Medium** - Normal priority, default
- 🟢 **Low** - Nice to have, can wait

## Tags

Use tags to organize tasks by context:

```bash
tick add "Fix auth bug" -t github high-priority
tick add "Write docs" -t docs low-priority
tick add "Review PR" -t github

# Filter by tag later
tick list --tag github
```

## Why This Exists

Because sticky notes get lost, todo apps are overkill, and "I'll remember that" is a lie. A simple CLI that's always in your terminal.

## Examples

```bash
# Personal tasks
tick add "Buy groceries" -p medium -t personal
tick add "Call mom" -p high -t personal

# Work tasks
tick add "Review code" -p high -t work github
tick add "Deploy to staging" -p medium -t work
tick add "Write documentation" -p low -t work docs

# Learning tasks
tick add "Learn Rust" -p low -t learning
tick add "Read system design book" -p medium -t learning

# Track progress
tick list --priority high
tick stats

# When done
tick done 3
tick done 5

# Cleanup
tick clear
```

## Tips

1. **Keep it simple** - If it takes more than a sentence, break it into multiple tasks
2. **Use priorities** - Mark truly urgent tasks as high
3. **Tag by context** - Group related tasks with tags
4. **Review weekly** - Use `tick clear` to clean up completed tasks
5. **Make it a habit** - Run `tick list` at the start of each session

## Integration Ideas

- **Pre-commit hook** - Remind you to check tasks before committing
- **Shell prompt** - Show todo count in your prompt
- **Cron job** - Send daily task summary via email
- **Team sync** - Share tasks.json with your team (version control)

## File Format

```json
[
  {
    "id": 1,
    "title": "Example task",
    "description": "Optional description",
    "priority": "high",
    "tags": ["work", "github"],
    "status": "todo",
    "created": "2026-02-14T12:00:00",
    "completed": null
  }
]
```
