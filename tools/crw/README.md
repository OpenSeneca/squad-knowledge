# crw - CrewAI Workflow Manager

A command-line tool for creating, managing, and orchestrating AI agent crews using YAML configuration.

## Overview

`crw` helps you define crews of AI agents with roles, goals, tasks, and workflows in a simple YAML format. Inspired by CrewAI, it provides a lightweight way to manage multi-agent systems.

## Installation

```bash
# Create symlink to PATH
ln -s ~/.openclaw/workspace/tools/crw/crw.py ~/.local/bin/crw

# Make executable
chmod +x ~/.openclaw/workspace/tools/crw/crw.py
```

## Quick Start

```bash
# Initialize crew directory
crw init

# Create a new crew
crw create research-team -d "Research and content creation crew"

# View your crew
crw show research-team

# List all crews
crw list

# Run a crew
crw run research-team

# Delete a crew
crw delete research-team
```

## Crew Configuration

Crews are defined in `~/.crew/<crew-name>/crew.yaml`:

```yaml
version: "1.0"

name: research-team
description: Research and content creation crew

agents:
  - id: researcher
    name: "Sarah"
    role: "Research Agent"
    goal: "Find and analyze information thoroughly"
    backstory: "An expert researcher with 10 years of experience"
    llm: "openai/gpt-4"
    tools: []
    verbose: true

  - id: writer
    name: "Mike"
    role: "Writer Agent"
    goal: "Create clear and engaging content"
    backstory: "A skilled technical writer"
    llm: "openai/gpt-4"
    tools: []
    verbose: true

tasks:
  - id: research
    name: "Gather Information"
    description: "Research the topic from multiple sources"
    expected_output: "Comprehensive research notes"
    agent: researcher
    context: []

  - id: draft
    name: "Write First Draft"
    description: "Create initial content based on research"
    expected_output: "First draft of the article"
    agent: writer
    depends_on: [research]

execution:
  process: "sequential"
  manager_llm: "openai/gpt-4"
  verbose: true
```

## Commands

### `crw init`
Initialize the crew directory structure (`~/.crew/`).

### `crw create <name> [-d <description>]`
Create a new crew with default configuration.

### `crw list`
List all available crews.

### `crw show <name>`
Show detailed information about a crew.

### `crw run <name>`
Execute a crew (runs the `run.sh` script).

### `crw delete <name>`
Delete a crew and its directory.

## Directory Structure

```
~/.crew/
├── crews.json              # Registry of all crews
└── <crew-name>/
    ├── crew.yaml          # Crew configuration
    ├── run.sh             # Execution script
    └── output/            # Task outputs (auto-created)
```

## Integration with CrewAI

This tool provides the scaffolding and configuration management for CrewAI-style workflows. To actually execute the agents, you would:

1. **Install CrewAI**: `pip install crewai`

2. **Create a Python runner** that reads `crew.yaml` and instantiates CrewAI agents:

```python
from crewai import Agent, Task, Crew, Process
import yaml

with open('crew.yaml') as f:
    config = yaml.safe_load(f)

# Create agents
agents = {}
for agent_config in config['agents']:
    agents[agent_config['id']] = Agent(
        role=agent_config['role'],
        goal=agent_config['goal'],
        backstory=agent_config['backstory'],
        verbose=agent_config.get('verbose', True)
    )

# Create tasks
tasks = {}
for task_config in config['tasks']:
    tasks[task_config['id']] = Task(
        description=task_config['description'],
        expected_output=task_config['expected_output'],
        agent=agents[task_config['agent']],
        context=[tasks[dep] for dep in task_config.get('depends_on', [])]
    )

# Create and run crew
crew = Crew(
    agents=list(agents.values()),
    tasks=list(tasks.values()),
    process=Process.sequential if config['execution']['process'] == 'sequential' else Process.hierarchical,
    verbose=True
)

result = crew.kickoff()
```

3. **Update `run.sh`** to run your Python script instead of the demo.

## Features

- ✅ YAML-based configuration
- ✅ Multi-agent definitions
- ✅ Task dependencies
- ✅ Sequential or hierarchical execution
- ✅ Crew registry and management
- ✅ Auto-generated execution scripts
- ✅ Zero external dependencies for core functionality

## Future Enhancements

- [ ] Direct CrewAI integration (Python backend)
- [ ] Task execution monitoring
- [ ] Output templates
- [ ] Crew templates (research, writing, analysis)
- [ ] Export to Python script
- [ ] Web dashboard integration

## License

MIT

## Author

Built by Archimedes (AI Agent) for the OpenClaw ecosystem.
