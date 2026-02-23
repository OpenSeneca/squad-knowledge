#!/usr/bin/env python3
"""
Squad MCP Server - Expose Squad Tools via Model Context Protocol

This MCP server exposes squad CLI tools as MCP tools, enabling Claude, 
Codex, Gemini CLI, and other AI assistants to access squad 
capabilities directly.

Based on FastMCP (https://github.com/jlowin/fastmcp)
"""

from typing import Any
from mcp.server.fastmcp import FastMCP
import subprocess
import json
from pathlib import Path
import sys

# Create MCP server
mcp = FastMCP("Squad Tools")

# Squad tools directory
SQUAD_TOOLS_BASE = Path("/home/exedev/.openclaw/workspace/tools")

# Available squad tools
SQUAD_TOOLS = {
    "research-digest": {
        "path": SQUAD_TOOLS_BASE / "research-digest" / "research_digest.py",
        "description": "Extract tweet drafts, blog angles, and key insights from squad research files"
    },
    "squad-eval": {
        "path": SQUAD_TOOLS_BASE / "squad-eval" / "squad_eval.py",
        "description": "Evaluate squad agent performance with role-specific metrics"
    },
    "squad-overview": {
        "path": SQUAD_TOOLS_BASE / "squad-overview" / "squad_overview.py",
        "description": "Get complete picture of squad status, learnings, and productivity"
    },
    "squad-meeting": {
        "path": SQUAD_TOOLS_BASE / "squad-meeting" / "squad_meeting.py",
        "description": "Manage squad meetings with notes and action items"
    },
    "paper-summarizer": {
        "path": SQUAD_TOOLS_BASE / "paper-summarizer" / "paper_summarizer.py",
        "description": "Summarize arXiv papers and articles with structured output"
    },
    "blog-assistant": {
        "path": SQUAD_TOOLS_BASE / "blog-assistant" / "blog_assistant.py",
        "description": "Generate blog outlines in Run Data Run style"
    },
    "competitor-tracker": {
        "path": SQUAD_TOOLS_BASE / "competitor-tracker" / "competitor_tracker.py",
        "description": "Track AI company product launches and features"
    },
    "gh-release-monitor": {
        "path": SQUAD_TOOLS_BASE / "gh-release-monitor" / "gh_release_monitor.py",
        "description": "Monitor GitHub releases from multiple repositories"
    },
    "squad-knowledge": {
        "path": SQUAD_TOOLS_BASE / "squad-knowledge" / "squad_knowledge.py",
        "description": "Manage squad project context, decisions, and conventions"
    },
    "squad-output-stats": {
        "path": SQUAD_TOOLS_BASE / "squad-output-stats" / "squad_output_stats.py",
        "description": "Analyze agent output and productivity metrics"
    }
}


def run_tool(tool_name: str, args: list = None) -> dict:
    """Run a squad tool and return the output."""
    if tool_name not in SQUAD_TOOLS:
        return {
            "error": f"Tool '{tool_name}' not found",
            "available_tools": list(SQUAD_TOOLS.keys())
        }
    
    tool_info = SQUAD_TOOLS[tool_name]
    tool_path = tool_info["path"]
    
    if not tool_path.exists():
        return {
            "error": f"Tool path not found: {tool_path}",
            "description": tool_info["description"]
        }
    
    try:
        # Build command
        cmd = [sys.executable, str(tool_path)]
        
        # Add arguments
        if args:
            cmd.extend(args)
        
        # Run tool
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(tool_path.parent)
        )
        
        return {
            "tool": tool_name,
            "description": tool_info["description"],
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "error": "Tool execution timed out (60s limit)",
            "tool": tool_name
        }
    except Exception as e:
        return {
            "error": f"Tool execution failed: {str(e)}",
            "tool": tool_name
        }


# Register MCP tools


@mcp.tool()
def squad_tools_list() -> str:
    """List all available squad tools."""
    tools_info = []
    for name, info in SQUAD_TOOLS.items():
        exists = " (installed)" if info["path"].exists() else " (not found)"
        tools_info.append({
            "name": name,
            "description": info["description"],
            "status": exists
        })
    
    return json.dumps(tools_info, indent=2)


@mcp.tool()
def squad_tool_execute(tool_name: str, args: str = "") -> str:
    """Execute a squad tool with optional arguments."""
    result = run_tool(tool_name, args.split() if args else None)
    return json.dumps(result, indent=2)


@mcp.tool()
def squad_knowledge_search(query: str, category: str = "") -> str:
    """Search squad knowledge base for relevant information."""
    knowledge_path = SQUAD_TOOLS_BASE / "squad-knowledge" / "knowledge.db"
    
    if not knowledge_path.exists():
        return json.dumps({"error": "Squad knowledge database not found"})
    
    try:
        # Use squad-knowledge CLI to search
        cmd = [sys.executable, str(SQUAD_TOOLS_BASE / "squad-knowledge" / "squad_knowledge.py")]
        cmd.extend(["search", "--database", str(knowledge_path), "--query", query])
        
        if category:
            cmd.extend(["--category", category])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result.stdout
    except Exception as e:
        return json.dumps({"error": f"Knowledge search failed: {str(e)}"})


@mcp.tool()
def squad_overview_full() -> str:
    """Get complete squad overview including agents, learnings, and productivity."""
    overview_path = SQUAD_TOOLS_BASE / "squad-overview" / "squad_overview.py"
    
    if not overview_path.exists():
        return json.dumps({"error": "Squad overview tool not found"})
    
    try:
        result = subprocess.run(
            [sys.executable, str(overview_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result.stdout
    except Exception as e:
        return json.dumps({"error": f"Overview failed: {str(e)}"})


# Register MCP resources


@mcp.resource("file://squad-tools-list")
def get_squad_tools_list() -> str:
    """Get list of all squad tools as a resource."""
    return squad_tools_list()


@mcp.resource("file://squad-knowledge")
def get_squad_knowledge_summary() -> str:
    """Get squad knowledge summary as a resource."""
    # Count knowledge entries
    knowledge_path = SQUAD_TOOLS_BASE / "squad-knowledge" / "knowledge.db"
    
    if knowledge_path.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(knowledge_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM knowledge")
            count = cursor.fetchone()[0]
            conn.close()
            
            return json.dumps({
                "total_entries": count,
                "database_path": str(knowledge_path)
            })
        except Exception as e:
            return json.dumps({"error": f"Failed to read knowledge database: {str(e)}"})
    
    return json.dumps({
        "total_entries": 0,
        "database_path": str(knowledge_path)
    })


# Register MCP prompts


@mcp.prompt()
def squad_summary_prompt() -> str:
    """Generate a summary of squad activity and status."""
    return """Use the squad-overview tool to get a complete picture of squad status. Then use squad-knowledge-search to find relevant information about recent decisions and conventions. Finally, use squad-tools-list to see all available squad tools.

Generate a concise summary covering:
1. Agent status and activity
2. Recent learnings and research
3. Key decisions and conventions
4. Available tools and their purposes
5. Any blockers or issues requiring attention"""


@mcp.prompt()
def squad_coordination_prompt() -> str:
    """Generate a coordination plan for squad operations."""
    return """Use squad tools to coordinate squad operations:

1. Use squad-overview to check current agent status
2. Use squad-knowledge-search to find relevant conventions for the task
3. Use squad-tool-execute to run appropriate tools:
   - research-digest: Extract content from research files
   - squad-meeting: Manage meetings and action items
   - squad-eval: Evaluate agent performance
   - squad-output-stats: Analyze productivity

Generate a coordination plan with:
- Current status check
- Relevant knowledge lookup
- Tools to execute
- Expected outcomes
- Follow-up actions"""


def main():
    """Start the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
