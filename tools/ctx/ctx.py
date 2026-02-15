#!/usr/bin/env python3
"""
ctx - AI Context Manager
Manage context, sessions, and knowledge for AI agent workflows
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

# Constants
CTX_DIR = Path.home() / ".ctx"
SESSIONS_FILE = CTX_DIR / "sessions.json"
KNOWLEDGE_FILE = CTX_DIR / "knowledge.json"
TEMPLATE_FILE = CTX_DIR / "templates.json"

def init():
    """Initialize ctx directory structure"""
    CTX_DIR.mkdir(parents=True, exist_ok=True)
    if not SESSIONS_FILE.exists():
        SESSIONS_FILE.write_text(json.dumps({}, indent=2))
    if not KNOWLEDGE_FILE.exists():
        KNOWLEDGE_FILE.write_text(json.dumps({}, indent=2))
    if not TEMPLATE_FILE.exists():
        TEMPLATE_FILE.write_text(json.dumps({
            "default": {
                "name": "default",
                "context": "You are a helpful AI assistant",
                "tools": ["web_search", "file_read", "file_write"],
                "rules": ["Be concise", "Provide code examples"]
            }
        }, indent=2))
    print(f"✅ Initialized ctx directory: {CTX_DIR}")

def create_session(name: str, description: str = "", template: Optional[str] = None):
    """Create a new AI session with context"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if name in sessions:
        print(f"❌ Session '{name}' already exists")
        sys.exit(1)

    # Load template if specified
    context_data = {}
    if template:
        templates = json.loads(TEMPLATE_FILE.read_text())
        if template not in templates:
            print(f"❌ Template '{template}' not found")
            sys.exit(1)
        context_data = templates[template].copy()

    # Create session
    sessions[name] = {
        "description": description or f"Session: {name}",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "context": context_data.get("context", ""),
        "tools": context_data.get("tools", []),
        "rules": context_data.get("rules", []),
        "history": [],
        "knowledge": [],
        "active": True
    }
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2))

    print(f"✅ Created session: {name}")
    print(f"📝 {description or 'No description'}")
    print(f"📅 Created: {sessions[name]['created']}")

def list_sessions(show_all: bool = False):
    """List all AI sessions"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if not sessions:
        print("📭 No sessions found. Create one with: ctx create <name>")
        return

    active_sessions = {k: v for k, v in sessions.items() if v.get("active", False)}
    archived_sessions = {k: v for k, v in sessions.items() if not v.get("active", False)}

    if active_sessions:
        print(f"🟢 Active Sessions ({len(active_sessions)}):")
        print()
        for name, session in active_sessions.items():
            print(f"  • {name}")
            print(f"    {session.get('description', 'No description')}")
            print(f"    Updated: {session['updated']}")
            if session.get('context'):
                print(f"    Context: {session['context'][:50]}...")
            print()

    if archived_sessions and show_all:
        print(f"⚪ Archived Sessions ({len(archived_sessions)}):")
        print()
        for name, session in archived_sessions.items():
            print(f"  • {name}")
            print(f"    Updated: {session['updated']}")
            print()

def show_session(name: str):
    """Show session details"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if name not in sessions:
        print(f"❌ Session '{name}' not found")
        sys.exit(1)

    session = sessions[name]

    print(f"📋 Session: {name}")
    print(f"📝 {session['description']}")
    print(f"📅 Created: {session['created']}")
    print(f"🔄 Updated: {session['updated']}")
    print(f"🟢 Status: {'Active' if session['active'] else 'Archived'}")
    print()

    if session.get('context'):
        print("🧠 Context:")
        print(f"   {session['context']}")
        print()

    if session.get('tools'):
        print("🛠️  Available Tools:")
        for tool in session['tools']:
            print(f"   • {tool}")
        print()

    if session.get('rules'):
        print("📜 Rules:")
        for rule in session['rules']:
            print(f"   • {rule}")
        print()

    if session.get('history'):
        print(f"📜 History ({len(session['history'])} entries):")
        for i, entry in enumerate(session['history'][-5:], 1):
            timestamp = entry.get('timestamp', 'Unknown')
            message = entry.get('message', '')[:50]
            print(f"   {i}. [{timestamp}] {message}...")
        print()

    if session.get('knowledge'):
        print(f"📚 Knowledge Base ({len(session['knowledge'])} items):")
        for item in session['knowledge'][-5:]:
            title = item.get('title', 'Unknown')
            print(f"   • {title}")
        print()

def update_session(name: str, context: Optional[str] = None, add_tool: Optional[str] = None,
                add_rule: Optional[str] = None, description: Optional[str] = None):
    """Update session context or metadata"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if name not in sessions:
        print(f"❌ Session '{name}' not found")
        sys.exit(1)

    session = sessions[name]

    if context:
        session['context'] = context
        print(f"✅ Updated context for '{name}'")

    if add_tool:
        if 'tools' not in session:
            session['tools'] = []
        if add_tool not in session['tools']:
            session['tools'].append(add_tool)
            print(f"✅ Added tool '{add_tool}' to '{name}'")
        else:
            print(f"⚠️  Tool '{add_tool}' already in session")

    if add_rule:
        if 'rules' not in session:
            session['rules'] = []
        if add_rule not in session['rules']:
            session['rules'].append(add_rule)
            print(f"✅ Added rule '{add_rule}' to '{name}'")
        else:
            print(f"⚠️  Rule '{add_rule}' already in session")

    if description:
        session['description'] = description
        print(f"✅ Updated description for '{name}'")

    session['updated'] = datetime.now().isoformat()
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2))

def archive_session(name: str):
    """Archive a session (set to inactive)"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if name not in sessions:
        print(f"❌ Session '{name}' not found")
        sys.exit(1)

    sessions[name]['active'] = False
    sessions[name]['updated'] = datetime.now().isoformat()
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2))

    print(f"📦 Archived session: {name}")

def activate_session(name: str):
    """Activate an archived session"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if name not in sessions:
        print(f"❌ Session '{name}' not found")
        sys.exit(1)

    sessions[name]['active'] = True
    sessions[name]['updated'] = datetime.now().isoformat()
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2))

    print(f"✅ Activated session: {name}")

def export_session(name: str, output: Optional[str] = None):
    """Export session context to file or stdout"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if name not in sessions:
        print(f"❌ Session '{name}' not found")
        sys.exit(1)

    session = sessions[name]

    # Format as context prompt
    context_text = f"""# Context for {name}

## Description
{session['description']}

## System Context
{session.get('context', 'No system context defined')}

## Available Tools
{', '.join(session.get('tools', ['None']))}

## Rules
{chr(10).join(f"- {rule}" for rule in session.get('rules', ['None']))}

## Session History ({len(session.get('history', []))} entries)
{chr(10).join(f"- {h.get('timestamp', 'Unknown')}: {h.get('message', '')}" for h in session.get('history', []))}

## Knowledge Base ({len(session.get('knowledge', []))} items)
{chr(10).join(f"- {k.get('title', '')}: {k.get('content', '')[:50]}..." for k in session.get('knowledge', []))}
"""

    if output:
        Path(output).write_text(context_text)
        print(f"✅ Exported session to: {output}")
    else:
        print(context_text)

def add_knowledge(name: str, title: str, content: str, tags: Optional[List[str]] = None):
    """Add knowledge to a session"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if name not in sessions:
        print(f"❌ Session '{name}' not found")
        sys.exit(1)

    if 'knowledge' not in sessions[name]:
        sessions[name]['knowledge'] = []

    sessions[name]['knowledge'].append({
        "title": title,
        "content": content,
        "tags": tags or [],
        "added": datetime.now().isoformat()
    })

    sessions[name]['updated'] = datetime.now().isoformat()
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2))

    print(f"✅ Added knowledge '{title}' to session '{name}'")

def delete_session(name: str):
    """Delete a session"""
    if not SESSIONS_FILE.exists():
        init()

    sessions = json.loads(SESSIONS_FILE.read_text())

    if name not in sessions:
        print(f"❌ Session '{name}' not found")
        sys.exit(1)

    del sessions[name]
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2))

    print(f"🗑️  Deleted session: {name}")

def main():
    parser = argparse.ArgumentParser(
        description="ctx - AI Context Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ctx init                    Initialize ctx directory
  ctx create my-session        Create a new session
  ctx create dev -t default   Create from template
  ctx list                    List active sessions
  ctx list --all              List all sessions
  ctx show my-session          Show session details
  ctx update my-session -c "You are a Python expert"
  ctx update my-session --add-tool web_search
  ctx archive my-session       Archive session
  ctx activate my-session      Activate archived session
  ctx export my-session        Export context to stdout
  ctx export my-session -o context.txt
  ctx delete my-session       Delete session
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    subparsers.add_parser("init", help="Initialize ctx directory")

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new session")
    create_parser.add_argument("name", help="Session name")
    create_parser.add_argument("-d", "--description", help="Session description")
    create_parser.add_argument("-t", "--template", help="Use template")

    # list command
    list_parser = subparsers.add_parser("list", help="List sessions")
    list_parser.add_argument("--all", action="store_true", help="Show archived sessions")

    # show command
    show_parser = subparsers.add_parser("show", help="Show session details")
    show_parser.add_argument("name", help="Session name")

    # update command
    update_parser = subparsers.add_parser("update", help="Update session")
    update_parser.add_argument("name", help="Session name")
    update_parser.add_argument("-c", "--context", help="Set system context")
    update_parser.add_argument("--add-tool", help="Add available tool")
    update_parser.add_argument("--add-rule", help="Add rule")
    update_parser.add_argument("-d", "--description", help="Update description")

    # archive command
    archive_parser = subparsers.add_parser("archive", help="Archive session")
    archive_parser.add_argument("name", help="Session name")

    # activate command
    activate_parser = subparsers.add_parser("activate", help="Activate session")
    activate_parser.add_argument("name", help="Session name")

    # export command
    export_parser = subparsers.add_parser("export", help="Export session")
    export_parser.add_argument("name", help="Session name")
    export_parser.add_argument("-o", "--output", help="Output file")

    # knowledge command
    knowledge_parser = subparsers.add_parser("add-knowledge", help="Add knowledge to session")
    knowledge_parser.add_argument("name", help="Session name")
    knowledge_parser.add_argument("title", help="Knowledge title")
    knowledge_parser.add_argument("content", help="Knowledge content")
    knowledge_parser.add_argument("-t", "--tags", nargs="*", help="Tags")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete session")
    delete_parser.add_argument("name", help="Session name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == "init":
        init()
    elif args.command == "create":
        create_session(args.name, args.description, args.template)
    elif args.command == "list":
        list_sessions(args.all)
    elif args.command == "show":
        show_session(args.name)
    elif args.command == "update":
        update_session(args.name, args.context, args.add_tool, args.add_rule, args.description)
    elif args.command == "archive":
        archive_session(args.name)
    elif args.command == "activate":
        activate_session(args.name)
    elif args.command == "export":
        export_session(args.name, args.output)
    elif args.command == "add-knowledge":
        add_knowledge(args.name, args.title, args.content, args.tags)
    elif args.command == "delete":
        delete_session(args.name)

if __name__ == "__main__":
    main()
