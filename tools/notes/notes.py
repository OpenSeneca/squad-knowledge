#!/usr/bin/env python3
"""
notes — Quick Note Taking Tool

Take notes with timestamps, tags, and categories. Search and organize easily.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class NotesManager:
    """Quick note taking and management."""

    def __init__(self):
        self.notes_dir = Path.home() / '.notes'
        self.notes_file = self.notes_dir / 'notes.json'
        self.categories_file = self.notes_dir / 'categories.json'

        self._ensure_config()

    def _ensure_config(self):
        """Ensure notes directory and files exist."""
        self.notes_dir.mkdir(parents=True, exist_ok=True)

        if not self.notes_file.exists():
            with open(self.notes_file, 'w') as f:
                json.dump([], f)

        if not self.categories_file.exists():
            default_categories = {
                'general': 'General notes and thoughts',
                'idea': 'Ideas and brainstorms',
                'task': 'Task reminders and TODOs',
                'meeting': 'Meeting notes',
                'learning': 'Learning and discoveries',
                'debug': 'Debugging notes and solutions'
            }
            with open(self.categories_file, 'w') as f:
                json.dump(default_categories, f, indent=2)

    def _read_notes(self) -> List[Dict]:
        """Read notes from storage."""
        try:
            with open(self.notes_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_notes(self, notes: List[Dict]):
        """Write notes to storage."""
        with open(self.notes_file, 'w') as f:
            json.dump(notes, f, indent=2)

    def _read_categories(self) -> Dict:
        """Read categories."""
        try:
            with open(self.categories_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_categories(self, categories: Dict):
        """Write categories."""
        with open(self.categories_file, 'w') as f:
            json.dump(categories, f, indent=2)

    def add(self, text: str, category: str = None, tags: List[str] = None, priority: str = None):
        """Add a new note."""
        notes = self._read_notes()
        categories = self._read_categories()

        # Default to general category
        if not category:
            category = 'general'
        elif category not in categories:
            print(f"⚠️  Category '{category}' doesn't exist. Using 'general'")
            category = 'general'

        # Priority levels: low, medium (default), high, urgent
        if not priority:
            priority = 'medium'
        elif priority not in ['low', 'medium', 'high', 'urgent']:
            print(f"⚠️  Invalid priority '{priority}'. Using 'medium'")
            priority = 'medium'

        # Create note
        note = {
            'id': len(notes) + 1,
            'text': text,
            'category': category,
            'tags': tags or [],
            'priority': priority,
            'created': datetime.now().isoformat(),
            'completed': False
        }

        notes.insert(0, note)  # Add to beginning

        self._write_notes(notes)

        # Show confirmation
        priority_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴', 'urgent': '🚨'}
        tags_str = ' '.join([f'#{t}' for t in note['tags']]) if note['tags'] else ''

        print(f"✅ Note added (#{note['id']})")
        if priority != 'medium':
            print(f"   Priority: {priority_emoji.get(priority, '')} {priority}")
        if tags_str:
            print(f"   Tags: {tags_str}")
        print(f"   Category: {category}")

        return True

    def list(self, category: str = None, tags: List[str] = None,
             priority: str = None, incomplete_only: bool = False,
             limit: int = None):
        """List notes with optional filtering."""
        notes = self._read_notes()

        # Filter notes
        filtered = []
        for note in notes:
            # Category filter
            if category and note['category'] != category:
                continue

            # Tags filter (AND logic - all tags must match)
            if tags and not all(tag in note['tags'] for tag in tags):
                continue

            # Priority filter
            if priority and note['priority'] != priority:
                continue

            # Incomplete only
            if incomplete_only and note['completed']:
                continue

            filtered.append(note)

        # Limit results
        if limit:
            filtered = filtered[:limit]

        if not filtered:
            print("📝 No notes found")
            return

        # Display notes
        print(f"📝 {len(filtered)} note(s):")
        print()

        for note in filtered:
            self._print_note(note)
            print()

    def _print_note(self, note: Dict):
        """Print a single note."""
        priority_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴', 'urgent': '🚨'}
        completed_mark = '✓' if note['completed'] else '○'

        # Header
        timestamp = self._format_time(note['created'])
        tags_str = ' '.join([f'#{t}' for t in note['tags']]) if note['tags'] else ''

        print(f"  {completed_mark} #{note['id']} {note['category'].upper()}")

        # Meta line
        meta_parts = []
        meta_parts.append(timestamp)
        if note['priority'] != 'medium':
            meta_parts.append(f"{priority_emoji.get(note['priority'])} {note['priority']}")
        if tags_str:
            meta_parts.append(tags_str)
        print(f"     {' | '.join(meta_parts)}")

        # Note text
        print(f"     {note['text']}")

    def show(self, note_id: int):
        """Show detailed note."""
        notes = self._read_notes()

        for note in notes:
            if note['id'] == note_id:
                print(f"📝 Note #{note['id']}")
                print()

                # Meta
                print(f"  Category: {note['category']}")
                print(f"  Priority: {note['priority']}")
                print(f"  Tags: {', '.join(note['tags']) or 'None'}")
                print(f"  Created: {note['created']}")
                print(f"  Status: {'Completed' if note['completed'] else 'Incomplete'}")
                print()

                # Text
                print(f"  {note['text']}")
                return True

        print(f"❌ Note #{note_id} not found")
        return False

    def edit(self, note_id: int, text: str = None, category: str = None,
              tags: List[str] = None, priority: str = None):
        """Edit a note."""
        notes = self._read_notes()
        categories = self._read_categories()

        for note in notes:
            if note['id'] == note_id:
                # Update fields
                if text:
                    note['text'] = text
                if category:
                    if category not in categories:
                        print(f"⚠️  Category '{category}' doesn't exist")
                        return False
                    note['category'] = category
                if tags is not None:
                    note['tags'] = tags
                if priority:
                    if priority not in ['low', 'medium', 'high', 'urgent']:
                        print(f"⚠️  Invalid priority '{priority}'")
                        return False
                    note['priority'] = priority

                # Update timestamp
                note['updated'] = datetime.now().isoformat()

                self._write_notes(notes)
                print(f"✅ Updated note #{note_id}")
                return True

        print(f"❌ Note #{note_id} not found")
        return False

    def complete(self, note_id: int):
        """Mark note as completed."""
        notes = self._read_notes()

        for note in notes:
            if note['id'] == note_id:
                note['completed'] = True
                note['completed_at'] = datetime.now().isoformat()

                self._write_notes(notes)
                print(f"✅ Completed note #{note_id}")
                return True

        print(f"❌ Note #{note_id} not found")
        return False

    def uncomplete(self, note_id: int):
        """Mark note as incomplete."""
        notes = self._read_notes()

        for note in notes:
            if note['id'] == note_id:
                note['completed'] = False
                if 'completed_at' in note:
                    del note['completed_at']

                self._write_notes(notes)
                print(f"✅ Uncompleted note #{note_id}")
                return True

        print(f"❌ Note #{note_id} not found")
        return False

    def delete(self, note_id: int):
        """Delete a note."""
        notes = self._read_notes()

        for i, note in enumerate(notes):
            if note['id'] == note_id:
                del notes[i]

                self._write_notes(notes)
                print(f"✅ Deleted note #{note_id}")
                return True

        print(f"❌ Note #{note_id} not found")
        return False

    def search(self, query: str):
        """Search notes by text."""
        notes = self._read_notes()
        query = query.lower()

        # Search
        results = []
        for note in notes:
            if (query in note['text'].lower() or
                query in note['category'].lower() or
                any(query in tag.lower() for tag in note['tags'])):
                results.append(note)

        if not results:
            print(f"🔍 No results for '{query}'")
            return

        print(f"🔍 {len(results)} result(s) for '{query}':")
        print()

        for note in results:
            self._print_note(note)
            print()

    def categories(self):
        """List all categories."""
        categories = self._read_categories()

        print("📁 Categories:")
        print()

        for name, description in sorted(categories.items()):
            # Count notes in category
            notes = self._read_notes()
            count = sum(1 for n in notes if n['category'] == name)

            print(f"  • {name}: {description} ({count} notes)")

    def stats(self):
        """Show note statistics."""
        notes = self._read_notes()

        total = len(notes)
        completed = sum(1 for n in notes if n['completed'])
        incomplete = total - completed

        # By category
        by_category = {}
        for note in notes:
            cat = note['category']
            by_category[cat] = by_category.get(cat, 0) + 1

        # By priority
        by_priority = {}
        for note in notes:
            pri = note['priority']
            by_priority[pri] = by_priority.get(pri, 0) + 1

        print("📊 Note Statistics")
        print()
        print(f"  Total: {total}")
        print(f"  Completed: {completed}")
        print(f"  Incomplete: {incomplete}")
        print()
        print(f"  By Category:")
        for cat, count in sorted(by_category.items()):
            print(f"    • {cat}: {count}")
        print()
        print(f"  By Priority:")
        for pri, count in [('urgent', 0), ('high', 0), ('medium', 0), ('low', 0)]:
            if pri in by_priority:
                print(f"    • {pri}: {by_priority[pri]}")

    def export(self, output: str, format: str = 'json'):
        """Export notes to file."""
        notes = self._read_notes()
        output_path = Path(output).expanduser()

        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(notes, f, indent=2)
        elif format == 'md':
            # Markdown export
            with open(output_path, 'w') as f:
                f.write("# Notes Export\n\n")
                for note in notes:
                    status = '~~' if note['completed'] else ''
                    f.write(f"## {status}Note #{note['id']}: {note['category']}\n\n")
                    f.write(f"**Created:** {note['created']}\n")
                    if note['tags']:
                        f.write(f"**Tags:** {', '.join(note['tags'])}\n")
                    f.write(f"**Priority:** {note['priority']}\n\n")
                    f.write(f"{status}{note['text']}\n\n")
                    f.write("---\n\n")
        else:
            print(f"❌ Unsupported format: {format}")
            return False

        print(f"✅ Exported {len(notes)} note(s) to {output_path}")
        return True

    def _format_time(self, iso_time: str) -> str:
        """Format ISO timestamp to relative time."""
        now = datetime.now()
        try:
            created = datetime.fromisoformat(iso_time)
            diff = (now - created).total_seconds()

            if diff < 60:
                return f"Just now"
            elif diff < 3600:
                mins = int(diff / 60)
                return f"{mins}m ago"
            elif diff < 86400:
                hours = int(diff / 3600)
                return f"{hours}h ago"
            else:
                days = int(diff / 86400)
                return f"{days}d ago"
        except:
            return iso_time


def main():
    parser = argparse.ArgumentParser(
        description='notes — Quick Note Taking Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  notes add "Remember to fix the bug" -c task -t bug -p high
  notes list
  notes list -c idea
  notes search "squad"
  notes show 123
  notes complete 123
  notes export notes.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add
    add_parser = subparsers.add_parser('add', help='Add a note')
    add_parser.add_argument('text', help='Note text')
    add_parser.add_argument('-c', '--category', help='Category')
    add_parser.add_argument('-t', '--tags', nargs='*', help='Tags')
    add_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high', 'urgent'],
                           help='Priority level')

    # List
    list_parser = subparsers.add_parser('list', help='List notes')
    list_parser.add_argument('-c', '--category', help='Filter by category')
    list_parser.add_argument('-t', '--tags', nargs='*', help='Filter by tags')
    list_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high', 'urgent'],
                           help='Filter by priority')
    list_parser.add_argument('-i', '--incomplete', action='store_true',
                           help='Show incomplete only')
    list_parser.add_argument('-l', '--limit', type=int, help='Limit results')

    # Show
    show_parser = subparsers.add_parser('show', help='Show note details')
    show_parser.add_argument('id', type=int, help='Note ID')

    # Edit
    edit_parser = subparsers.add_parser('edit', help='Edit a note')
    edit_parser.add_argument('id', type=int, help='Note ID')
    edit_parser.add_argument('--text', help='New text')
    edit_parser.add_argument('-c', '--category', help='New category')
    edit_parser.add_argument('-t', '--tags', nargs='*', help='New tags')
    edit_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high', 'urgent'],
                           help='New priority')

    # Complete
    complete_parser = subparsers.add_parser('complete', help='Mark note as completed')
    complete_parser.add_argument('id', type=int, help='Note ID')

    # Uncomplete
    uncomplete_parser = subparsers.add_parser('uncomplete', help='Mark note as incomplete')
    uncomplete_parser.add_argument('id', type=int, help='Note ID')

    # Delete
    delete_parser = subparsers.add_parser('delete', help='Delete a note')
    delete_parser.add_argument('id', type=int, help='Note ID')

    # Search
    search_parser = subparsers.add_parser('search', help='Search notes')
    search_parser.add_argument('query', help='Search query')

    # Categories
    subparsers.add_parser('categories', help='List categories')

    # Stats
    subparsers.add_parser('stats', help='Show statistics')

    # Export
    export_parser = subparsers.add_parser('export', help='Export notes')
    export_parser.add_argument('file', help='Output file')
    export_parser.add_argument('-f', '--format', default='json', choices=['json', 'md'],
                           help='Export format')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    manager = NotesManager()

    if args.command == 'add':
        manager.add(args.text, args.category, args.tags, args.priority)
    elif args.command == 'list':
        manager.list(args.category, args.tags, args.priority, args.incomplete, args.limit)
    elif args.command == 'show':
        manager.show(args.id)
    elif args.command == 'edit':
        manager.edit(args.id, args.text, args.category, args.tags, args.priority)
    elif args.command == 'complete':
        manager.complete(args.id)
    elif args.command == 'uncomplete':
        manager.uncomplete(args.id)
    elif args.command == 'delete':
        manager.delete(args.id)
    elif args.command == 'search':
        manager.search(args.query)
    elif args.command == 'categories':
        manager.categories()
    elif args.command == 'stats':
        manager.stats()
    elif args.command == 'export':
        manager.export(args.file, args.format)

    return 0


if __name__ == '__main__':
    sys.exit(main())
