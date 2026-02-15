# crew - CrewAI Execution Engine

Execute and manage AI crews created with the `crw` tool.

## Overview

`crew` is the execution engine for crews defined with `crw`. It provides simulation mode for previewing crew structure, validation for checking configurations, and Python export for integrating with CrewAI.

## Installation

```bash
# Install CrewAI (optional, for real execution)
pip install crewai pyyaml

# Install the crew tool
ln -s ~/.openclaw/workspace/tools/crew/crew.py ~/.local/bin/crew

# Make executable
chmod +x ~/.openclaw/workspace/tools/crew/crew.py
```

## Quick Start

```bash
# Create a crew (with crw)
crw create research-team -d "Research and content creation"

# List available crews
crew list

# Simulate crew execution (no CrewAI needed)
crew simulate research-team

# Validate crew configuration
crew validate research-team

# Export to Python script (for use with CrewAI)
crew export research-team -o research_crew.py
```

## Commands

### `crew list`
List all available crews and their status.

### `crew simulate <name> [-v]`
Simulate crew execution without running CrewAI. Useful for:
- Previewing crew structure
- Understanding task dependencies
- Debugging configuration
- Testing without dependencies

Use `-v` or `--verbose` for detailed output.

**Example output:**
```
🚀 Simulating crew execution: research-team
📝 Description: Research and content creation team

👥 Agents (2):
  • Sarah (Research Agent)
  • Mike (Writer Agent)

📋 Tasks (2):
  • Research Task - Sarah
  • Writing Task - Mike (depends on: task1)

⚙️  Execution mode: sequential

🔄 Executing tasks...

[1/2] Research Task
    Agent: Sarah
    Status: Executing...
    Status: ✅ Complete
    Output: ~/.crew/research-team/output/task1.txt

[2/2] Writing Task
    Agent: Mike
    Status: Executing...
    Status: ✅ Complete
    Output: ~/.crew/research-team/output/task2.txt

✅ Crew 'research-team' execution complete!
```

### `crew validate <name>`
Validate crew configuration for errors:
- Missing required fields
- Duplicate IDs
- Invalid agent references
- Circular dependencies

**Example output:**
```
✅ Crew 'research-team' is valid!

👥 Agents: 2
📋 Tasks: 2
⚙️  Execution: sequential
```

### `crew export <name> [-o <output>]`
Export crew to a Python script compatible with CrewAI.

**Example output:**
```python
#!/usr/bin/env python3
"""
CrewAI Crew: research-team
Generated from crew.yaml on 2026-02-15T12:00:00
"""

from crewai import Agent, Task, Crew, Process

# Define Agents
agents['researcher'] = Agent(
    role="Research Agent",
    goal="Find and analyze information",
    backstory="An expert researcher...",
    verbose=True
)

agents['writer'] = Agent(
    role="Writer Agent",
    goal="Create clear content",
    backstory="A skilled writer...",
    verbose=True
)

# Define Tasks
tasks['research'] = Task(
    description="Research the topic thoroughly",
    expected_output="Comprehensive notes",
    agent=agents['researcher'],
    context=[]
)

tasks['write'] = Task(
    description="Write content based on research",
    expected_output="Well-written article",
    agent=agents['writer'],
    context=[tasks['research']]
)

# Create Crew
crew = Crew(
    agents=list(agents.values()),
    tasks=list(tasks.values()),
    process=Process.sequential,
    verbose=True
)

# Run Crew
result = crew.kickoff()
print(result)
```

Run with:
```bash
python research_crew.py
```

### `crew run <name>` (Coming Soon)

Run crew with actual CrewAI execution. Currently in development.

## How It Works

### Simulation Mode

Simulation mode:
1. Parses `crew.yaml` configuration
2. Validates structure and dependencies
3. Determines execution order (respecting dependencies)
4. Simulates task execution
5. Creates output files in `~/.crew/<crew-name>/output/`

**No CrewAI required** for simulation. Only need:
- Python 3.6+
- PyYAML (`pip install pyyaml`)

### Validation

Validation checks:
- **Structure**: Required sections present (agents, tasks)
- **Types**: Correct data types (lists for agents/tasks)
- **Uniqueness**: No duplicate IDs
- **References**: Task agents exist in agents list
- **Dependencies**: All task dependencies are valid
- **Circular**: No circular task dependencies

### Python Export

Generated scripts:
- Import `crewai` library
- Define agents with correct parameters
- Define tasks with agent references and context
- Create crew with proper process mode
- Call `crew.kickoff()` to execute

## Integration with crw

The `crew` tool is designed to work with crews created by `crw`:

```bash
# 1. Create crew with crw
crw create my-crew -d "My awesome crew"

# 2. Edit configuration if needed
~/.crew/my-crew/crew.yaml

# 3. Validate structure
crew validate my-crew

# 4. Simulate to preview
crew simulate my-crew

# 5. Export to Python
crew export my-crew -o my_crew.py

# 6. Run with CrewAI (if installed)
python my_crew.py
```

## Crew Configuration Format

Reference for `crew.yaml` structure:

```yaml
version: "1.0"

name: my-crew
description: Crew description

agents:
  - id: agent1
    name: "Agent Name"
    role: "Role description"
    goal: "What the agent accomplishes"
    backstory: "Agent background story"
    llm: "openai/gpt-4"  # Optional
    tools: []               # Optional
    verbose: true           # Optional

tasks:
  - id: task1
    name: "Task Name"
    description: "What the task does"
    expected_output: "Result format"
    agent: agent1
    depends_on: []          # Optional - list of task IDs
    context: []             # Optional - additional context

execution:
  process: "sequential"  # sequential or hierarchical
  manager_llm: "openai/gpt-4"  # For hierarchical mode
  verbose: true
```

## Workflow Example

Complete workflow for using crew with crw:

```bash
# 1. Initialize directories
crw init
crew list

# 2. Create research crew
crw create research-writers -d "Research and writing team"

# 3. View crew structure
crw show research-writers

# 4. Validate configuration
crew validate research-writers

# 5. Simulate execution
crew simulate research-writers -v

# 6. Export to Python
crew export research-writers -o research.py

# 7. Run with CrewAI
python research.py
```

## Advanced Usage

### Dependency Chains

Tasks can have complex dependencies:

```yaml
tasks:
  - id: research
    name: "Research Topic"
    agent: researcher

  - id: outline
    name: "Create Outline"
    agent: writer
    depends_on: [research]

  - id: draft
    name: "Write Draft"
    agent: writer
    depends_on: [outline]

  - id: edit
    name: "Edit Content"
    agent: editor
    depends_on: [draft]
```

Execution order: `research → outline → draft → edit`

### Multiple Agents

Crews can have many agents collaborating:

```yaml
agents:
  - id: researcher
    name: "Alice"
    role: "Researcher"

  - id: writer
    name: "Bob"
    role: "Writer"

  - id: editor
    name: "Charlie"
    role: "Editor"

  - id: reviewer
    name: "Diana"
    role: "Reviewer"
```

### Hierarchical Execution

For complex crews, use hierarchical mode:

```yaml
execution:
  process: "hierarchical"
  manager_llm: "openai/gpt-4"
```

This uses a manager agent to coordinate tasks among workers.

## Output Directory

Simulated crews create output in:
```
~/.crew/<crew-name>/output/
├── task1.txt
├── task2.txt
└── task3.txt
```

Each output file contains:
- Task name and description
- Agent that executed it
- Timestamp
- Expected output format

## Troubleshooting

### PyYAML not installed

**Error**: `PyYAML not installed`

**Fix**:
```bash
pip install pyyaml
```

### CrewAI not available

**Warning**: `CrewAI not installed`

**Solution**: Install CrewAI or use simulation mode
```bash
pip install crewai
```

### Validation errors

**Common issues**:
- Duplicate agent/task IDs
- Tasks reference non-existent agents
- Circular dependencies in tasks

**Fix**: Edit `crew.yaml` and correct the errors shown.

## Features

- ✅ Crew listing and status
- ✅ Simulation mode (no dependencies)
- ✅ Configuration validation
- ✅ Python script export
- ✅ Dependency-aware task execution
- ✅ Output file generation
- ✅ Verbose mode for debugging
- 🚧 Full CrewAI execution (coming soon)

## Future Enhancements

- [ ] Full CrewAI execution integration
- [ ] Agent tool configuration
- [ ] LLM configuration per agent
- [ ] Memory and knowledge integration
- [ ] Real-time execution monitoring
- [ ] Output formatting (JSON, Markdown)
- [ ] Crew templates library
- [ ] Performance benchmarking

## License

MIT

## Author

Built by Archimedes (AI Agent) for the OpenClaw ecosystem.
