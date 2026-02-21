# Squad Meeting Manager

A CLI tool for managing squad meetings, agendas, and action items. Helps coordinate across agents (Seneca, Marcus, Galen, Archimedes).

## Why This Matters

The squad needs to:
- Track decisions and discussions
- Manage action items with assignees and due dates
- Coordinate across different agents
- Export meeting notes for documentation

This tool provides a simple, persistent way to manage squad meetings without external dependencies.

## Installation

```bash
cd ~/.openclaw/workspace/tools/squad-meeting
chmod +x squad-meeting
ln -sf $(pwd)/squad-meeting ~/.local/bin/squad-meeting
```

## Usage

### Create a Meeting

```bash
squad-meeting create \
  --title "Squad Sync - Q1 Planning" \
  --participants seneca,marcus,galen,archimedes \
  --duration 45 \
  --agenda "Review Q1 goals and assign tasks"
```

Output:
```
🤝 Squad Meeting Manager
   Coordinate squad meetings and actions

✅ Meeting created!
📅 ID: a1b2c3d4
📝 Title: Squad Sync - Q1 Planning
👥 Participants: seneca, marcus, galen, archimedes
⏱️  Duration: 45 minutes
📋 Status: scheduled
```

### List Meetings

```bash
# All meetings
squad-meeting list

# Filter by status
squad-meeting list --status scheduled

# Filter by agent participation
squad-meeting list --agent marcus
```

Shows:
- Meeting details (title, ID, status, participants)
- Notes count per meeting
- Action items (total + pending)
- Pending actions across all meetings

### Add Notes During Meeting

```bash
squad-meeting note \
  --meeting-id a1b2c3d4 \
  --note "Decided to prioritize dashboard deployment" \
  --author archimedes
```

### Create Action Items

```bash
# During a meeting
squad-meeting action \
  --meeting-id a1b2c3d4 \
  --description "Deploy squad dashboard to forge" \
  --assignee archimedes \
  --due 2026-02-25 \
  --priority high

# Standalone action (not tied to meeting)
squad-meeting action \
  --description "Research MCP servers" \
  --assignee marcus \
  --due 2026-02-28 \
  --priority medium
```

### Complete Actions

```bash
squad-meeting complete --action-id e5f6g7h8
```

### Update Meeting Status

```bash
# Start meeting
squad-meeting status --meeting-id a1b2c3d4 --status in_progress

# End meeting
squad-meeting status --meeting-id a1b2c3d4 --status completed

# Cancel meeting
squad-meeting status --meeting-id a1b2c3d4 --status cancelled
```

### Export Meeting Notes

```bash
squad-meeting export \
  --meeting-id a1b2c3d4 \
  --output squad-sync-notes.md
```

Generates Markdown with:
- Title, date, status, participants
- Agenda (if provided)
- All notes with timestamps and authors
- Action items with completion status

## Options

### create
| Option | Description |
|--------|-------------|
| `--title TEXT` | Meeting title (required) |
| `--participants LIST` | Comma-separated agent names (default: all agents) |
| `--duration MINUTES` | Duration in minutes (default: 30) |
| `--agenda TEXT` | Meeting agenda |

### list
| Option | Description |
|--------|-------------|
| `--status STATUS` | Filter by status (scheduled, in_progress, completed, cancelled) |
| `--agent NAME` | Filter by agent participation |

### note
| Option | Description |
|--------|-------------|
| `--meeting-id ID` | Meeting ID (required) |
| `--note TEXT` | Note content (required) |
| `--author NAME` | Note author (default: unknown) |

### action
| Option | Description |
|--------|-------------|
| `--description TEXT` | Action description (required) |
| `--meeting-id ID` | Associated meeting ID (optional) |
| `--assignee NAME` | Assigned agent (default: unassigned) |
| `--due DATE` | Due date (YYYY-MM-DD) |
| `--priority LEVEL` | Priority: low, medium, high (default: medium) |

### complete
| Option | Description |
|--------|-------------|
| `--action-id ID` | Action ID to complete (required) |

### status
| Option | Description |
|--------|-------------|
| `--meeting-id ID` | Meeting ID (required) |
| `--status STATUS` | New status (required) |

### export
| Option | Description |
|--------|-------------|
| `--meeting-id ID` | Meeting ID (required) |
| `--output FILE` | Output file (default: <id>-notes.md) |

## Valid Agents

- seneca
- marcus
- galen
- archimedes
- justin

## Data Storage

Meetings are stored in: `~/.openclaw/squad-meetings/meetings.json`

Format:
```json
{
  "meetings": [
    {
      "id": "a1b2c3d4",
      "title": "Squad Sync",
      "participants": ["seneca", "marcus", "galen"],
      "duration": 30,
      "agenda": "Review goals",
      "status": "completed",
      "notes": [...],
      "actions": [...],
      "createdAt": "2026-02-21T06:00:00.000Z",
      "updatedAt": "2026-02-21T06:30:00.000Z"
    }
  ],
  "actions": [
    {
      "id": "e5f6g7h8",
      "meetingId": "a1b2c3d4",
      "description": "Deploy dashboard",
      "assignee": "archimedes",
      "dueDate": "2026-02-25",
      "priority": "high",
      "status": "pending",
      "createdAt": "2026-02-21T06:15:00.000Z"
    }
  ]
}
```

## Example Workflow

### Weekly Squad Sync

```bash
# 1. Create meeting
squad-meeting create \
  --title "Weekly Squad Sync" \
  --participants seneca,marcus,galen,archimedes \
  --agenda "1. Review progress
2. Plan next week
3. Assign tasks"

# Save ID: a1b2c3d4

# 2. Start meeting
squad-meeting status --meeting-id a1b2c3d4 --status in_progress

# 3. Add notes during discussion
squad-meeting note \
  --meeting-id a1b2c3d4 \
  --note "Marcus found interesting new MCP server" \
  --author marcus

squad-meeting note \
  --meeting-id a1b2c3d4 \
  --note "Need to prioritize dashboard deployment" \
  --author justin

# 4. Create action items
squad-meeting action \
  --meeting-id a1b2c3d4 \
  --description "Research MCP server integration" \
  --assignee marcus \
  --due 2026-02-25 \
  --priority high

squad-meeting action \
  --meeting-id a1b2c3d4 \
  --description "Deploy dashboard to forge" \
  --assignee archimedes \
  --due 2026-02-23 \
  --priority critical

# 5. End meeting
squad-meeting status --meeting-id a1b2c3d4 --status completed

# 6. Export notes for documentation
squad-meeting export --meeting-id a1b2c3d4 --output weekly-sync-2026-02-21.md

# 7. Check pending actions
squad-meeting list
```

## Integration with Squad Tools

Works well with other squad tools:

```bash
# After squad-overview, identify blockers to discuss
squad-overview | grep "blocked"

# Create meeting to address blockers
squad-meeting create --title "Unblockers Sync" --agenda "Resolve SSH and deployment issues"

# Export notes and add to research-digest
squad-meeting export --meeting-id <id> | research-digest --stdin
```

## For the Squad

**Seneca**: Use for squad coordination, task delegation, and tracking overall progress
**Marcus**: Use for research syncs, tool decisions, and action item tracking
**Galen**: Use for biopharma research planning and cross-team coordination
**Archimedes**: Use for technical discussions, deployment planning, and engineering decisions
**Justin**: Use for high-level syncs, goal reviews, and squad direction

## Notes

- All meetings and actions stored locally (no external deps)
- Meeting IDs are 8-character hex strings
- Actions can be standalone or tied to meetings
- Exported notes include all metadata for documentation

## License

MIT
