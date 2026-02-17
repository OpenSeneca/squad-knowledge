#!/usr/bin/env python3
"""
squad-stats — Analyze agent output productivity

Analyze agent outputs to show:
- How many outputs each agent produced
- Word/character counts per agent
- Trends over time (daily, weekly)
- Most productive agents

Usage:
    squad-stats
    squad-stats --days 7
    squad-stats --agents marcus galen
    squad-stats --format json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path


def scan_outputs(days=30):
    """Scan agent outputs directory."""
    outputs_dir = Path.home() / ".openclaw/workspace/outputs"

    if not outputs_dir.exists():
        print(f"❌ Outputs directory not found: {outputs_dir}")
        return {}

    # Get files modified in last N days
    cutoff = datetime.now() - timedelta(days=days)
    files = []

    for f in outputs_dir.glob("*.md"):
        if f.stat().st_mtime > cutoff.timestamp():
            files.append(f)

    if not files:
        print(f"⚠️  No output files found in last {days} days")
        return {}

    print(f"🔍 Scanning {len(files)} output files from last {days} days...")

    # Read and analyze each file
    stats = defaultdict(lambda: {
        'files': 0,
        'words': 0,
        'characters': 0,
        'lines': 0,
        'dates': []
    })

    for f in files:
        try:
            with open(f) as file:
                content = file.read()

            # Extract agent name from filename
            agent = extract_agent_from_filename(f.name)

            # Count metrics
            words = len(content.split())
            chars = len(content)
            lines = len(content.split('\n'))
            date = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')

            stats[agent]['files'] += 1
            stats[agent]['words'] += words
            stats[agent]['characters'] += chars
            stats[agent]['lines'] += lines
            stats[agent]['dates'].append(date)

        except Exception as e:
            print(f"⚠️  Error reading {f.name}: {e}")

    return dict(stats)


def extract_agent_from_filename(filename):
    """Extract agent name from output filename."""
    # Try to find agent name patterns
    patterns = [
        r'([a-z]+)-\d{4}-\d{2}-\d{2}',  # agent-YYYY-MM-DD
        r'([a-z]+)-output',  # agent-output
        r'([a-z]+)-daily',  # agent-daily
        r'([a-z]+)-summary',  # agent-summary
        r'^([a-z]+)-',  # agent-anything
    ]

    for pattern in patterns:
        match = re.match(pattern, filename.lower())
        if match:
            return match.group(1).capitalize()

    # Default to "Unknown"
    return "Unknown"


def calculate_daily_trends(stats):
    """Calculate daily output trends."""
    trends = defaultdict(lambda: defaultdict(int))

    for agent, data in stats.items():
        for date in data['dates']:
            # Approximate daily output (words / unique dates)
            unique_dates = len(set(data['dates']))
            if unique_dates > 0:
                trends[agent][date] = data['words'] / unique_dates

    return dict(trends)


def generate_report(stats, days, format_type='text'):
    """Generate stats report."""
    if format_type == 'json':
        return generate_json_report(stats, days)

    return generate_text_report(stats, days)


def generate_text_report(stats, days):
    """Generate human-readable text report."""
    lines = [
        "# Squad Output Statistics",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Period:** Last {days} days",
        f"---",
        f"",
    ]

    if not stats:
        lines.append("No output data available.")
        return '\n'.join(lines)

    # Summary table
    lines.append("## Summary by Agent")
    lines.append("")
    lines.append("| Agent | Files | Words | Characters | Lines | Avg Words/File |")
    lines.append("|-------|-------|-------|------------|-------|----------------|")

    for agent, data in sorted(stats.items(), key=lambda x: x[1]['words'], reverse=True):
        avg_words = data['words'] / data['files'] if data['files'] > 0 else 0
        lines.append(f"| {agent} | {data['files']} | {data['words']:,} | {data['characters']:,} | {data['lines']:,} | {avg_words:.0f} |")

    lines.append("")

    # Overall stats
    total_files = sum(d['files'] for d in stats.values())
    total_words = sum(d['words'] for d in stats.values())
    total_chars = sum(d['characters'] for d in stats.values())
    total_lines = sum(d['lines'] for d in stats.values())

    lines.append("## Overall Statistics")
    lines.append("")
    lines.append(f"- **Total Files:** {total_files}")
    lines.append(f"- **Total Words:** {total_words:,}")
    lines.append(f"- **Total Characters:** {total_chars:,}")
    lines.append(f"- **Total Lines:** {total_lines:,}")
    lines.append(f"- **Active Agents:** {len(stats)}")
    lines.append("")

    # Top producers
    lines.append("## Top Producers (by word count)")
    lines.append("")

    sorted_agents = sorted(stats.items(), key=lambda x: x[1]['words'], reverse=True)
    for i, (agent, data) in enumerate(sorted_agents[:5], 1):
        lines.append(f"{i}. **{agent}** — {data['words']:,} words ({data['files']} files)")

    if len(sorted_agents) > 5:
        lines.append(f"... and {len(sorted_agents) - 5} more agents")

    lines.append("")

    # Productivity ranking
    lines.append("## Productivity Ranking")
    lines.append("")

    for i, (agent, data) in enumerate(sorted_agents, 1):
        avg_words = data['words'] / data['files'] if data['files'] > 0 else 0
        lines.append(f"{i}. **{agent}** — {avg_words:.0f} avg words/file")

    lines.append("")

    # Daily trends
    lines.append("## Notes")
    lines.append("")
    lines.append("- Word counts are approximate (space-separated tokens)")
    lines.append("- Files are counted if modified in the specified period")
    lines.append("- Agent names are extracted from filename patterns")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by squad-stats*")

    return '\n'.join(lines)


def generate_json_report(stats, days):
    """Generate JSON report."""
    report = {
        'generated': datetime.now().isoformat(),
        'period_days': days,
        'summary': {}
    }

    # Add per-agent stats
    for agent, data in stats.items():
        avg_words = data['words'] / data['files'] if data['files'] > 0 else 0
        avg_chars = data['characters'] / data['files'] if data['files'] > 0 else 0
        avg_lines = data['lines'] / data['files'] if data['files'] > 0 else 0

        report['summary'][agent] = {
            'files': data['files'],
            'words': data['words'],
            'characters': data['characters'],
            'lines': data['lines'],
            'avg_words_per_file': round(avg_words, 2),
            'avg_characters_per_file': round(avg_chars, 2),
            'avg_lines_per_file': round(avg_lines, 2),
            'unique_dates': len(set(data['dates']))
        }

    # Add totals
    report['totals'] = {
        'total_files': sum(d['files'] for d in stats.values()),
        'total_words': sum(d['words'] for d in stats.values()),
        'total_characters': sum(d['characters'] for d in stats.values()),
        'total_lines': sum(d['lines'] for d in stats.values()),
        'active_agents': len(stats)
    }

    return json.dumps(report, indent=2)


def save_report(content, output_path=None):
    """Save report to file."""
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        if content.strip().startswith('{'):
            # JSON format
            output_path = Path.home() / ".openclaw/workspace/outputs" / f"squad-stats-{timestamp}.json"
        else:
            # Text format
            output_path = Path.home() / ".openclaw/workspace/outputs" / f"squad-stats-{timestamp}.md"

    output_path = Path(output_path).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)

    print(f"✅ Saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Analyze agent output productivity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze last 30 days (default)
  squad-stats

  # Analyze last 7 days
  squad-stats --days 7

  # Save to file
  squad-stats --days 7 --save

  # JSON output for programmatic use
  squad-stats --format json

Output:
  - Files per agent
  - Word/character/line counts
  - Productivity ranking
  - Top producers

What It Analyzes:
- Agent outputs in ~/workspace/outputs/
- Files modified in last N days
- Agent names extracted from filename patterns

Use Cases:
- Justin: Track squad productivity over time
- Squad: Identify most/least productive agents
- Review: Weekly/monthly productivity reports
        """
    )

    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to analyze (default: 30)',
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format: text (default) or json',
    )

    parser.add_argument(
        '--save',
        action='store_true',
        help='Save report to outputs directory',
    )

    parser.add_argument(
        '--output',
        help='Output file path',
    )

    args = parser.parse_args()

    # Scan outputs
    stats = scan_outputs(days=args.days)

    if not stats:
        print("\nNo data to analyze.")
        sys.exit(0)

    # Generate report
    print(f"\n📊 Generating report...")
    report = generate_report(stats, args.days, args.format)

    # Print report
    print(f"\n{report}")

    # Save to file if requested
    if args.save:
        save_report(report, args.output)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
