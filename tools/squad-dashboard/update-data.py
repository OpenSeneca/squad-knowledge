#!/usr/bin/env python3
"""
Squad Dashboard Data Updater

Queries all squad agents for status and updates data.json for the dashboard.
Run this periodically (cron) to keep the dashboard data fresh.

Usage:
    squad-dashboard-update
    squad-dashboard-update --output /path/to/data.json
    squad-dashboard-update --agents seneca marcus galen
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


# Terminal colors for output
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
        "role": "Research",
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
        "role": "Research",
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
    except subprocess.TimeoutExpired:
        # Timeout: network or agent is slow
        return None
    except subprocess.SubprocessError as e:
        # Could be SSH key issues, connection refused
        return None
    except FileNotFoundError:
        # SSH command not found
        print(f"{Colors.RED}✗ ssh command not found{Colors.RESET}")
        return None


def get_last_output(host: str) -> Optional[str]:
    """
    Get the most recent output file from an agent.
    Checks learnings/ and outputs/ directories.
    """
    # Try learnings/ first
    output = ssh_command(
        host,
        "ls -t ~/.openclaw/learnings/ 2>/dev/null | head -1",
    )
    if output:
        return output

    # Fall back to outputs/
    output = ssh_command(
        host,
        "ls -t ~/.openclaw/workspace/outputs/ 2>/dev/null | head -1",
    )
    if output:
        return output

    return None


def get_uptime(host: str) -> str:
    """
    Get agent uptime in days.
    """
    output = ssh_command(host, "uptime -p 2>/dev/null")
    if output:
        # Parse "up X days, Y hours, Z minutes"
        if "days" in output:
            parts = output.split()
            for i, part in enumerate(parts):
                if part == "days" and i > 0:
                    try:
                        days = int(parts[i - 1])
                        return f"{days}d"
                    except ValueError:
                        pass
        return "0d"
    return "0d"


def calculate_activity(host: str) -> int:
    """
    Calculate activity score based on recent output.
    Simple heuristic: check if there's been output in the last 24h.
    """
    last_output = get_last_output(host)
    if not last_output:
        return 0

    # Check file modification time
    timestamp = ssh_command(
        host,
        f"stat -c %Y ~/.openclaw/learnings/{last_output} 2>/dev/null",
    )
    if not timestamp:
        return 0

    try:
        ts = int(timestamp)
        now = datetime.now(timezone.utc).timestamp()
        hours_ago = (now - ts) / 3600

        # Activity score: 100 if <1h, scales down to 0 at 24h
        if hours_ago < 1:
            return 100
        elif hours_ago < 6:
            return int(100 - (hours_ago - 1) * 20)  # 100 -> 0
        elif hours_ago < 12:
            return 50
        elif hours_ago < 24:
            return 25
        else:
            return 0
    except ValueError:
        return 0


def get_agent_status(host: str) -> str:
    """
    Determine agent status based on recent activity.
    """
    last_output = get_last_output(host)
    if not last_output:
        return "inactive"

    # Check if the agent is reachable
    reachable = ssh_command(host, "echo pong", timeout=5)
    if reachable == "pong":
        return "active"
    else:
        return "inactive"


def query_agent(agent_id: str, agent_config: Dict) -> Dict:
    """
    Query a single agent for status.
    """
    host = agent_config["host"]
    now = datetime.now(timezone.utc).isoformat()

    print(f"  Querying {agent_config['name']} ({host})...")

    last_output = get_last_output(host)
    uptime = get_uptime(host)
    activity = calculate_activity(host)
    status = get_agent_status(host)

    return {
        "name": agent_config["name"],
        "role": agent_config["role"],
        "status": status,
        "host": host,
        "ip": agent_config["ip"],
        "last_output": last_output or "Unknown",
        "last_updated": now,
        "uptime": uptime,
        "activity": activity,
    }


def update_data_json(output_path: Path, agent_list: List[str] = None) -> bool:
    """
    Query all agents and update data.json.
    """
    now = datetime.now(timezone.utc).isoformat()

    agents = []
    agent_ids = agent_list or list(AGENTS.keys())

    for agent_id in agent_ids:
        if agent_id not in AGENTS:
            print(f"{Colors.YELLOW}⚠ Unknown agent '{agent_id}'{Colors.RESET}")
            continue

        agent_config = AGENTS[agent_id]
        agent_data = query_agent(agent_id, agent_config)
        agents.append(agent_data)

    data = {
        "updated": now,
        "agents": agents,
    }

    # Write to file
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n{Colors.GREEN}✓{Colors.RESET} Updated data.json: {output_path}")
        print(f"{Colors.GREEN}✓{Colors.RESET} Queried {len(agents)} agents")

        # Show summary statistics
        active_count = sum(1 for a in agents if a["status"] == "active")
        print(f"\n{Colors.BLUE}Summary:{Colors.RESET}")
        print(f"  Active agents:   {Colors.GREEN}{active_count}{Colors.RESET} / {len(agents)}")
        if len(agents) > 0:
            avg_activity = sum(a["activity"] for a in agents) / len(agents)
            print(f"  Average activity: {avg_activity:.1f}/100")

        return True
    except IOError as e:
        print(f"\n{Colors.RED}✗ Error writing data.json: {e}{Colors.RESET}", file=sys.stderr)
        return False


def show_status():
    """Show current status of all agents without updating data.json."""
    print(f"{Colors.BOLD}Squad Agent Status{Colors.RESET}")
    print("=" * 50)
    print()

    active_count = 0
    inactive_count = 0
    total_activity = 0

    for agent_id, config in AGENTS.items():
        host = config["host"]
        last_output = get_last_output(host)
        status = get_agent_status(host)
        activity = calculate_activity(host)

        if status == "active":
            active_count += 1
            status_symbol = f"{Colors.GREEN}●{Colors.RESET}"
        else:
            inactive_count += 1
            status_symbol = f"{Colors.RED}●{Colors.RESET}"

        print(f"  {status_symbol} {config['name']:<15} {config['role']:<12} {last_output or 'No output':<30} [{activity:3d}]")
        total_activity += activity

    print()
    print(f"{Colors.BLUE}Summary:{Colors.RESET}")
    print(f"  {Colors.GREEN}Active:{Colors.RESET}   {active_count}")
    print(f"  {Colors.RED}Inactive:{Colors.RESET} {inactive_count}")
    if active_count + inactive_count > 0:
        avg_activity = total_activity / (active_count + inactive_count)
        print(f"  Avg Activity:  {avg_activity:.1f}/100")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Update squad dashboard data.json"
    )
    parser.add_argument(
        "action",
        choices=['update', 'status'],
        nargs='?',
        default='update',
        help="Action: 'update' to refresh data.json, 'status' to show agent status"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path(__file__).parent / "data.json",
        help="Output data.json path (default: ./data.json)",
    )
    parser.add_argument(
        "--agents",
        "-a",
        nargs="+",
        help="Specific agents to query (default: all)",
    )
    args = parser.parse_args()

    if args.action == "status":
        show_status()
        sys.exit(0)

    print(f"{Colors.BOLD}Squad Dashboard Data Updater{Colors.RESET}")
    print("=" * 50)
    print()

    success = update_data_json(args.output, args.agents)

    if success:
        print(f"\n{Colors.BLUE}Dashboard will show updated data on next refresh{Colors.RESET}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
