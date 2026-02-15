# toolbox - OpenClaw CLI Tool Manager

Overview and manage all OpenClaw CLI tools from a single interface.

## Overview

`toolbox` provides a centralized interface for the OpenClaw CLI toolset. List tools, search capabilities, check installation status, and discover common workflows.

## Installation

```bash
# Install toolbox
ln -s ~/.openclaw/workspace/tools/toolbox/toolbox.py ~/.local/bin/toolbox

# Make executable
chmod +x ~/.openclaw/workspace/tools/toolbox/toolbox.py
```

## Quick Start

```bash
# List all tools
toolbox list

# Show tool details
toolbox show prj

# Search for tools
toolbox search research

# Show workflow examples
toolbox workflows

# Show statistics
toolbox stats
```

## Commands

### `toolbox list [-v]`
List all available tools and their installation status.

**Example:**
```
🧰 OpenClaw CLI Toolbox - 8 tools

✅ prj — Project Scaffolding
✅ agt — Agent Scaffolding
✅ snip — Snippet Manager
✅ tick — Task Tracker
✅ crw — CrewAI Workflow Manager
✅ flow — Workflow Orchestrator
✅ ctx — AI Context Manager
✅ crew — CrewAI Execution Engine
```

Use `-v` for verbose details (location, description, commands).

### `toolbox show <tool>`
Show detailed information about a specific tool.

**Example:**
```
📦 Tool: prj
📝 Name: Project Scaffolding
📍 Location: ~/workspace/tools/prj
✅ Status: ✅ Installed

📄 Description:
   Create new projects with best-practice structure

🛠️  Available Commands:
   • init
   • types
   • create
   • list

💡 Example Usage:
   prj create my-project -t python

📖 Documentation:
   /home/exedev/.openclaw/workspace/tools/prj/README.md
```

### `toolbox search <query>`
Search for tools by name or description.

**Example:**
```
🔍 Found 2 tool(s) matching 'workflow':

✅ crw — CrewAI Workflow Manager
   Create and manage AI agent crews

✅ flow — Workflow Orchestrator
   Orchestrate multi-stage development workflows
```

### `toolbox workflows`
Show common workflow examples using multiple tools.

**Example:**
```
🔄 Common Workflows

1. New Project Setup
   Start a new Python project with agents and tasks
   Commands:
     • prj create my-api -t python
     • agt create api-agent -t code
     • crw create api-crew -d 'API development'
     • ctx create python-dev -d 'Python API context'
     • tick add 'Setup project structure' -p high

2. Research Workflow
   Set up research agents and context
   Commands:
     • crw create research-team -d 'Research and writing'
     • crew simulate research-team
     • ctx create researcher -d 'AI research agent'
     • snip add research-note 'Findings here' -t research

3. Development Pipeline
   Multi-stage workflow for production code
   Commands:
     • flow create dev-pipeline -d 'Full dev workflow'
     • flow run dev-pipeline --dry-run
     • tick add 'Implement features' -p high
     • snip add debug-tip 'How to debug' -t debugging
```

### `toolbox stats`
Show statistics about the toolbox.

**Example:**
```
📊 Toolbox Statistics

📦 Total Tools: 8
✅ Installed: 8
❌ Not Found: 0
📈 Coverage: 100%

🛠️  Commands Distribution:
   Total Commands: 35
   Average per Tool: 4.4
```

## Tool Categories

### Project Creation
- **prj** - Project scaffolding (Python, TypeScript, web, CLI)
- **agt** - Agent scaffolding (research, code, writer, analyst)

### Development Tools
- **snip** - Snippet management with tags
- **tick** - Task tracking with priorities

### AI & Workflow
- **crw** - CrewAI workflow manager (YAML config)
- **flow** - Workflow orchestrator (multi-stage pipelines)
- **ctx** - AI context and session manager
- **crew** - CrewAI execution engine (simulation, validation)

## Integration Examples

### 1. Start a New Project

```bash
# Create project
prj create my-app -t typescript

# Create agent
agt create app-agent -t code

# Create workflow
flow create app-dev -d "App development workflow"

# Track tasks
tick add "Setup structure" -p high
tick add "Implement features" -p medium

# Save snippets
snip add setup-commands "npm install && npm test" -t dev
```

### 2. Research and Analysis

```bash
# Create crew
crw create research-team -d "Research and writing"

# Simulate execution
crew simulate research-team -v

# Export context
ctx create researcher -d "AI research agent"
ctx update researcher -c "You are an expert researcher"

# Save findings
snip add research-results "Key findings from analysis" -t research
```

### 3. Development Workflow

```bash
# Create workflow
flow create full-cycle -d "Complete development cycle"

# Preview workflow
flow run full-cycle --dry-run

# Execute workflow
flow run full-cycle

# Track progress
tick list --priority high
```

## Tool Status

Tool `toolbox` automatically checks if each tool is installed:

- **✅ Installed** - Tool responds to `--help` command
- **❌ Not Installed** - Tool not found in PATH
- **⚠️ Error** - Tool found but has errors

Run `toolbox stats` to see overall coverage.

## Finding the Right Tool

Not sure which tool to use? Try:

```bash
# Search by keyword
toolbox search project
toolbox search agent
toolbox search workflow
toolbox search task
toolbox search snippet
```

Or use `toolbox list -v` to see all tools with descriptions.

## Complete Tool List

| Tool | Name | Primary Use |
|------|-------|-------------|
| prj | Project Scaffolding | Create new projects |
| agt | Agent Scaffolding | Create AI agents |
| snip | Snippet Manager | Save code snippets |
| tick | Task Tracker | Track to-dos |
| crw | CrewAI Workflow | Manage AI crews |
| flow | Workflow Orchestrator | Automate workflows |
| ctx | AI Context Manager | Manage AI sessions |
| crew | CrewAI Execution | Run AI crews |
| toolbox | Tool Manager | Manage all tools |

## Features

- ✅ Centralized tool overview
- ✅ Installation status checking
- ✅ Tool search by name/description
- ✅ Workflow examples
- ✅ Statistics and coverage
- ✅ Detailed tool information
- ✅ Common command patterns

## Design Philosophy

The OpenClaw toolset follows these principles:

1. **Composability**: Tools work together naturally
2. **Discoverability**: `--help` on all tools, searchable via toolbox
3. **Simplicity**: Single-file, zero dependencies
4. **Consistency**: Similar command patterns across tools

## Troubleshooting

### Tool Shows as Not Installed

**Symptom**: `toolbox list` shows tool as `❌ Not Installed`

**Cause**: Symlink broken or tool not in PATH

**Fix**:
```bash
# Check symlink
ls -la ~/.local/bin/<tool>

# Re-create if needed
ln -s ~/.openclaw/workspace/tools/<tool>/<tool>.py ~/.local/bin/<tool>
```

### Tool Shows as Error

**Symptom**: `toolbox list` shows tool as `⚠️ Error`

**Cause**: Tool has runtime errors or missing dependencies

**Fix**:
```bash
# Run tool directly
<tool> --help

# Check dependencies
python3 -c "import yaml; print('PyYAML ok')"
```

## Future Enhancements

- [ ] Interactive mode for tool discovery
- [ ] Tool updates and version checking
- [ ] Integration tests between tools
- [ ] Web UI for tool management
- [ ] Tool recommendation system
- [ ] Command completion (bash/zsh)

## License

MIT

## Author

Built by Archimedes (AI Agent) for the OpenClaw ecosystem.
