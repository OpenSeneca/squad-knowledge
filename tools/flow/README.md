# flow - Development Workflow Orchestrator

A command-line tool for orchestrating development workflows that combine prj, agt, tick, snip, and crw tools.

## Overview

`flow` helps you define repeatable development workflows with multiple stages. Each stage can run commands using your favorite CLI tools, making it easy to automate common development patterns.

## Installation

```bash
# Create symlink to PATH
ln -s ~/.openclaw/workspace/tools/flow/flow.py ~/.local/bin/flow

# Make executable
chmod +x ~/.openclaw/workspace/tools/flow/flow.py
```

## Quick Start

```bash
# Initialize flow directory
flow init

# Create a new workflow
flow create project-setup -d "Setup new project structure"

# View your workflow
flow show project-setup

# Run a workflow (dry run to preview)
flow run project-setup --dry-run

# Run for real
flow run project-setup

# List all workflows
flow list

# Delete a workflow
flow delete project-setup
```

## Workflow Configuration

Workflows are defined in `~/.flow/<workflow-name>/workflow.yaml`:

```yaml
name: project-setup
description: Setup new project structure

stages:
  - id: setup
    name: "Setup Project"
    description: "Initialize project structure"
    commands:
      - tool: prj
        action: create
        args: ["{{project_name}}", "--type", "{{project_type}}"]
      - tool: snip
        action: add
        args: ["{{project_name}}-start", "# {{project_name}}", "-t", "project"]

  - id: develop
    name: "Development"
    description: "Develop the application"
    commands:
      - tool: tick
        action: add
        args: ["Implement core features", "-p", "high"]
      - tool: agt
        action: create
        args: ["{{project_name}}-agent", "--template", "code"]
```

## Commands

### `flow init`
Initialize the flow directory structure (`~/.flow/`).

### `flow create <name> [-d <description>] [-t <template>]`
Create a new workflow with default configuration.

### `flow list`
List all available workflows.

### `flow show <name>`
Show detailed information about a workflow.

### `flow run <name> [--dry-run]`
Execute a workflow. Use `--dry-run` to preview commands without running them.

### `flow delete <name>`
Delete a workflow and its directory.

## Supported Tools

The following CLI tools can be used in workflows:

| Tool | Purpose | Example Commands |
|------|---------|-----------------|
| **prj** | Project scaffolding | `create my-project --type python` |
| **agt** | Agent scaffolding | `create my-agent --template research` |
| **tick** | Task tracking | `add "Fix bug" -p high`, `done 1` |
| **snip** | Snippet management | `add my-snippet "code here" -t tag` |
| **crw** | Crew orchestration | `create my-crew`, `run my-crew` |

## Example Workflows

### New Project Workflow

```yaml
stages:
  - id: project
    name: "Create Project"
    commands:
      - tool: prj
        action: create
        args: ["{{name}}", "--type", "{{type}}"]

  - id: agents
    name: "Setup Agents"
    commands:
      - tool: agt
        action: create
        args: ["{{name}}-dev", "--template", "code"]
      - tool: crw
        action: create
        args: ["{{name}}-crew", "-d", "{{name}} dev team"]

  - id: tasks
    name: "Initial Tasks"
    commands:
      - tool: tick
        action: add
        args: ["Setup project structure", "-p", "high"]
      - tool: tick
        action: add
        args: ["Implement core features", "-p", "medium"]
```

### Research Workflow

```yaml
stages:
  - id: research
    name: "Research Phase"
    commands:
      - tool: crw
        action: create
        args: ["research-team", "-d", "Research and analysis"]
      - tool: tick
        action: add
        args: ["Gather requirements", "-p", "high"]

  - id: documentation
    name: "Document Findings"
    commands:
      - tool: snip
        action: add
        args: ["research-notes", "# Research findings", "-t", "docs"]
```

## Directory Structure

```
~/.flow/
├── flows.json              # Registry of all workflows
└── <workflow-name>/
    └── workflow.yaml       # Workflow configuration
```

## Features

- ✅ Multi-stage workflow definitions
- ✅ Integration with prj, agt, tick, snip, crw tools
- ✅ Dry-run mode for previewing commands
- ✅ Workflow registry and management
- ✅ YAML-based configuration
- ✅ Template variables support ({{variable}})
- ✅ Zero external dependencies

## Use Cases

**Project Setup:** Automate creating new projects with consistent structure
- Create project with prj
- Setup dev agents with agt
- Create initial tasks with tick
- Save useful snippets with snip

**Research Workflows:** Coordinate research agents and documentation
- Create research crew with crw
- Track research tasks with tick
- Save research snippets with snip

**Development Pipelines:** Automate repetitive development tasks
- Standardize project initialization
- Ensure consistent agent setup
- Track progress with task management

## Future Enhancements

- [ ] Workflow templates (project, research, deployment)
- [ ] Conditional stages based on exit codes
- [ ] Workflow variables and parameter passing
- [ ] Parallel stage execution
- [ ] Workflow export/import
- [ ] Integration with CI/CD systems
- [ ] Web UI for workflow management

## License

MIT

## Author

Built by Archimedes (AI Agent) for the OpenClaw ecosystem.
