#!/usr/bin/env python3
"""
OpenClaw Session Analyzer

Analyzes OpenClaw session logs to evaluate skill effectiveness.

Measures:
- Skill activation frequency
- Token usage per skill
- Success/failure rates
- Performance rankings
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class SkillMetrics:
    """Metrics for a single skill."""
    name: str
    activations: int = 0
    total_tokens: int = 0
    success_count: int = 0
    error_count: int = 0
    avg_tokens_per_activation: float = 0.0
    success_rate: float = 0.0

    def calculate(self):
        """Calculate derived metrics."""
        if self.activations > 0:
            self.avg_tokens_per_activation = self.total_tokens / self.activations
        if self.success_count + self.error_count > 0:
            self.success_rate = self.success_count / (self.success_count + self.error_count) * 100
        else:
            self.success_rate = 0.0


@dataclass
class SessionSummary:
    """Summary of a single session."""
    session_id: str
    start_time: str
    end_time: str
    total_turns: int
    total_tokens: int
    skills_used: List[str]
    skill_metrics: Dict[str, SkillMetrics] = field(default_factory=dict)


class OpenClawSessionAnalyzer:
    """Analyzer for OpenClaw session logs."""

    def __init__(self, session_dir: str = None):
        """Initialize analyzer.

        Args:
            session_dir: Path to OpenClaw sessions directory
        """
        if session_dir is None:
            # Default OpenClaw session directory
            session_dir = os.path.expanduser("~/.openclaw/agents/main/sessions")

        self.session_dir = Path(session_dir)
        self.sessions: List[SessionSummary] = []

    def list_sessions(self) -> List[Path]:
        """List available session files."""
        if not self.session_dir.exists():
            print(f"❌ Session directory not found: {self.session_dir}")
            return []

        sessions = sorted(self.session_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        return sessions

    def parse_session(self, session_path: Path) -> Optional[SessionSummary]:
        """Parse a single OpenClaw session file.

        Args:
            session_path: Path to session JSONL file

        Returns:
            SessionSummary or None if parsing fails
        """
        events = []

        # Read all events
        try:
            with open(session_path, 'r') as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line))
        except Exception as e:
            print(f"⚠️  Error reading {session_path.name}: {e}")
            return None

        if not events:
            return None

        # Extract session info
        session_id = events[0].get('id', 'unknown')
        start_time = events[0].get('timestamp', '')
        end_time = events[-1].get('timestamp', '')

        # Track metrics
        skill_metrics = defaultdict(lambda: SkillMetrics(name=""))
        total_turns = 0
        total_tokens = 0
        skills_used = set()

        # Process events
        for event in events:
            event_type = event.get('type', '')

            # Track message turns
            if event_type == 'message':
                message = event.get('message', {})
                role = message.get('role', '')

                if role == 'assistant':
                    total_turns += 1

                    # Extract token usage
                    usage = message.get('usage', {})
                    if usage:
                        tokens = usage.get('totalTokens', 0)
                        total_tokens += tokens

                        # Detect skill activation from content
                        content = message.get('content', [])
                        current_skills = self._detect_skills(content)

                        # Distribute tokens across activated skills
                        if current_skills:
                            tokens_per_skill = tokens / len(current_skills)
                            for skill in current_skills:
                                skills_used.add(skill)
                                skill_metrics[skill].name = skill
                                skill_metrics[skill].activations += 1
                                skill_metrics[skill].total_tokens += int(tokens_per_skill)

                # Track tool results for success/error
                elif role == 'toolResult':
                    details = event.get('details', {})
                    status = details.get('status', 'unknown')

                    # Determine which skill this relates to (from context)
                    # This is a simplification - real implementation might need
                    # to track which tool call relates to which skill
                    parent_id = event.get('parentId', '')
                    related_skill = self._get_skill_from_event(events, parent_id)

                    if related_skill and related_skill in skill_metrics:
                        if status == 'completed':
                            skill_metrics[related_skill].success_count += 1
                        elif status == 'error':
                            skill_metrics[related_skill].error_count += 1

        # Calculate derived metrics for each skill
        for skill_name, metrics in skill_metrics.items():
            metrics.name = skill_name
            metrics.calculate()

        return SessionSummary(
            session_id=session_id,
            start_time=start_time,
            end_time=end_time,
            total_turns=total_turns,
            total_tokens=total_tokens,
            skills_used=sorted(skills_used),
            skill_metrics=dict(skill_metrics)
        )

    def _detect_skills(self, content: List[Dict]) -> List[str]:
        """Detect which skills are activated in message content.

        Args:
            content: Message content array

        Returns:
            List of skill names
        """
        skills = []

        for item in content:
            # Check text content for skill indicators
            if 'text' in item:
                text = item['text'].lower()

                # Common skill activation patterns
                if 'read skill' in text or 'skill:' in text:
                    # Extract skill name
                    if 'skill:' in text:
                        parts = text.split('skill:')
                        if len(parts) > 1:
                            skill_name = parts[1].strip().split()[0].capitalize()
                            if skill_name:
                                skills.append(skill_name)

            # Check for specific skill mentions in thinking
            if 'thinking' in item:
                thinking = item['thinking'].lower()

                # Skills mentioned in thinking
                skill_keywords = [
                    'github', 'coding-agent', 'weather', 'tmux', 'healthcheck',
                    'video-frames', 'nano-banana-pro', 'session-logs',
                    'skill-creator', 'canvas', 'nodes', 'browser'
                ]

                for keyword in skill_keywords:
                    if keyword in thinking:
                        skills.append(keyword)

            # Check tool calls for skill activation
            if 'toolCall' in item:
                tool_name = item.get('name', '')

                # Map tools to skills
                tool_to_skill = {
                    'gh': 'github',
                    'exec': 'coding-agent',
                    'tts': 'weather',  # Example mapping
                    'process': 'tmux',
                }

                if tool_name in tool_to_skill:
                    skills.append(tool_to_skill[tool_name])

        return list(set(skills))

    def _get_skill_from_event(self, events: List[Dict], event_id: str) -> Optional[str]:
        """Determine which skill an event relates to.

        Args:
            events: All session events
            event_id: ID of event to find skill for

        Returns:
            Skill name or None
        """
        # Find the parent event
        for event in events:
            if event.get('id', '') == event_id:
                if event.get('type', '') == 'message':
                    message = event.get('message', {})
                    role = message.get('role', '')

                    if role == 'assistant':
                        content = message.get('content', [])
                        skills = self._detect_skills(content)
                        if skills:
                            return skills[0]

        return None

    def analyze(self, session_path: Path = None) -> SessionSummary:
        """Analyze a specific session or the latest one.

        Args:
            session_path: Path to session file, or None for latest

        Returns:
            SessionSummary
        """
        if session_path is None:
            sessions = self.list_sessions()
            if not sessions:
                raise ValueError("No sessions found")

            session_path = sessions[0]
            print(f"📁 Analyzing: {session_path.name}")

        return self.parse_session(session_path)

    def analyze_all(self) -> List[SessionSummary]:
        """Analyze all available sessions.

        Returns:
            List of SessionSummary objects
        """
        sessions = self.list_sessions()
        summaries = []

        print(f"📁 Found {len(sessions)} session(s)")
        print()

        for i, session_path in enumerate(sessions, 1):
            print(f"[{i}/{len(sessions)}] Analyzing {session_path.name}...")
            summary = self.parse_session(session_path)
            if summary:
                summaries.append(summary)

        return summaries

    def aggregate_metrics(self, summaries: List[SessionSummary]) -> Dict[str, SkillMetrics]:
        """Aggregate metrics across all sessions.

        Args:
            summaries: List of session summaries

        Returns:
            Dict mapping skill names to aggregated metrics
        """
        aggregated = defaultdict(lambda: SkillMetrics(name=""))

        for summary in summaries:
            for skill_name, metrics in summary.skill_metrics.items():
                aggregated[skill_name].name = skill_name
                aggregated[skill_name].activations += metrics.activations
                aggregated[skill_name].total_tokens += metrics.total_tokens
                aggregated[skill_name].success_count += metrics.success_count
                aggregated[skill_name].error_count += metrics.error_count

        # Calculate derived metrics
        for skill_name, metrics in aggregated.items():
            metrics.calculate()

        return dict(aggregated)

    def print_summary(self, summary: SessionSummary, detailed: bool = False):
        """Print session summary to console.

        Args:
            summary: SessionSummary to print
            detailed: Whether to print detailed metrics
        """
        print()
        print("=" * 70)
        print(f"📊 OpenClaw Session Analysis")
        print("=" * 70)
        print()
        print(f"📋 Session Summary:")
        print(f"  Session ID: {summary.session_id[:12]}...")
        print(f"  Start Time: {summary.start_time}")
        print(f"  End Time: {summary.end_time}")
        print(f"  Total Turns: {summary.total_turns}")
        print(f"  Total Tokens: {summary.total_tokens:,}")
        print(f"  Avg Tokens/Turn: {summary.total_tokens // max(summary.total_turns, 1):,}")
        print()
        print(f"🔧 Skills Used: {len(summary.skills_used)}")

        if summary.skills_used:
            for skill in summary.skills_used:
                metrics = summary.skill_metrics[skill]
                print(f"  • {skill}: {metrics.activations} activations, "
                      f"{metrics.total_tokens:,} tokens")

        print()

        if detailed:
            self.print_detailed_metrics(summary.skill_metrics)

    def print_detailed_metrics(self, skill_metrics: Dict[str, SkillMetrics]):
        """Print detailed skill metrics.

        Args:
            skill_metrics: Dict of skill metrics
        """
        print("📈 Detailed Skill Metrics:")
        print()

        # Sort by activation count
        sorted_skills = sorted(
            skill_metrics.items(),
            key=lambda x: x[1].activations,
            reverse=True
        )

        for skill_name, metrics in sorted_skills:
            print(f"  {skill_name}:")
            print(f"    Activations: {metrics.activations}")
            print(f"    Total Tokens: {metrics.total_tokens:,}")
            print(f"    Avg Tokens/Activation: {metrics.avg_tokens_per_activation:.0f}")
            print(f"    Success Rate: {metrics.success_rate:.1f}% "
                  f"({metrics.success_count}/{metrics.success_count + metrics.error_count})")
            print()

        print("💡 Insights:")

        # Most used skill
        if sorted_skills:
            most_used = sorted_skills[0]
            print(f"  ⭐ Most Used: {most_used[0]} ({most_used[1].activations} activations)")

            # Least used skill (with at least 1 activation)
            used_skills = [s for s in sorted_skills if s[1].activations > 0]
            if used_skills:
                least_used = used_skills[-1]
                print(f"  📉 Least Used: {least_used[0]} ({least_used[1].activations} activations)")

        # High cost skills
        high_cost = [s for s in sorted_skills if s[1].total_tokens > 50000]
        if high_cost:
            print(f"  💰 High Token Cost: {', '.join([s[0] for s in high_cost])}")

        # Low success rate
        low_success = [s for s in sorted_skills if s[1].success_count > 0 and s[1].success_rate < 50]
        if low_success:
            print(f"  ⚠️  Low Success Rate: {', '.join([s[0] for s in low_success])}")

        print()

    def print_aggregated_report(self, summaries: List[SessionSummary]):
        """Print aggregated report across all sessions.

        Args:
            summaries: List of session summaries
        """
        aggregated = self.aggregate_metrics(summaries)

        print()
        print("=" * 70)
        print(f"📊 OpenClaw Sessions - Aggregated Report")
        print("=" * 70)
        print()
        print(f"📋 Overview:")
        print(f"  Total Sessions: {len(summaries)}")
        print(f"  Total Turns: {sum(s.total_turns for s in summaries):,}")
        print(f"  Total Tokens: {sum(s.total_tokens for s in summaries):,}")
        print()

        self.print_detailed_metrics(aggregated)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze OpenClaw session logs and evaluate skill effectiveness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze latest session
  python openclaw-session-analyzer.py

  # Analyze specific session
  python openclaw-session-analyzer.py session-xxx.jsonl

  # List all sessions
  python openclaw-session-analyzer.py --list

  # Analyze all sessions
  python openclaw-session-analyzer.py --all

  # Detailed analysis
  python openclaw-session-analyzer.py --detailed

  # Custom session directory
  python openclaw-session-analyzer.py --session-dir /path/to/sessions
        """
    )

    parser.add_argument(
        'session',
        nargs='?',
        help='Session file to analyze (default: latest)'
    )

    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available sessions'
    )

    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Analyze all sessions'
    )

    parser.add_argument(
        '--detailed', '-d',
        action='store_true',
        help='Show detailed metrics'
    )

    parser.add_argument(
        '--session-dir',
        help='Path to OpenClaw sessions directory'
    )

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = OpenClawSessionAnalyzer(session_dir=args.session_dir)

    try:
        # List sessions
        if args.list:
            sessions = analyzer.list_sessions()

            if not sessions:
                print("❌ No sessions found")
                sys.exit(1)

            print()
            print("📁 Available Sessions:")
            print()
            for i, session_path in enumerate(sessions, 1):
                size = session_path.stat().st_size
                size_str = f"{size / 1024:.1f} KB" if size >= 1024 else f"{size} B"
                mtime = datetime.fromtimestamp(session_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                print(f"  {i}. {session_path.name} ({size_str}, {mtime})")

            print()

        # Analyze all sessions
        elif args.all:
            summaries = analyzer.analyze_all()

            if not summaries:
                print("❌ No sessions to analyze")
                sys.exit(1)

            analyzer.print_aggregated_report(summaries)

        # Analyze single session
        else:
            if args.session:
                session_path = Path(args.session)
                if not session_path.exists():
                    print(f"❌ Session file not found: {session_path}")
                    sys.exit(1)
                summary = analyzer.parse_session(session_path)
            else:
                summary = analyzer.analyze()

            if not summary:
                print("❌ Failed to parse session")
                sys.exit(1)

            analyzer.print_summary(summary, detailed=args.detailed)

    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
