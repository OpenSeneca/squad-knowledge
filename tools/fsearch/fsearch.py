#!/usr/bin/env python3
"""
find — Fast File Search and Finder

Search files by name, extension, content, or metadata. Fast and flexible.
"""

import os
import sys
import argparse
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional
import re


class FileFinder:
    """Fast file search and finder."""

    def __init__(self):
        self.current_dir = Path.cwd()

    def search(self,
              query: str = None,
              extension: str = None,
              content: str = None,
              name_pattern: str = None,
              min_size: int = None,
              max_size: int = None,
              modified_after: str = None,
              modified_before: str = None,
              type_filter: str = None,
              exclude_dir: List[str] = None,
              max_depth: int = None,
              include_hidden: bool = False,
              case_sensitive: bool = False) -> List[Dict]:
        """Search for files."""
        results = []

        for root, dirs, files in os.walk(self.current_dir):
            root_path = Path(root)

            # Check depth
            if max_depth:
                try:
                    depth = len(root_path.relative_to(self.current_dir).parts)
                    if depth > max_depth:
                        dirs[:] = []  # Don't descend
                        continue
                except ValueError:
                    pass  # Can't compute relative path

            # Filter directories
            if exclude_dir:
                dirs[:] = [d for d in dirs if d not in exclude_dir and not d.startswith('.')]

            # Skip hidden directories (unless include_hidden)
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]

            # Search files
            for filename in files:
                # Skip hidden files
                if not include_hidden and filename.startswith('.'):
                    continue

                filepath = root_path / filename

                try:
                    file_info = {
                        'path': str(filepath),
                        'name': filename,
                        'size': filepath.stat().st_size,
                        'modified': datetime.fromtimestamp(filepath.stat().st_mtime),
                        'extension': filepath.suffix.lower()
                    }

                    # Name pattern filter
                    if name_pattern:
                        pattern = name_pattern if case_sensitive else name_pattern.lower()
                        name_match = filename if case_sensitive else filename.lower()
                        if not re.search(pattern, name_match):
                            continue

                    # Extension filter
                    if extension:
                        ext_filter = extension.lower()
                        if not filepath.suffix.lower().endswith(ext_filter):
                            continue

                    # Type filter
                    if type_filter:
                        if not self._matches_type(filepath, type_filter):
                            continue

                    # Size filter
                    if min_size and file_info['size'] < min_size:
                        continue
                    if max_size and file_info['size'] > max_size:
                        continue

                    # Modified date filter
                    if modified_after:
                        after_date = self._parse_date(modified_after)
                        if file_info['modified'] < after_date:
                            continue
                    if modified_before:
                        before_date = self._parse_date(modified_before)
                        if file_info['modified'] > before_date:
                            continue

                    # Content search
                    if content:
                        if not self._search_content(filepath, content, case_sensitive):
                            continue

                    # Name query
                    if query:
                        query_lower = query if case_sensitive else query.lower()
                        name_lower = filename if case_sensitive else filename.lower()
                        if query_lower not in name_lower:
                            continue

                    results.append(file_info)

                except (PermissionError, OSError):
                    continue

        return results

    def _matches_type(self, filepath: Path, type_filter: str) -> bool:
        """Check if file matches type filter."""
        mime_type, _ = mimetypes.guess_type(str(filepath))

        type_map = {
            'image': ['image/'],
            'video': ['video/'],
            'audio': ['audio/'],
            'text': ['text/', 'application/json', 'application/xml', 'application/javascript'],
            'code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.rb', '.sh'],
            'document': ['.pdf', '.doc', '.docx', '.txt', '.md', '.odt', '.rtf'],
            'archive': ['.zip', '.tar', '.gz', '.bz2', '.7z', '.rar'],
        }

        if type_filter not in type_map:
            return False

        # Check by MIME type
        if type_filter in ['image', 'video', 'audio', 'text']:
            return mime_type and any(mime_type.startswith(t) for t in type_map[type_filter])

        # Check by extension
        if type_filter in ['code', 'document', 'archive']:
            return any(filepath.suffix.lower() == ext for ext in type_map[type_filter])

        return False

    def _search_content(self, filepath: Path, query: str, case_sensitive: bool) -> bool:
        """Search file content."""
        try:
            # Only search text files
            if filepath.stat().st_size > 1024 * 1024:  # Skip large files (> 1MB)
                return False

            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()

            if not case_sensitive:
                content = content.lower()
                query = query.lower()

            return query in content
        except (UnicodeDecodeError, PermissionError, OSError):
            return False

    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string."""
        try:
            # Try Unix timestamp
            if date_str.isdigit():
                return datetime.fromtimestamp(int(date_str))

            # Try ISO format
            if 'T' in date_str:
                return datetime.fromisoformat(date_str)

            # Try relative date (1d, 1h, 1w)
            if date_str.endswith(('d', 'h', 'w')):
                unit = date_str[-1]
                value = int(date_str[:-1])

                now = datetime.now()
                if unit == 'd':
                    return now.replace(day=now.day - value)
                elif unit == 'h':
                    return now.replace(hour=now.hour - value)
                elif unit == 'w':
                    return now.replace(day=now.day - value * 7)

            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            return datetime.min

    def format_size(self, size: int) -> str:
        """Format file size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size}{unit}"
            size /= 1024
        return f"{int(size)}GB"

    def format_path(self, path: str, base_dir: Path) -> str:
        """Format path relative to base directory."""
        try:
            rel_path = Path(path).relative_to(base_dir)
            return f"./{rel_path}"
        except ValueError:
            return path


def main():
    parser = argparse.ArgumentParser(
        description='find — Fast File Search and Finder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  find search "config"
  find search "test" --extension .py
  find search "TODO" --content
  find --type code
  find --extension .md --modified 1d
  find search "main" --max-depth 2
        """
    )

    # Search options
    parser.add_argument('query', nargs='*', help='Search query (filename)')
    parser.add_argument('-e', '--extension', help='File extension (e.g., .py, .js)')
    parser.add_argument('-c', '--content', help='Search file content')
    parser.add_argument('-p', '--pattern', help='Name pattern (regex)')
    parser.add_argument('--min-size', type=int, help='Minimum file size (bytes)')
    parser.add_argument('--max-size', type=int, help='Maximum file size (bytes)')

    # Date filters
    parser.add_argument('--modified-after', help='Modified after (ISO, Unix, or relative)')
    parser.add_argument('--modified-before', help='Modified before (ISO, Unix, or relative)')

    # Type filters
    parser.add_argument('--type', choices=['image', 'video', 'audio', 'text', 'code', 'document', 'archive'],
                    help='Filter by file type')

    # Directory options
    parser.add_argument('-d', '--max-depth', type=int, help='Maximum directory depth')
    parser.add_argument('-x', '--exclude-dir', action='append',
                    help='Exclude directory (can be repeated)')
    parser.add_argument('-a', '--all', action='store_true',
                    help='Include hidden files and directories')

    # Output options
    parser.add_argument('-l', '--long', action='store_true', help='Long format (show details)')
    parser.add_argument('-i', '--case-insensitive', action='store_true', help='Case insensitive search')
    parser.add_argument('-n', '--count', action='store_true', help='Count matches only')
    parser.add_argument('--limit', type=int, help='Limit results')

    args = parser.parse_args()

    finder = FileFinder()

    # Build exclude list
    exclude_dirs = args.exclude_dir or ['node_modules', '__pycache__', '.git', '.next', 'dist', 'build']

    # Handle query (convert list to string or None)
    query = ' '.join(args.query) if args.query else None

    # Search
    results = finder.search(
        query=query,
        extension=args.extension,
        content=args.content,
        name_pattern=args.pattern,
        min_size=args.min_size,
        max_size=args.max_size,
        modified_after=args.modified_after,
        modified_before=args.modified_before,
        type_filter=args.type,
        exclude_dir=exclude_dirs,
        max_depth=args.max_depth,
        include_hidden=args.all,
        case_sensitive=not args.case_insensitive
    )

    # Limit results
    if args.limit:
        results = results[:args.limit]

    # Output
    if args.count:
        print(f"📊 Found {len(results)} file(s)")
    elif not results:
        print("📭 No files found")
    else:
        print(f"📊 Found {len(results)} file(s):\n")

        for i, file_info in enumerate(results, 1):
            if args.long:
                size_str = finder.format_size(file_info['size'])
                mod_time = file_info['modified'].strftime('%Y-%m-%d %H:%M')
                print(f"{i:3d}. {file_info['name']}")
                print(f"     Path: {finder.format_path(file_info['path'], finder.current_dir)}")
                print(f"     Size: {size_str}")
                print(f"     Modified: {mod_time}")
                print()
            else:
                path_str = finder.format_path(file_info['path'], finder.current_dir)
                print(f"  {path_str}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
