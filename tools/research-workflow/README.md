# Research Workflow Manager

A CLI tool for managing research projects and workflows. Integrates with research-note, research-digest, and squad-meeting.

## Why This Matters

Research needs structure. Marcus (AI research) and Galen (biopharma research) both need to:

- Track multiple research projects
- Manage tasks within each project
- Run research-digest on project files
- Export project summaries

This tool provides project-based research management with task tracking and tool integration.

## Installation

```bash
cd ~/.openclaw/workspace/tools/research-workflow
chmod +x research-workflow
ln -sf $(pwd)/research-workflow ~/.local/bin/research-workflow
```

## Usage

### Create a Project

```bash
research-workflow create \
  --project "AI Agent Memory Research" \
  --type ai-research \
  --description "Investigate memory infrastructure for AI agents" \
  --tags "memory,agents,claude-mem" \
  --owner marcus
```

Output:
```
🔬 Research Workflow Manager
   Manage research projects and workflows

✅ Project created!
📁 ID: a1b2c3d4
📝 Name: AI Agent Memory Research
🔬 Type: ai-research
🏷️  Tags: memory, agents, claude-mem
👤 Owner: marcus
📂 Directory: ~/.openclaw/research-workflow/a1b2c3d4
```

### List Projects

```bash
# All projects
research-workflow list

# Filter by status
research-workflow list --status active

# Filter by type
research-workflow list --type ai-research

# Filter by owner
research-workflow list --owner marcus
```

Shows:
- Project details (name, ID, type, owner)
- Status and tags
- Task summary (total, completed, blocked)

### Add Tasks

```bash
research-workflow add-task \
  --project-id a1b2c3d4 \
  --task "Read claude-mem paper" \
  --description "Analyze memory architecture" \
  --priority high \
  --assignee marcus
```

### Update Task Status

```bash
research-workflow task-status \
  --task-id e5f6g7h8 \
  --status in-progress

research-workflow task-status \
  --task-id e5f6g7h8 \
  --status completed
```

Valid statuses: `todo`, `in-progress`, `completed`, `blocked`

### Run Digest

```bash
research-workflow digest --project-id a1b2c3d4
```

This runs `research-digest` on the project directory, extracting:
- Tweet drafts
- Blog angles
- Key insights

Saves results to: `~/.openclaw/research-workflow/<project-id>/digest.json`

### Export Project

```bash
research-workflow export \
  --project-id a1b2c3d4 \
  --output memory-research.md
```

Generates Markdown with:
- Project details (type, owner, status)
- Description and tags
- All tasks with status and assignees

## Options

### create
| Option | Description |
|--------|-------------|
| `--project TEXT` | Project name (required) |
| `--type TYPE` | Project type (ai-research, biopharma, competitive-analysis, tool-exploration, general) |
| `--description TEXT` | Project description |
| `--tags TAGS` | Comma-separated tags |
| `--owner NAME` | Project owner |

### list
| Option | Description |
|--------|-------------|
| `--status STATUS` | Filter by status (active, completed, archived) |
| `--type TYPE` | Filter by type |
| `--owner NAME` | Filter by owner |

### add-task
| Option | Description |
|--------|-------------|
| `--project-id ID` | Project ID (required) |
| `--task TEXT` | Task name (required) |
| `--description TEXT` | Task description |
| `--priority LEVEL` | Priority: low, medium, high (default: medium) |
| `--assignee NAME` | Task assignee (default: unassigned) |

### task-status
| Option | Description |
|--------|-------------|
| `--task-id ID` | Task ID (required) |
| `--status STATUS` | New status (required) |

### digest
| Option | Description |
|--------|-------------|
| `--project-id ID` | Project ID (required) |

### export
| Option | Description |
|--------|-------------|
| `--project-id ID` | Project ID (required) |
| `--output FILE` | Output file (default: <id>-project.md) |

## Data Storage

Projects stored in: `~/.openclaw/research-workflow/projects.json`

Each project has its own directory: `~/.openclaw/research-workflow/<project-id>/`

Format:
```json
{
  "projects": [
    {
      "id": "a1b2c3d4",
      "name": "AI Agent Memory Research",
      "type": "ai-research",
      "description": "Investigate memory...",
      "tags": ["memory", "agents"],
      "owner": "marcus",
      "status": "active",
      "createdAt": "2026-02-21T07:00:00.000Z",
      "updatedAt": "2026-02-21T07:30:00.000Z"
    }
  ],
  "tasks": [
    {
      "id": "e5f6g7h8",
      "projectId": "a1b2c3d4",
      "name": "Read claude-mem paper",
      "description": "Analyze memory architecture",
      "priority": "high",
      "assignee": "marcus",
      "status": "in-progress",
      "createdAt": "2026-02-21T07:15:00.000Z",
      "updatedAt": "2026-02-21T07:30:00.000Z"
    }
  ]
}
```

## Project Types

- **ai-research**: AI models, frameworks, agent systems
- **biopharma**: Clinical trials, drug development, biotech
- **competitive-analysis**: Company research, market analysis
- **tool-exploration**: CLI tools, frameworks, new tech
- **general**: Miscellaneous research

## Example Workflow

### AI Research Project

```bash
# 1. Create project
research-workflow create \
  --project "Memory Infrastructure" \
  --type ai-research \
  --owner marcus

# Save ID: a1b2c3d4

# 2. Add tasks
research-workflow add-task \
  --project-id a1b2c3d4 \
  --task "Research claude-mem" \
  --priority high

research-workflow add-task \
  --project-id a1b2c3d4 \
  --task "Compare with alternatives" \
  --priority medium

# 3. Start first task
research-workflow task-status \
  --task-id <task-id> \
  --status in-progress

# 4. Use research-note to log findings
research-note "claude-mem architecture" \
  --note "Memory uses vector DB + retrieval" \
  --tags "memory,research"

# 5. Copy notes to project directory
cp ~/clawd/research/*.md ~/.openclaw/research-workflow/a1b2c3d4/

# 6. Run digest
research-workflow digest --project-id a1b2c3d4

# 7. Complete task
research-workflow task-status \
  --task-id <task-id> \
  --status completed

# 8. Export project
research-workflow export --project-id a1b2c3d4
```

## Integration with Squad Tools

Works with other research tools:

```bash
# Add research notes to project
research-note "Topic" --note "Findings" \
  | tee ~/.openclaw/research-workflow/<id>/notes.md

# After gathering notes, run digest
research-workflow digest --project-id <id>

# Create squad meeting for project discussion
squad-meeting create \
  --title "Project Review: <name>" \
  --participants seneca,marcus,galen \
  --agenda "Review findings and next steps"
```

## For Marcus

Use for AI research projects:
```bash
# Create AI research project
research-workflow create \
  --project "Agentic Workflows" \
  --type ai-research \
  --owner marcus

# Track tasks across multiple papers/tools
research-workflow add-task \
  --project-id <id> \
  --task "Read MCP documentation" \
  --priority high

# Log findings with research-note
research-note "MCP servers" --note "Standard protocol..."

# Generate digest for blog/twitter content
research-workflow digest --project-id <id>
```

## For Galen

Use for biopharma research projects:
```bash
# Create biopharma project
research-workflow create \
  --project "Drug Delivery Research" \
  --type biopharma \
  --owner galen

# Track clinical trial reviews
research-workflow add-task \
  --project-id <id> \
  --task "Review Phase 2 results" \
  --priority critical

# Extract insights for reports
research-workflow digest --project-id <id>
```

## Notes

- All projects stored locally (no external deps)
- Project directories created automatically
- Integrates with research-digest (must be installed)
- Can export to Markdown for documentation
- Task status: todo, in-progress, completed, blocked

## License

MIT
