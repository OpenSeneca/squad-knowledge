#!/usr/bin/env python3
"""
Squad Learnings Aggregator

Pulls learnings from all squad agents and creates a unified digest.
Supports SSH to remote agents with graceful fallback.

Usage:
    squad-learnings                      # All agents, recent only
    squad-learnings --days 7             # Last 7 days
    squad-learnings --agents marcus galen  # Specific agents only
    squad-learnings --output digest.md    # Save to file
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional
import argparse


# Terminal colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# Squad agent configuration
AGENTS = {
    "seneca": {
        "name": "Seneca",
        "role": "Coordinator",
        "host": "lobster-1",
        "ip": "100.101.15.68",
    },
    "marcus": {
        "name": "Marcus",
        "role": "Research (AI)",
        "host": "marcus-squad",
        "ip": "100.98.223.103",
    },
    "archimedes": {
        "name": "Archimedes",
        "role": "Build",
        "host": "archimedes-squad",
        "ip": "100.100.56.102",
    },
    "argus": {
        "name": "Argus",
        "role": "Ops",
        "host": "argus-squad",
        "ip": "100.108.219.91",
    },
    "galen": {
        "name": "Galen",
        "role": "Research (Biotech)",
        "host": "galen-squad",
        "ip": "100.123.121.125",
    },
}


def ssh_command(host: str, command: str, timeout: int = 10) -> Optional[str]:
    """
    Run SSH command and return output, or None on failure.
    """
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes", host, command],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return None


def get_learnings_list(agent_id: str, days: int = 1) -> List[Dict[str, str]]:
    """
    Get list of learning files from an agent, optionally filtered by date.
    Returns list of {filename, content, agent, role, date}
    """
    if agent_id not in AGENTS:
        return []

    agent = AGENTS[agent_id]
    host = agent["host"]

    # Try SSH first - filter for YYYY-MM-DD-*.md format only (not seed files)
    files_json = ssh_command(
        host,
        f"find ~/.openclaw/learnings/ -name '????-??-??-*.md' -mtime -{days} -type f 2>/dev/null | sort -r | head -20",
    )

    # Fallback: local agent
    if not files_json and agent_id == "archimedes":
        local_path = Path.home() / ".openclaw" / "learnings"
        if local_path.exists():
            # Filter for YYYY-MM-DD-*.md pattern only
            pattern = re.compile(r'\d{4}-\d{2}-\d{2}-.*\.md$')
            files = [f for f in local_path.glob("*.md") if pattern.match(f.name) and f.stat().st_mtime >= (datetime.now().timestamp() - days * 86400)]
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            files_json = "\n".join(str(f.name) for f in files[:20])

    if not files_json:
        return []

    files = [f for f in files_json.split("\n") if f.strip()]
    learnings = []

    for filename in files:
        if not filename:
            continue

        # Get file content via SSH
        content = ssh_command(host, f"cat ~/.openclaw/learnings/{filename}")

        # Fallback: local content
        if not content and agent_id == "archimedes":
            local_file = Path.home() / ".openclaw" / "learnings" / filename
            if local_file.exists():
                content = local_file.read_text()

        if content:
            # Extract date from filename (YYYY-MM-DD-format)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
            date_str = date_match.group(1) if date_match else "Unknown"
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d") if date_str != "Unknown" else datetime.now()
            except ValueError:
                date = datetime.now()

            learnings.append({
                "filename": filename,
                "content": content,
                "agent": agent["name"],
                "role": agent["role"],
                "agent_id": agent_id,
                "date": date,
                "date_str": date_str,
            })

    return learnings


def extract_insights(content: str) -> Dict[str, List[str]]:
    """
    Extract structured insights from learning file content.
    """
    insights = {
        "key_points": [],
        "tools": [],
        "recommendations": [],
        "tweets": [],
    }

    lines = content.split("\n")

    for line in lines:
        # Key points (bullet points)
        if line.strip().startswith(("-", "*")) and len(line.strip()) > 10:
            clean_line = re.sub(r'^[-*]\s*', '', line.strip())
            if clean_line and len(clean_line) < 200:
                insights["key_points"].append(clean_line)

        # Tool mentions
        tool_match = re.search(r'`([\w-]+)`', line)
        if tool_match and len(tool_match.group(1)) > 3:
            tool = tool_match.group(1)
            if tool not in insights["tools"]:
                insights["tools"].append(tool)

        # Tweet drafts
        if "## Tweet Draft" in line or "tweet draft" in line.lower():
            # Extract next few lines as tweet
            idx = lines.index(line)
            tweet_lines = []
            for tweet_line in lines[idx+1:idx+5]:
                if not tweet_line.strip() or tweet_line.startswith("#"):
                    break
                tweet_lines.append(tweet_line.strip())
            if tweet_lines:
                insights["tweets"].append("\n".join(tweet_lines))

        # Recommendations
        if "## Recommendations" in line or "recommendation" in line.lower():
            idx = lines.index(line)
            for rec_line in lines[idx+1:idx+10]:
                if not rec_line.strip() or rec_line.startswith("##"):
                    break
                if rec_line.strip().startswith(("-", "*")):
                    clean_rec = re.sub(r'^[-*]\s*', '', rec_line.strip())
                    insights["recommendations"].append(clean_rec)

    return insights


def format_markdown(learnings: List[Dict], title: str = "Squad Learnings Digest") -> str:
    """
    Format all learnings as a unified markdown digest.
    """
    output = []
    output.append(f"# {title}\n")
    output.append(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
    output.append(f"**Total Learnings:** {len(learnings)}\n")

    # Group by agent
    by_agent = {}
    for learning in learnings:
        agent_name = learning["agent"]
        if agent_name not in by_agent:
            by_agent[agent_name] = []
        by_agent[agent_name].append(learning)

    # Section for each agent
    for agent_name, agent_learnings in sorted(by_agent.items(), key=lambda x: x[0]):
        if not agent_learnings:
            continue

        role = agent_learnings[0]["role"]
        output.append(f"\n## {agent_name} ({role})\n")

        for learning in sorted(agent_learnings, key=lambda x: x["date"], reverse=True):
            output.append(f"\n### {learning['filename']}")
            output.append(f"_Date: {learning['date_str']}_\n")

            insights = extract_insights(learning["content"])

            # Key points
            if insights["key_points"]:
                output.append("\n**Key Points:**")
                for point in insights["key_points"][:5]:  # Max 5 points
                    output.append(f"- {point}")

            # Tools mentioned
            if insights["tools"]:
                output.append(f"\n**Tools:** {', '.join(insights['tools'][:5])}")

            # Tweet drafts
            if insights["tweets"]:
                output.append("\n**Tweet Draft:**")
                for tweet in insights["tweets"][:1]:  # First tweet only
                    output.append(f"> {tweet}")

            # Recommendations
            if insights["recommendations"]:
                output.append("\n**Recommendations:**")
                for rec in insights["recommendations"][:3]:  # Max 3
                    output.append(f"- {rec}")

            output.append("\n---")

    # Summary section
    output.append("\n## Summary\n\n")

    all_tools = set()
    all_tweets = []
    all_recs = []

    for learning in learnings:
        insights = extract_insights(learning["content"])
        all_tools.update(insights["tools"])
        all_tweets.extend(insights["tweets"])
        all_recs.extend(insights["recommendations"])

    if all_tools:
        output.append(f"**Tools Mentioned:** {', '.join(sorted(all_tools)[:10])}\n")

    if all_tweets:
        output.append(f"\n**Tweet Drafts:** {len(all_tweets)} ready\n")

    if all_recs:
        output.append(f"\n**Recommendations:** {len(all_recs)} items\n")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate squad learnings from all agents"
    )
    parser.add_argument(
        "--days",
        "-d",
        type=int,
        default=1,
        help="Days of learnings to include (default: 1)",
    )
    parser.add_argument(
        "--agents",
        "-a",
        nargs="+",
        help="Specific agents to include (default: all)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path (default: stdout)",
    )
    args = parser.parse_args()

    print(f"{Colors.BOLD}Squad Learnings Aggregator{Colors.RESET}")
    print("=" * 50)
    print()

    # Collect learnings from all agents
    agent_ids = args.agents or list(AGENTS.keys())
    all_learnings = []

    for agent_id in agent_ids:
        print(f"  Querying {AGENTS[agent_id]['name']}...", end="")

        learnings = get_learnings_list(agent_id, days=args.days)

        if learnings:
            print(f" {Colors.GREEN}✓{Colors.RESET} {len(learnings)} files")
            all_learnings.extend(learnings)
        else:
            print(f" {Colors.YELLOW}✗{Colors.RESET} No learnings")

    if not all_learnings:
        print(f"\n{Colors.YELLOW}No learnings found{Colors.RESET}")
        sys.exit(0)

    # Generate markdown
    title = f"Squad Learnings - {datetime.now().strftime('%Y-%m-%d')}"
    markdown = format_markdown(all_learnings, title)

    # Output
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown)
        print(f"\n{Colors.GREEN}✓{Colors.RESET} Digest saved to {args.output}")
    else:
        print(f"\n{Colors.BLUE}--- Digest ---{Colors.RESET}\n")
        print(markdown)


if __name__ == "__main__":
    main()
