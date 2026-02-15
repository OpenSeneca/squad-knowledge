# ctx - AI Context Manager

A command-line tool for managing AI agent contexts, sessions, and knowledge bases.

## Overview

`ctx` helps you maintain persistent context across AI agent interactions. Track system prompts, available tools, rules, conversation history, and knowledge bases for different AI sessions.

## Installation

```bash
# Create symlink to PATH
ln -s ~/.openclaw/workspace/tools/ctx/ctx.py ~/.local/bin/ctx

# Make executable
chmod +x ~/.openclaw/workspace/tools/ctx/ctx.py
```

## Quick Start

```bash
# Initialize ctx directory
ctx init

# Create a new session
ctx create coding-assistant -d "Python coding help"

# Update session with context
ctx update coding-assistant -c "You are an expert Python developer"

# Add tools the agent can use
ctx update coding-assistant --add-tool web_search
ctx update coding-assistant --add-tool file_operations

# Add rules for the agent
ctx update coding-assistant --add-rule "Always include docstrings"
ctx update coding-assistant --add-rule "Use type hints"

# View session details
ctx show coding-assistant

# Export context for use with other tools
ctx export coding-assistant -o context.txt

# List all active sessions
ctx list
ctx list --all  # Include archived
```

## Commands

### `ctx init`
Initialize the ctx directory structure (`~/.ctx/`).

### `ctx create <name> [-d <description>] [-t <template>]`
Create a new AI session with optional template.

### `ctx list [--all]`
List all active sessions. Use `--all` to include archived sessions.

### `ctx show <name>`
Show detailed information about a session, including context, tools, rules, history, and knowledge base.

### `ctx update <name> [-c <context>] [--add-tool <tool>] [--add-rule <rule>] [-d <description>]`
Update session context, tools, rules, or description.

### `ctx archive <name>`
Archive a session (mark as inactive).

### `ctx activate <name>`
Activate an archived session.

### `ctx export <name> [-o <output>]`
Export session context to formatted text file or stdout.

### `ctx add-knowledge <name> <title> <content> [-t <tags>]`
Add knowledge to a session's knowledge base.

### `ctx delete <name>`
Delete a session permanently.

## Session Management

Sessions contain:

- **Context**: System prompt defining the AI's role and behavior
- **Tools**: List of tools/functions the AI can use
- **Rules**: Behavioral rules and constraints
- **History**: Conversation history across sessions
- **Knowledge Base**: Persistent knowledge items with tags
- **Status**: Active or archived

## Use Cases

### 1. Project-Specific AI Assistants

Create dedicated sessions for different projects:

```bash
ctx create web-dev -d "Web development assistant"
ctx create data-science -d "Data analysis and ML"
ctx create devops -d "Infrastructure and deployment"
```

Each session maintains its own context and knowledge.

### 2. Team AI Contexts

Share consistent AI configurations across team members:

```bash
# Export session
ctx export web-dev -o team-context.txt

# Team members import/use the same context
```

### 3. Knowledge Accumulation

Build up knowledge bases over time:

```bash
ctx add-knowledge web-dev "FastAPI Best Practices" \
  "Use async endpoints, dependency injection, Pydantic models..." \
  -t api python performance

ctx add-knowledge web-dev "Common Errors" \
  "1. CORS issues - use CORSMiddleware..." \
  -t debugging errors
```

### 4. Context Switching

Quickly switch between different AI personas:

```bash
# Switch to coding mode
ctx activate coding-assistant

# Switch to writing mode
ctx activate copywriter

# Switch to research mode
ctx activate researcher
```

## Directory Structure

```
~/.ctx/
├── sessions.json       # Session registry
├── knowledge.json     # Shared knowledge base
└── templates.json     # Session templates
```

## Templates

Templates provide pre-configured session setups:

```bash
# Create from template
ctx create my-session -t default

# Available templates:
- default: General-purpose assistant
```

Custom templates can be added to `~/.ctx/templates.json`.

## Exported Context Format

Exported sessions include:

```markdown
# Context for coding-assistant

## Description
Python coding help

## System Context
You are an expert Python developer...

## Available Tools
web_search, file_operations

## Rules
- Always include docstrings
- Use type hints

## Session History (N entries)
- 2026-02-15T10:00:00: Fixed bug in user service...
- 2026-02-15T09:30:00: Added unit tests...

## Knowledge Base (N items)
- FastAPI Best Practices: Use async endpoints...
- Common Errors: CORS issues require...
```

This format can be pasted directly into AI prompts or used with other tools.

## Features

- ✅ Persistent session management
- ✅ System context tracking
- ✅ Tool availability configuration
- ✅ Rule enforcement
- ✅ Conversation history
- ✅ Knowledge base with tags
- ✅ Session templates
- ✅ Active/archived states
- ✅ Export to formatted text
- ✅ Zero external dependencies

## Integration Ideas

**With OpenClaw:**
```bash
# Export context
ctx export my-session -o context.txt

# Use with OpenClaw
openclaw agent -f context.txt
```

**With Claude Code:**
```bash
# Export and pipe to Claude
ctx export coding | claude code --context -
```

**Custom Scripts:**
```bash
# Auto-load context in shell scripts
context=$(ctx export my-session)
ai-assistant --context "$context"
```

## Best Practices

1. **Create Specific Sessions**: One session per project or use case
2. **Update Context Regularly**: Keep system prompts current
3. **Add Knowledge Frequently**: Build up knowledge bases over time
4. **Archive Old Sessions**: Keep active list clean
5. **Export for Sharing**: Share consistent contexts with teams

## Future Enhancements

- [ ] Session cloning
- [ ] Knowledge base search
- [ ] Tag-based filtering
- [ ] Integration with AI providers
- [ ] Context templates marketplace
- [ ] Session comparison/merge
- [ ] History cleanup and summarization

## License

MIT

## Author

Built by Archimedes (AI Agent) for the OpenClaw ecosystem.
