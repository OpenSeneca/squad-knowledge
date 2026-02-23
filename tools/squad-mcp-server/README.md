# Squad MCP Server

Expose squad CLI tools via Model Context Protocol (MCP), enabling Claude, Codex, Gemini CLI, and other AI assistants to access squad capabilities directly.

## What Is MCP?

MCP (Model Context Protocol) is a standard for connecting AI applications to external systems—files, databases, internal tools—so AI has usable context and can do tool-based work.

**Without MCP:**
- You paste a policy into Claude every time
- Manual context sharing
- Inconsistent outputs

**With MCP:**
- Claude accesses approved knowledge sources directly
- Consistent team outputs
- Better audit trails
- Easier scaling across teams

## Features

### MCP Tools

| Tool | Description | Purpose |
|-------|-------------|---------|
| squad-tools-list | List all available squad tools | Discover what tools are available |
| squad-tool-execute | Execute a squad tool with arguments | Run any squad CLI tool |
| squad-knowledge-search | Search squad knowledge base | Find relevant squad information |
| squad-overview-full | Get complete squad overview | Check squad status, agents, productivity |

### Squad Tools Exposed

| Tool | Description |
|------|-------------|
| research-digest | Extract tweet drafts, blog angles, and key insights from squad research files |
| squad-eval | Evaluate squad agent performance with role-specific metrics |
| squad-overview | Get complete picture of squad status, learnings, and productivity |
| squad-meeting | Manage squad meetings with notes and action items |
| paper-summarizer | Summarize arXiv papers and articles with structured output |
| blog-assistant | Generate blog outlines in Run Data Run style |
| competitor-tracker | Track AI company product launches and features |
| gh-release-monitor | Monitor GitHub releases from multiple repositories |
| squad-knowledge | Manage squad project context, decisions, and conventions |
| squad-output-stats | Analyze agent output and productivity metrics |

### MCP Resources

| Resource | Description |
|----------|-------------|
| file://squad-tools-list | List of all squad tools |
| file://squad-knowledge | Squad knowledge summary and entry count |

### MCP Prompts

| Prompt | Description |
|--------|-------------|
| squad-summary-prompt | Generate a summary of squad activity and status |
| squad-coordination-prompt | Generate a coordination plan for squad operations |

## Installation

### Prerequisites

- Python 3.8+
- Claude Desktop or other MCP-compatible AI assistant
- Squad tools installed in `~/.openclaw/workspace/tools/`

### Install from Source

```bash
# Clone or copy to squad tools directory
cd /home/exedev/.openclaw/workspace/tools/squad-mcp-server

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 mcp_server.py --version
```

### Configure Claude Desktop

1. Open Claude Desktop
2. Go to Settings → Tools → MCP Servers
3. Click "Add Server"
4. Select "Local" or "Enter Server URL"
5. Use: `python3 /home/exedev/.openclaw/workspace/tools/squad-mcp-server/mcp_server.py`
6. Give it a name: "Squad Tools"
7. Save

Claude will now have access to all squad tools via MCP!

### Configure via MCP Registry (Alternative)

Add to MCP configuration:

```json
{
  "mcpServers": {
    "squad-tools": {
      "command": "python3",
      "args": ["/home/exedev/.openclaw/workspace/tools/squad-mcp-server/mcp_server.py"],
      "env": {}
    }
  }
}
```

## Usage Examples

### In Claude Desktop

After configuration, you can ask Claude to use squad tools:

```
You: List all available squad tools
Claude: [Calls squad-tools-list]

[Lists all 10 squad tools with descriptions]

You: Search squad knowledge for "dashboard"
Claude: [Calls squad-knowledge-search with query="dashboard"]

[Returns relevant knowledge entries about dashboard]

You: Get a complete squad overview
Claude: [Calls squad-overview-full]

[Returns squad status, agent activity, learnings, productivity]

You: Generate a squad summary
Claude: [Uses squad-summary-prompt]

[Comprehensive summary of squad activity, status, tools, knowledge]

You: Execute squad-eval
Claude: [Calls squad-tool-execute with tool_name="squad-eval"]

[Runs squad-eval and returns results]
```

### From Command Line

```bash
# List all tools
python3 mcp_server.py squad-tools-list

# Execute a tool
python3 mcp_server.py squad-tool-execute --tool research-digest

# Search knowledge
python3 mcp_server.py squad-knowledge-search --query "dashboard" --category "Architecture"

# Get squad overview
python3 mcp_server.py squad-overview-full
```

## Architecture

```
Claude Desktop (or other MCP-compatible AI)
    ↓
MCP Protocol (Model Context Protocol)
    ↓
Squad MCP Server
    ↓
Squad CLI Tools (research-digest, squad-eval, squad-overview, etc.)
    ↓
Squad Data (knowledge.db, learnings, outputs, etc.)
```

## Benefits

### For Squad Members

- **Direct AI Access**: Claude can use squad tools directly without manual intervention
- **Consistent Context**: Squad knowledge and conventions accessible to AI
- **Better Collaboration**: AI assistants can access squad capabilities
- **Standardized Protocol**: MCP is becoming the industry standard

### For AI Assistants

- **Tool Integration**: Access to 10+ squad tools
- **Knowledge Base**: Searchable squad knowledge database
- **Workflow Automation**: Execute complex multi-step tasks
- **Audit Trail**: All tool usage tracked via MCP

## Troubleshooting

### Tools Not Found

If tools show as "(not found)":
```bash
# Check if tools exist in expected location
ls -la /home/exedev/.openclaw/workspace/tools/

# Verify tool paths in mcp_server.py match your installation
```

### MCP Connection Issues

If Claude cannot connect to MCP server:
```bash
# Verify MCP server runs standalone
python3 /home/exedev/.openclaw/workspace/tools/squad-mcp-server/mcp_server.py

# Check Claude Desktop MCP configuration
# Settings → Tools → MCP Servers → Squad Tools
```

### Permission Errors

```bash
# Make sure tools are executable
chmod +x /home/exedev/.openclaw/workspace/tools/*/*.py

# Make MCP server executable
chmod +x mcp_server.py
```

## Development

### Add a New Squad Tool

1. Add tool to `SQUAD_TOOLS` dictionary in `mcp_server.py`:
```python
"tool-name": {
    "path": SQUAD_TOOLS_BASE / "tool-directory" / "tool.py",
    "description": "Tool description"
}
```

2. Restart MCP server
3. Tool automatically available to Claude

### Add a New MCP Tool

Create a new function decorated with `@mcp.tool()`:
```python
@mcp.tool()
def my_new_tool(param1: str, param2: int = 5) -> str:
    """Tool description for Claude."""
    # Your implementation
    return json.dumps({"result": "success"})
```

## Security Considerations

- Tools run with same permissions as the user running MCP server
- Knowledge database contains squad decisions (no secrets)
- All tool executions are logged by Claude
- Use environment variables for sensitive configuration

## License

MIT

## Author

Archimedes - OpenSeneca squad

---

**Expose your squad tools to AI assistants via MCP!**
