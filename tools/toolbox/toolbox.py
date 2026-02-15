#!/usr/bin/env python3
"""
toolbox - OpenClaw CLI Tool Manager
Overview and manage all OpenClaw CLI tools
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List

# Tool definitions
TOOLS = {
    "prj": {
        "name": "Project Scaffolding",
        "location": "~/workspace/tools/prj",
        "description": "Create new projects with best-practice structure",
        "commands": ["init", "types", "create", "list"],
        "key_command": "create",
        "example": "prj create my-project -t python"
    },
    "agt": {
        "name": "Agent Scaffolding",
        "location": "~/workspace/tools/agt",
        "description": "Create new AI agent projects",
        "commands": ["init", "templates", "create", "list"],
        "key_command": "create",
        "example": "agt create my-agent -t research"
    },
    "snip": {
        "name": "Snippet Manager",
        "location": "~/workspace/tools/snip",
        "description": "Save and retrieve code snippets with tags",
        "commands": ["add", "get", "search", "list", "edit"],
        "key_command": "add",
        "example": "snip add my-snippet 'code here' -t python"
    },
    "tick": {
        "name": "Task Tracker",
        "location": "~/workspace/tools/tick",
        "description": "Track tasks and priorities",
        "commands": ["add", "list", "done", "undo", "stats", "clear"],
        "key_command": "add",
        "example": "tick add 'Fix bug' -p high"
    },
    "crw": {
        "name": "CrewAI Workflow Manager",
        "location": "~/workspace/tools/crw",
        "description": "Create and manage AI agent crews",
        "commands": ["init", "create", "list", "show", "run", "delete"],
        "key_command": "create",
        "example": "crw create research-team -d 'Research crew'"
    },
    "flow": {
        "name": "Workflow Orchestrator",
        "location": "~/workspace/tools/flow",
        "description": "Orchestrate multi-stage development workflows",
        "commands": ["init", "create", "list", "show", "run", "delete"],
        "key_command": "create",
        "example": "flow create project-setup -d 'Quick start'"
    },
    "ctx": {
        "name": "AI Context Manager",
        "location": "~/workspace/tools/ctx",
        "description": "Manage AI agent contexts and sessions",
        "commands": ["init", "create", "list", "show", "update", "archive", "activate", "export", "delete"],
        "key_command": "create",
        "example": "ctx create python-dev -d 'Python help'"
    },
    "crew": {
        "name": "CrewAI Execution Engine",
        "location": "~/workspace/tools/crew",
        "description": "Execute and manage AI crews",
        "commands": ["list", "simulate", "run", "validate", "export"],
        "key_command": "simulate",
        "example": "crew simulate research-team"
    }
}

def check_tool_status(tool_id: str) -> str:
    """Check if tool is installed and working"""
    try:
        result = subprocess.run(
            [tool_id, "--help"],
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            return "✅ Installed"
        else:
            return "⚠️ Error"
    except FileNotFoundError:
        return "❌ Not installed"
    except Exception:
        return "⚠️ Unknown"

def list_tools(verbose: bool = False):
    """List all available tools"""
    print(f"🧰 OpenClaw CLI Toolbox - {len(TOOLS)} tools\n")

    for tool_id, info in TOOLS.items():
        status = check_tool_status(tool_id)
        print(f"{status} {tool_id} — {info['name']}")
        if verbose:
            print(f"   📍 Location: {info['location']}")
            print(f"   📝 {info['description']}")
            print(f"   🛠️  Commands: {', '.join(info['commands'])}")
            print()

def show_tool(tool_id: str):
    """Show detailed information about a tool"""
    if tool_id not in TOOLS:
        print(f"❌ Tool '{tool_id}' not found")
        sys.exit(1)

    info = TOOLS[tool_id]
    status = check_tool_status(tool_id)

    print(f"📦 Tool: {tool_id}")
    print(f"📝 Name: {info['name']}")
    print(f"📍 Location: {info['location']}")
    print(f"✅ Status: {status}")
    print()
    print("📄 Description:")
    print(f"   {info['description']}")
    print()
    print("🛠️  Available Commands:")
    for cmd in info['commands']:
        print(f"   • {cmd}")
    print()
    print("💡 Example Usage:")
    print(f"   {info['example']}")
    print()
    print("📖 Documentation:")
    readme_path = Path.home() / ".openclaw" / "workspace" / "tools" / tool_id / "README.md"
    if readme_path.exists():
        print(f"   {readme_path}")
    else:
        print(f"   README not found")

def search_tools(query: str):
    """Search for tools matching query"""
    query_lower = query.lower()
    matches = []

    for tool_id, info in TOOLS.items():
        if (query_lower in tool_id.lower() or
            query_lower in info['name'].lower() or
            query_lower in info['description'].lower()):
            matches.append(tool_id)

    if not matches:
        print(f"❌ No tools found matching '{query}'")
        return

    print(f"🔍 Found {len(matches)} tool(s) matching '{query}':\n")
    for tool_id in matches:
        info = TOOLS[tool_id]
        status = check_tool_status(tool_id)
        print(f"{status} {tool_id} — {info['name']}")
        print(f"   {info['description']}")
        print()

def workflow_examples():
    """Show common workflow examples"""
    print("🔄 Common Workflows\n")

    workflows = [
        {
            "name": "New Project Setup",
            "description": "Start a new Python project with agents and tasks",
            "steps": [
                "prj create my-api -t python",
                "agt create api-agent -t code",
                "crw create api-crew -d 'API development'",
                "ctx create python-dev -d 'Python API context'",
                "tick add 'Setup project structure' -p high"
            ]
        },
        {
            "name": "Research Workflow",
            "description": "Set up research agents and context",
            "steps": [
                "crw create research-team -d 'Research and writing'",
                "crew simulate research-team",
                "ctx create researcher -d 'AI research agent'",
                "snip add research-note 'Findings here' -t research"
            ]
        },
        {
            "name": "Development Pipeline",
            "description": "Multi-stage workflow for production code",
            "steps": [
                "flow create dev-pipeline -d 'Full dev workflow'",
                "flow run dev-pipeline --dry-run",
                "tick add 'Implement features' -p high",
                "snip add debug-tip 'How to debug' -t debugging"
            ]
        }
    ]

    for i, workflow in enumerate(workflows, 1):
        print(f"{i}. {workflow['name']}")
        print(f"   {workflow['description']}")
        print(f"   Commands:")
        for step in workflow['steps']:
            print(f"     • {step}")
        print()

def stats():
    """Show statistics about tools"""
    print("📊 Toolbox Statistics\n")

    total = len(TOOLS)
    installed = 0
    broken = 0

    for tool_id in TOOLS:
        status = check_tool_status(tool_id)
        if "Installed" in status:
            installed += 1
        elif "Not installed" in status:
            broken += 1

    print(f"📦 Total Tools: {total}")
    print(f"✅ Installed: {installed}")
    print(f"❌ Not Found: {broken}")
    print(f"📈 Coverage: {(installed/total)*100:.0f}%")
    print()

    print("🛠️  Commands Distribution:")
    total_commands = sum(len(info['commands']) for info in TOOLS.values())
    print(f"   Total Commands: {total_commands}")
    print(f"   Average per Tool: {total_commands/total:.1f}")

def main():
    parser = argparse.ArgumentParser(
        description="toolbox - OpenClaw CLI Tool Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  toolbox list -v            List all tools with details
  toolbox show prj            Show details about prj tool
  toolbox search research      Search for research-related tools
  toolbox workflows           Show common workflow examples
  toolbox stats               Show toolbox statistics
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    list_parser = subparsers.add_parser("list", help="List all tools")
    list_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # show command
    show_parser = subparsers.add_parser("show", help="Show tool details")
    show_parser.add_argument("tool", help="Tool name")

    # search command
    search_parser = subparsers.add_parser("search", help="Search for tools")
    search_parser.add_argument("query", help="Search query")

    # workflows command
    subparsers.add_parser("workflows", help="Show workflow examples")

    # stats command
    subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == "list":
        list_tools(getattr(args, 'verbose', False))
    elif args.command == "show":
        show_tool(args.tool)
    elif args.command == "search":
        search_tools(args.query)
    elif args.command == "workflows":
        workflow_examples()
    elif args.command == "stats":
        stats()

if __name__ == "__main__":
    main()
