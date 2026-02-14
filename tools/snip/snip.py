#!/usr/bin/env python3
"""
snip - Simple snippet manager
Save, search, and retrieve code snippets with tags.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from difflib import get_close_matches

SNIP_FILE = Path.home() / ".snip" / "snippets.json"
EDITOR = os.environ.get("EDITOR", "vim")


def load_snippets():
    """Load snippets from file."""
    SNIP_FILE.parent.mkdir(parents=True, exist_ok=True)
    if SNIP_FILE.exists():
        with open(SNIP_FILE, "r") as f:
            return json.load(f)
    return {}


def save_snippets(snippets):
    """Save snippets to file."""
    SNIP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SNIP_FILE, "w") as f:
        json.dump(snippets, f, indent=2)


def add_snippet(name, content, tags=None, description=""):
    """Add a new snippet."""
    snippets = load_snippets()
    if name in snippets:
        print(f"❌ Snippet '{name}' already exists. Use --update to overwrite.")
        return False

    snippets[name] = {
        "content": content,
        "tags": tags or [],
        "description": description,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    save_snippets(snippets)
    print(f"✅ Saved snippet: {name}")
    return True


def update_snippet(name, content=None, tags=None, description=None):
    """Update an existing snippet."""
    snippets = load_snippets()
    if name not in snippets:
        print(f"❌ Snippet '{name}' not found.")
        return False

    if content:
        snippets[name]["content"] = content
    if tags is not None:
        snippets[name]["tags"] = tags
    if description is not None:
        snippets[name]["description"] = description
    snippets[name]["updated"] = datetime.now().isoformat()

    save_snippets(snippets)
    print(f"✅ Updated snippet: {name}")
    return True


def get_snippet(name):
    """Get a snippet by name."""
    snippets = load_snippets()
    if name not in snippets:
        # Try fuzzy matching
        matches = get_close_matches(name, list(snippets.keys()), n=3, cutoff=0.6)
        if matches:
            print(f"❌ Snippet '{name}' not found. Did you mean: {', '.join(matches)}?")
        else:
            print(f"❌ Snippet '{name}' not found.")
        return None

    snippet = snippets[name]
    print(f"\n📌 {name}")
    if snippet.get("description"):
        print(f"   {snippet['description']}")
    if snippet.get("tags"):
        print(f"   Tags: {', '.join(snippet['tags'])}")
    print("\n" + snippet["content"])
    return snippet


def search_snippets(query, tag=None):
    """Search snippets by content or tag."""
    snippets = load_snippets()
    results = []

    query = query.lower() if query else ""

    for name, data in snippets.items():
        if tag:
            # Filter by tag
            if tag.lower() in [t.lower() for t in data.get("tags", [])]:
                if not query or query in name.lower() or query in data.get("description", "").lower():
                    results.append((name, data))
        else:
            # Search by name, description, or content
            if query in name.lower() or query in data.get("description", "").lower() or query in data["content"].lower():
                results.append((name, data))

    if not results:
        print(f"❌ No results found.")
        return

    print(f"\n🔍 Found {len(results)} snippet(s):\n")
    for name, data in results:
        tags_str = f" [{', '.join(data['tags'])}]" if data.get("tags") else ""
        desc_str = f" - {data.get('description', '')}" if data.get("description") else ""
        print(f"  • {name}{tags_str}{desc_str}")


def list_snippets(tag=None):
    """List all snippets, optionally filtered by tag."""
    snippets = load_snippets()

    if tag:
        filtered = {k: v for k, v in snippets.items() if tag.lower() in [t.lower() for t in v.get("tags", [])]}
        snippets = filtered

    if not snippets:
        print("❌ No snippets found.")
        return

    print(f"\n📚 {len(snippets)} snippet(s):\n")
    for name, data in sorted(snippets.items()):
        tags_str = f" [{', '.join(data['tags'])}]" if data.get("tags") else ""
        desc_str = f" - {data.get('description', '')}" if data.get("description") else ""
        print(f"  • {name}{tags_str}{desc_str}")


def delete_snippet(name):
    """Delete a snippet."""
    snippets = load_snippets()
    if name not in snippets:
        print(f"❌ Snippet '{name}' not found.")
        return False

    del snippets[name]
    save_snippets(snippets)
    print(f"✅ Deleted snippet: {name}")
    return True


def edit_snippet(name):
    """Edit a snippet in $EDITOR."""
    snippets = load_snippets()
    if name not in snippets:
        print(f"❌ Snippet '{name}' not found.")
        return False

    # Create temp file with current content
    temp_file = Path(f"/tmp/snip_{name}.txt")
    temp_file.write_text(snippets[name]["content"])

    # Open editor
    os.system(f"{EDITOR} {temp_file}")

    # Read back and update
    new_content = temp_file.read_text()
    snippets[name]["content"] = new_content
    snippets[name]["updated"] = datetime.now().isoformat()
    save_snippets(snippets)
    temp_file.unlink()

    print(f"✅ Updated snippet: {name}")
    return True


def export_snippets(filepath):
    """Export all snippets to a JSON file."""
    snippets = load_snippets()
    export_path = Path(filepath)
    export_path.parent.mkdir(parents=True, exist_ok=True)
    export_path.write_text(json.dumps(snippets, indent=2))
    print(f"✅ Exported {len(snippets)} snippet(s) to {filepath}")


def import_snippets(filepath):
    """Import snippets from a JSON file."""
    import_path = Path(filepath)
    if not import_path.exists():
        print(f"❌ File not found: {filepath}")
        return False

    imported = json.loads(import_path.read_text())
    snippets = load_snippets()

    count = 0
    for name, data in imported.items():
        if name not in snippets:
            snippets[name] = data
            count += 1
        else:
            print(f"⚠️  Skipping '{name}' (already exists)")

    save_snippets(snippets)
    print(f"✅ Imported {count} snippet(s) from {filepath}")
    return True


def main():
    parser = argparse.ArgumentParser(description="snip - Simple snippet manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add
    add = subparsers.add_parser("add", help="Add a new snippet")
    add.add_argument("name", help="Snippet name")
    add.add_argument("content", nargs="?", help="Snippet content (or use -e to edit)")
    add.add_argument("-t", "--tags", nargs="+", help="Tags for this snippet")
    add.add_argument("-d", "--description", help="Short description")

    # Get
    get = subparsers.add_parser("get", help="Get a snippet")
    get.add_argument("name", help="Snippet name")

    # Update
    update = subparsers.add_parser("update", help="Update an existing snippet")
    update.add_argument("name", help="Snippet name")
    update.add_argument("-c", "--content", help="New content")
    update.add_argument("-t", "--tags", nargs="+", help="New tags")
    update.add_argument("-d", "--description", help="New description")

    # Search
    search = subparsers.add_parser("search", help="Search snippets")
    search.add_argument("query", nargs="?", help="Search query")
    search.add_argument("--tag", help="Filter by tag")

    # List
    list_cmd = subparsers.add_parser("list", help="List all snippets")
    list_cmd.add_argument("--tag", help="Filter by tag")

    # Delete
    delete = subparsers.add_parser("delete", help="Delete a snippet")
    delete.add_argument("name", help="Snippet name")

    # Edit
    edit = subparsers.add_parser("edit", help="Edit snippet in $EDITOR")
    edit.add_argument("name", help="Snippet name")

    # Export/Import
    export = subparsers.add_parser("export", help="Export snippets to file")
    export.add_argument("filepath", help="Output file path")

    import_cmd = subparsers.add_parser("import", help="Import snippets from file")
    import_cmd.add_argument("filepath", help="Input file path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "add":
        if not args.content:
            print("❌ Content required. Use snip edit to add interactively.")
            return
        add_snippet(args.name, args.content, args.tags, args.description)
    elif args.command == "get":
        get_snippet(args.name)
    elif args.command == "update":
        update_snippet(args.name, args.content, args.tags, args.description)
    elif args.command == "search":
        search_snippets(args.query, args.tag)
    elif args.command == "list":
        list_snippets(args.tag)
    elif args.command == "delete":
        delete_snippet(args.name)
    elif args.command == "edit":
        edit_snippet(args.name)
    elif args.command == "export":
        export_snippets(args.filepath)
    elif args.command == "import":
        import_snippets(args.filepath)


if __name__ == "__main__":
    main()
