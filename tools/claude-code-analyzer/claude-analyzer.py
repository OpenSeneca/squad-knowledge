#!/usr/bin/env python3
"""
claude-analyzer — Claude Code Session Analyzer

Analyze Claude Code session logs and identify inefficiencies.
"""

import sys
import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter
import datetime


class ClaudeSessionAnalyzer:
    """Analyze Claude Code session logs."""

    def __init__(self):
        self.session_dir = Path.home() / '.claude'
        self.turns = []
        self.file_accesses = defaultdict(int)
        self.tool_usage = Counter()
        self.token_usage = []
        self.context_compactions = 0

    def load_session(self, session_file: Path) -> bool:
        """Load and parse a Claude session file."""
        try:
            with open(session_file, 'r') as f:
                content = f.read()

            # Parse as JSONL (one JSON object per line)
            for line in content.strip().split('\n'):
                if not line:
                    continue

                try:
                    turn = json.loads(line)
                    self.turns.append(turn)
                    self._analyze_turn(turn)
                except json.JSONDecodeError:
                    continue

            return True

        except Exception as e:
            print(f"Error loading session: {e}", file=sys.stderr)
            return False

    def _analyze_turn(self, turn: Dict):
        """Analyze a single turn."""
        # Track file accesses
        if 'tool_calls' in turn:
            for tool_call in turn['tool_calls']:
                tool_name = tool_call.get('name', 'unknown')
                self.tool_usage[tool_name] += 1

                # Check read operations
                if tool_name == 'read':
                    args = tool_call.get('arguments', {})
                    file_path = args.get('file_path', args.get('path', ''))
                    if file_path:
                        self.file_accesses[file_path] += 1

        # Track context compactions
        if 'context_compacted' in turn:
            if turn['context_compacted']:
                self.context_compactions += 1

        # Track token usage
        if 'usage' in turn:
            usage = turn['usage']
            if 'total_tokens' in usage:
                self.token_usage.append(usage['total_tokens'])

    def analyze_anti_patterns(self) -> List[str]:
        """Detect anti-patterns in session."""
        insights = []

        # Duplicate file reads
        duplicate_reads = {k: v for k, v in self.file_accesses.items() if v > 1}
        if duplicate_reads:
            top_duplicates = sorted(duplicate_reads.items(), key=lambda x: x[1], reverse=True)[:5]
            for file_path, count in top_duplicates:
                insights.append(f"⚠️  File read {count} times: {file_path}")

        # Sensitive file reads
        sensitive_files = ['.env', '.env.local', 'secrets.json', 'config/secrets.yml']
        for sensitive_file in sensitive_files:
            if any(sensitive_file in f for f in self.file_accesses.keys()):
                insights.append(f"🔒 Sensitive file accessed: {sensitive_file}")

        # Excessive context compactions
        if self.context_compactions > 2:
            insights.append(f"📦 Context compacted {self.context_compactions} times — consider shorter sessions")

        # High tool usage
        if self.tool_usage:
            top_tool = self.tool_usage.most_common(1)[0]
            if top_tool[1] > 20:
                insights.append(f"🔧 '{top_tool[0]}' used {top_tool[1]} times — consider batching operations")

        return insights

    def get_file_access_patterns(self) -> List[Tuple[str, int]]:
        """Get file access patterns."""
        return sorted(self.file_accesses.items(), key=lambda x: x[1], reverse=True)

    def get_tool_usage(self) -> List[Tuple[str, int]]:
        """Get tool usage statistics."""
        return self.tool_usage.most_common()

    def get_token_stats(self) -> Dict:
        """Get token usage statistics."""
        if not self.token_usage:
            return {}

        return {
            'total': sum(self.token_usage),
            'avg': sum(self.token_usage) / len(self.token_usage),
            'max': max(self.token_usage),
            'min': min(self.token_usage),
            'turns': len(self.token_usage)
        }

    def generate_summary(self) -> Dict:
        """Generate session summary."""
        return {
            'turn_count': len(self.turns),
            'tool_usage_count': sum(self.tool_usage.values()),
            'unique_files': len(self.file_accesses),
            'context_compactions': self.context_compactions,
            'token_stats': self.get_token_stats()
        }

    def print_report(self, detailed: bool = False):
        """Print analysis report."""
        summary = self.generate_summary()
        insights = self.analyze_anti_patterns()

        print(f"\n{'=' * 70}")
        print(f"📊 Claude Code Session Analysis")
        print('=' * 70)

        # Summary
        print(f"\n📋 Session Summary:")
        print(f"  Turns: {summary['turn_count']}")
        print(f"  Tool calls: {summary['tool_usage_count']}")
        print(f"  Unique files: {summary['unique_files']}")
        print(f"  Context compactions: {summary['context_compactions']}")

        if summary['token_stats']:
            stats = summary['token_stats']
            print(f"  Total tokens: {stats['total']:,}")
            print(f"  Avg tokens/turn: {stats['avg']:,.0f}")

        # Insights
        if insights:
            print(f"\n💡 Insights & Anti-Patterns:")
            for insight in insights:
                print(f"  {insight}")

        # File access patterns
        if detailed:
            print(f"\n📁 File Access Patterns:")
            file_patterns = self.get_file_access_patterns()[:10]
            for file_path, count in file_patterns:
                print(f"  {count:3d}x  {file_path}")

        # Tool usage
        if detailed:
            print(f"\n🔧 Tool Usage:")
            tool_usage = self.get_tool_usage()[:10]
            for tool_name, count in tool_usage:
                print(f"  {count:3d}x  {tool_name}")

        print(f"\n{'=' * 70}\n")

    def load_latest_session(self) -> bool:
        """Load the latest session file."""
        if not self.session_dir.exists():
            print(f"Error: Session directory not found: {self.session_dir}", file=sys.stderr)
            return False

        # Find session files
        session_files = list(self.session_dir.glob('*.jsonl'))

        if not session_files:
            print(f"Error: No session files found in {self.session_dir}", file=sys.stderr)
            return False

        # Sort by modification time
        latest_session = max(session_files, key=lambda p: p.stat().st_mtime)

        print(f"Loading session: {latest_session.name}")
        return self.load_session(latest_session)

    def list_sessions(self) -> List[Path]:
        """List available session files."""
        if not self.session_dir.exists():
            return []

        session_files = list(self.session_dir.glob('*.jsonl'))
        return sorted(session_files, key=lambda p: p.stat().st_mtime, reverse=True)


def main():
    parser = argparse.ArgumentParser(
        description='claude-analyzer — Claude Code Session Analyzer'
    )

    parser.add_argument('session', nargs='?', help='Session file to analyze (default: latest)')
    parser.add_argument('--list', '-l', action='store_true',
                      help='List available sessions')
    parser.add_argument('--detailed', '-d', action='store_true',
                      help='Show detailed analysis')
    parser.add_argument('--session-dir', default=None,
                      help='Override session directory (default: ~/.claude)')

    args = parser.parse_args()

    analyzer = ClaudeSessionAnalyzer()

    # Override session directory
    if args.session_dir:
        analyzer.session_dir = Path(args.session_dir)

    # List sessions
    if args.list:
        sessions = analyzer.list_sessions()
        if not sessions:
            print("No sessions found")
            return 0

        print(f"\n📁 Available Sessions:\n")
        for i, session in enumerate(sessions[:10], 1):
            mtime = datetime.datetime.fromtimestamp(session.stat().st_mtime)
            print(f"  {i}. {session.name} ({mtime.strftime('%Y-%m-%d %H:%M')})")

        print()
        return 0

    # Load session
    if args.session:
        session_file = Path(args.session)
        if not session_file.is_absolute():
            session_file = analyzer.session_dir / session_file
    else:
        # Load latest session
        if not analyzer.load_latest_session():
            return 1
        analyzer.print_report(args.detailed)
        return 0

    # Load specific session
    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        return 1

    if not analyzer.load_session(session_file):
        return 1

    analyzer.print_report(args.detailed)

    return 0


if __name__ == '__main__':
    sys.exit(main())
