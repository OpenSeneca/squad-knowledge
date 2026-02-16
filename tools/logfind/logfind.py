#!/usr/bin/env python3
"""
logfind — Log File Search and Analyzer

Search, filter, and analyze log files with powerful patterns and time filters.
"""

import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional, Iterator
from datetime import datetime, timedelta
import json


class LogEntry:
    """A single log entry."""

    def __init__(self, line: str, filepath: str = None):
        self.raw = line
        self.filepath = filepath
        self.timestamp = None
        self.level = None
        self.message = line
        self._parse()

    def _parse(self):
        """Parse log entry for common formats."""
        # Try to extract timestamp
        # Common formats: YYYY-MM-DD HH:MM:SS, [timestamp], timestamp=
        timestamp_patterns = [
            r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})',
            r'\[(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})\]',
            r'timestamp=(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})',
            r'(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2})',
        ]

        for pattern in timestamp_patterns:
            match = re.search(pattern, self.raw)
            if match:
                try:
                    self.timestamp = self._parse_timestamp(match.group(1))
                    break
                except:
                    pass

        # Try to extract log level
        level_patterns = [
            r'\b(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL|TRACE)\b',
            r'\[(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL|TRACE)\]',
            r'\blevel=(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL|TRACE)\b',
        ]

        for pattern in level_patterns:
            match = re.search(pattern, self.raw)
            if match:
                self.level = match.group(1).upper()
                break

    def _parse_timestamp(self, ts_str: str) -> datetime:
        """Parse timestamp string."""
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%m/%d/%Y %H:%M:%S',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(ts_str.split('.')[0], fmt)
            except ValueError:
                pass

        raise ValueError(f"Cannot parse timestamp: {ts_str}")

    def matches(self,
                pattern: str = None,
                level: str = None,
                after: datetime = None,
                before: datetime = None) -> bool:
        """Check if entry matches filters."""
        # Pattern match
        if pattern and not re.search(pattern, self.raw, re.IGNORECASE):
            return False

        # Level match
        if level and self.level != level.upper():
            return False

        # Time range
        if after and self.timestamp and self.timestamp < after:
            return False
        if before and self.timestamp and self.timestamp > before:
            return False

        return True


class LogAnalyzer:
    """Log file analyzer."""

    def __init__(self):
        self.entries: List[LogEntry] = []

    def read_file(self, filepath: str) -> Iterator[LogEntry]:
        """Read log file."""
        try:
            with open(filepath, 'r', errors='ignore') as f:
                for line in f:
                    line = line.rstrip('\n\r')
                    if line:
                        yield LogEntry(line, filepath)
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)

    def search(self,
              filepaths: List[str],
              pattern: str = None,
              level: str = None,
              after: str = None,
              before: str = None,
              context: int = 0,
              reverse: bool = False) -> List[LogEntry]:
        """Search log files."""
        results = []
        after_dt = self._parse_time(after) if after else None
        before_dt = self._parse_time(before) if before else None

        # Read all entries
        all_entries = []
        for filepath in filepaths:
            for entry in self.read_file(filepath):
                if entry.matches(pattern, level, after_dt, before_dt):
                    all_entries.append(entry)

        # Sort by timestamp if available
        all_entries.sort(key=lambda x: x.timestamp or datetime.min)

        # Reverse if requested
        if reverse:
            all_entries.reverse()

        # Add context
        if context > 0:
            for entry in all_entries[:]:
                if entry.filepath:
                    context_entries = self._get_context(entry.filepath, context)
                    for ctx_entry in context_entries:
                        if ctx_entry not in results:
                            results.append(ctx_entry)

        return all_entries

    def _get_context(self, filepath: str, lines: int) -> List[LogEntry]:
        """Get context lines around a match."""
        # This is a simplified implementation
        # In a full implementation, we'd track line numbers
        return []

    def _parse_time(self, time_str: str) -> datetime:
        """Parse time string."""
        now = datetime.now()

        # Relative time
        if time_str.endswith('m'):
            minutes = int(time_str[:-1])
            return now - timedelta(minutes=minutes)
        elif time_str.endswith('h'):
            hours = int(time_str[:-1])
            return now - timedelta(hours=hours)
        elif time_str.endswith('d'):
            days = int(time_str[:-1])
            return now - timedelta(days=days)

        # ISO format
        try:
            if 'T' in time_str:
                return datetime.fromisoformat(time_str)
            else:
                return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        except:
            pass

        raise ValueError(f"Cannot parse time: {time_str}")

    def stats(self, entries: List[LogEntry]) -> Dict:
        """Calculate statistics."""
        stats = {
            'total': len(entries),
            'by_level': {},
            'by_file': {},
            'with_timestamp': 0,
            'without_timestamp': 0,
        }

        for entry in entries:
            # Count by level
            if entry.level:
                stats['by_level'][entry.level] = stats['by_level'].get(entry.level, 0) + 1

            # Count by file
            if entry.filepath:
                stats['by_file'][entry.filepath] = stats['by_file'].get(entry.filepath, 0) + 1

            # Count timestamps
            if entry.timestamp:
                stats['with_timestamp'] += 1
            else:
                stats['without_timestamp'] += 1

        return stats

    def tail(self, filepath: str, lines: int = 10) -> List[LogEntry]:
        """Get last N lines from file."""
        entries = list(self.read_file(filepath))
        return entries[-lines:] if entries else []

    def grep(self, filepath: str, pattern: str, context: int = 0) -> List[str]:
        """Grep file for pattern."""
        results = []
        try:
            with open(filepath, 'r', errors='ignore') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if re.search(pattern, line, re.IGNORECASE):
                        # Add context
                        start = max(0, i - context)
                        end = min(len(lines), i + context + 1)
                        results.extend(lines[start:end])
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)

        return results


def format_entry(entry: LogEntry, show_file: bool = False,
                show_level: bool = False, show_time: bool = False) -> str:
    """Format log entry."""
    parts = []

    if show_file and entry.filepath:
        parts.append(f"[{Path(entry.filepath).name}]")

    if show_level and entry.level:
        level_color = {
            'DEBUG': '\033[36m',    # Cyan
            'INFO': '\033[32m',     # Green
            'WARN': '\033[33m',     # Yellow
            'WARNING': '\033[33m',  # Yellow
            'ERROR': '\033[31m',    # Red
            'FATAL': '\033[31m',    # Red
            'CRITICAL': '\033[31m', # Red
            'TRACE': '\033[37m',    # White
        }
        reset = '\033[0m'
        color = level_color.get(entry.level, '')
        parts.append(f"{color}[{entry.level}]{reset}")

    if show_time and entry.timestamp:
        parts.append(f"[{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]")

    parts.append(entry.raw)

    return ' '.join(parts)


def main():
    parser = argparse.ArgumentParser(
        description='logfind — Log File Search and Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  logfind app.log
  logfind app.log --pattern "ERROR"
  logfind app.log --level ERROR
  logfind app.log --pattern "timeout" --after 1h
  logfind app.log,access.log --pattern "404"
  logfind app.log --tail 50
  logfind app.log --grep "user.*login"
  logfind app.log --stats

Common Use Cases:
  - Search for errors in logs
  - Filter by log level
  - Search within time range
  - Monitor log files
  - Analyze log statistics
        """
    )

    # Files
    parser.add_argument('files', nargs='+', help='Log files to search')

    # Search options
    parser.add_argument('-p', '--pattern', help='Search pattern (regex)')
    parser.add_argument('-l', '--level',
                      choices=['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL', 'TRACE'],
                      help='Filter by log level')
    parser.add_argument('--after', help='Show entries after time (ISO or relative, e.g., 1h, 30m)')
    parser.add_argument('--before', help='Show entries before time (ISO or relative, e.g., 1h, 30m)')

    # Output options
    parser.add_argument('--tail', type=int, help='Show last N lines')
    parser.add_argument('--head', type=int, help='Show first N lines')
    parser.add_argument('--grep', help='Simple grep (no log parsing)')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Formatting
    parser.add_argument('--show-file', action='store_true', help='Show filename')
    parser.add_argument('--show-level', action='store_true', help='Show log level')
    parser.add_argument('--show-time', action='store_true', help='Show timestamp')
    parser.add_argument('--color', action='store_true', help='Colored output (default if terminal)')

    # Direction
    parser.add_argument('--reverse', action='store_true', help='Show in reverse order (newest first)')

    args = parser.parse_args()

    analyzer = LogAnalyzer()

    # Tail mode
    if args.tail:
        for filepath in args.files:
            entries = analyzer.tail(filepath, args.tail)
            for entry in entries:
                print(entry.raw)
        return 0

    # Grep mode
    if args.grep:
        for filepath in args.files:
            results = analyzer.grep(filepath, args.grep)
            for line in results:
                print(line.rstrip())
        return 0

    # Stats mode
    if args.stats:
        all_entries = []
        for filepath in args.files:
            all_entries.extend(analyzer.read_file(filepath))

        stats = analyzer.stats(all_entries)
        print(f"📊 Log Statistics\n")
        print(f"Total entries: {stats['total']}")
        print(f"  With timestamps: {stats['with_timestamp']}")
        print(f"  Without timestamps: {stats['without_timestamp']}")

        if stats['by_level']:
            print(f"\nBy level:")
            for level, count in sorted(stats['by_level'].items()):
                print(f"  {level}: {count}")

        if stats['by_file']:
            print(f"\nBy file:")
            for filepath, count in sorted(stats['by_file'].items()):
                print(f"  {filepath}: {count}")

        return 0

    # Search mode
    results = analyzer.search(
        args.files,
        pattern=args.pattern,
        level=args.level,
        after=args.after,
        before=args.before,
        reverse=args.reverse
    )

    # Limit results
    if args.head:
        results = results[:args.head]

    # Output
    if args.json:
        output = []
        for entry in results:
            output.append({
                'file': entry.filepath,
                'raw': entry.raw,
                'timestamp': entry.timestamp.isoformat() if entry.timestamp else None,
                'level': entry.level,
            })
        print(json.dumps(output, indent=2))
    else:
        # Auto-detect if we want color (terminal)
        show_color = args.color if args.color is not None else sys.stdout.isatty()

        for entry in results:
            if show_color and args.show_level and entry.level:
                # Color output is handled in format_entry
                print(format_entry(entry, args.show_file, args.show_level, args.show_time))
            else:
                # Strip ANSI codes if no color
                line = format_entry(entry, args.show_file, args.show_level, args.show_time)
                print(line)  # Let the terminal handle codes

    return 0


if __name__ == '__main__':
    sys.exit(main())
