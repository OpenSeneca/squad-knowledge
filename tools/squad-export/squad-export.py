#!/usr/bin/env python3
"""
Squad Export Tool - Export squad data for unified interfaces.

Exports squad status, learnings, and tools in unified formats
for integration with multi-agent platforms like AionUi.

Usage:
    squad-export [options]

Options:
    --format FORMAT    Output format: json, markdown (default: json)
    --output FILE      Output file (default: stdout)
    --since DATE       Filter learnings by date (YYYY-MM-DD)
    --agents AGENTS     Comma-separated agent names (default: all)
    --include-learnings Include learnings in export
    --include-tools     Include tool inventory in export
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import glob


class SquadExport:
    """Export squad data for unified interfaces."""

    def __init__(self, workspace_path=None, learnings_path=None):
        self.workspace = Path(workspace_path or os.path.expanduser("~/.openclaw/workspace"))
        self.learnings = Path(learnings_path or os.path.expanduser("~/.openclaw/learnings"))

    def get_dashboard_data(self):
        """Load squad dashboard data.json if available."""
        dashboard_path = self.workspace / "tools/squad-dashboard/data.json"

        if not dashboard_path.exists():
            return None

        try:
            with open(dashboard_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load dashboard data: {e}", file=sys.stderr)
            return None

    def get_agent_status(self, agents=None):
        """Get agent status from dashboard data."""
        dashboard = self.get_dashboard_data()

        if not dashboard:
            return []

        agent_list = agents.split(",") if agents else None

        status_list = []

        # Handle both array and object formats
        agents_data = dashboard.get("agents", [])

        # If it's a dict (object), convert to list
        if isinstance(agents_data, dict):
            agents_data = list(agents_data.values())

        for agent_data in agents_data:
            # Get agent ID
            agent_id = agent_data.get("id", agent_data.get("name", "unknown"))

            # Filter by agent names if specified
            if agent_list:
                if agent_id not in agent_list:
                    continue

            status = {
                "id": agent_id,
                "name": agent_data.get("name", agent_id),
                "role": agent_data.get("role", "unknown"),
                "status": agent_data.get("status", "unknown"),
                "last_output": agent_data.get("last_output"),
                "uptime_hours": agent_data.get("uptime_hours", 0),
                "activity_score": agent_data.get("activity_score", 0)
            }
            status_list.append(status)

        return status_list

    def get_learnings(self, since=None, days=None, agents=None):
        """Get learnings from all agents."""
        learnings_list = []

        # Parse date filter
        since_date = None
        if since:
            try:
                since_date = datetime.strptime(since, "%Y-%m-%d")
            except ValueError:
                print(f"Warning: Invalid date format: {since}", file=sys.stderr)

        # Calculate cutoff date for days filter
        cutoff_date = None
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)

        # Find learning files (YYYY-MM-DD-*.md pattern)
        for learning_file in sorted(self.learnings.glob("*.md"), reverse=True):
            filename = learning_file.name

            # Skip seed files
            if filename.startswith("seed-"):
                continue

            # Skip archive directory
            if learning_file.parent.name == "archive":
                continue

            # Extract date from filename
            try:
                # Format: YYYY-MM-DD-*.md
                date_str = filename[:10]
                file_date = datetime.strptime(date_str, "%Y-%m-%d")

                # Apply date filters
                if since_date and file_date < since_date:
                    continue
                if cutoff_date and file_date < cutoff_date:
                    continue

                # Check if file is from a specific agent
                # This assumes agents write to files named YYYY-MM-DD-*.md
                # and the agent is mentioned in the content

                content = learning_file.read_text()

                learning_entry = {
                    "filename": filename,
                    "date": date_str,
                    "path": str(learning_file),
                    "preview": self._get_preview(content),
                    "lines": len(content.splitlines())
                }

                # Try to detect agent from content or filename
                agent = self._detect_agent(content, filename)
                if agent:
                    learning_entry["agent"] = agent
                    if agents and agent not in agents.split(","):
                        continue

                learnings_list.append(learning_entry)

            except (ValueError, IndexError):
                continue

        return learnings_list

    def _get_preview(self, content, max_chars=300):
        """Get preview of learning content."""
        lines = content.splitlines()

        # Skip empty lines and metadata headers
        preview_lines = []
        for line in lines[:20]:
            if line.strip() and not line.startswith("#") and not line.startswith("---"):
                preview_lines.append(line.strip())

        preview = " ".join(preview_lines)
        if len(preview) > max_chars:
            preview = preview[:max_chars-3] + "..."

        return preview

    def _detect_agent(self, content, filename):
        """Try to detect agent from learning content."""
        # Check for agent names in content
        agents = ["archimedes", "marcus", "galen", "argus", "seneca"]

        content_lower = content.lower()

        for agent in agents:
            if agent in content_lower:
                return agent

        # Check filename for agent hints
        if "-" in filename and len(filename.split("-")) > 2:
            # Format: YYYY-MM-DD-*.md, the * might contain agent name
            parts = filename.split("-")
            if len(parts) > 2:
                suffix = "-".join(parts[2:])  # Everything after date
                suffix = suffix.replace(".md", "")

                # Check if suffix matches agent names
                suffix_lower = suffix.lower()
                for agent in agents:
                    if agent in suffix_lower:
                        return agent

        return None

    def get_tools_inventory(self):
        """Get tool inventory from workspace."""
        tools_dir = self.workspace / "tools"

        if not tools_dir.exists():
            return []

        tools_list = []

        for tool_dir in sorted(tools_dir.iterdir()):
            if not tool_dir.is_dir():
                continue

            # Skip __pycache__ and hidden directories
            if tool_dir.name.startswith("_") or tool_dir.name.startswith("."):
                continue

            tool_info = {
                "name": tool_dir.name,
                "path": str(tool_dir)
            }

            # Check for README
            readme_path = tool_dir / "README.md"
            tool_info["has_readme"] = readme_path.exists()

            # Check for Python files
            py_files = list(tool_dir.glob("*.py"))
            tool_info["python_files"] = [f.name for f in py_files]
            tool_info["python_count"] = len(py_files)

            # Check for Bash scripts
            sh_files = list(tool_dir.glob("*.sh"))
            tool_info["bash_files"] = [f.name for f in sh_files]
            tool_info["bash_count"] = len(sh_files)

            # Check for package.json (Node)
            package_path = tool_dir / "package.json"
            tool_info["has_node"] = package_path.exists()

            # Check for requirements.txt or pyproject.toml (Python dependencies)
            deps_files = []
            for dep_file in ["requirements.txt", "pyproject.toml", "setup.py"]:
                if (tool_dir / dep_file).exists():
                    deps_files.append(dep_file)
            tool_info["deps_files"] = deps_files

            tools_list.append(tool_info)

        return tools_list

    def export_json(self, agents=None, since=None, days=None,
                   include_learnings=False, include_tools=False):
        """Export data as JSON."""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "squad": {
                "agents": self.get_agent_status(agents),
            }
        }

        if include_learnings:
            export_data["squad"]["learnings"] = self.get_learnings(since, days, agents)

        if include_tools:
            export_data["squad"]["tools"] = self.get_tools_inventory()

        return json.dumps(export_data, indent=2)

    def export_markdown(self, agents=None, since=None, days=None,
                      include_learnings=False, include_tools=False):
        """Export data as Markdown."""
        lines = []

        lines.append("# Squad Export")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().isoformat()}")
        lines.append("")

        # Agent Status
        lines.append("## Agent Status")
        lines.append("")

        agent_list = self.get_agent_status(agents)

        if not agent_list:
            lines.append("*No agent data available*")
        else:
            lines.append("| ID | Name | Role | Status | Uptime | Activity |")
            lines.append("|----|------|------|--------|--------|----------|")

            for agent in agent_list:
                status = agent["status"]
                status_emoji = "🟢" if status == "active" else "🔴"

                lines.append(f"| {agent['id']} | {agent['name']} | {agent['role']} | "
                          f"{status_emoji} {status} | {agent['uptime_hours']:.1f}h | "
                          f"{agent['activity_score']} |")

        # Learnings
        if include_learnings:
            lines.append("")
            lines.append("## Recent Learnings")
            lines.append("")

            learnings_list = self.get_learnings(since, days, agents)

            if not learnings_list:
                lines.append("*No learnings found*")
            else:
                for learning in learnings_list[:20]:  # Limit to 20 most recent
                    agent_display = f" [{learning['agent']}]" if learning.get('agent') else ""
                    lines.append(f"### {learning['date']}{agent_display}")
                    lines.append("")
                    lines.append(f"**File:** `{learning['filename']}`")
                    lines.append("")
                    lines.append(learning['preview'])
                    lines.append("")

        # Tools
        if include_tools:
            lines.append("")
            lines.append("## Tools Inventory")
            lines.append("")

            tools_list = self.get_tools_inventory()

            if not tools_list:
                lines.append("*No tools found*")
            else:
                for tool in tools_list:
                    readme_badge = "✅" if tool["has_readme"] else "❌"
                    lang = "Python" if tool["python_count"] > 0 else "Bash" if tool["bash_count"] > 0 else "Other"

                    lines.append(f"### {tool['name']}")
                    lines.append("")
                    lines.append(f"- **Language:** {lang}")
                    lines.append(f"- **README:** {readme_badge}")
                    lines.append(f"- **Files:** {tool['python_count'] + tool['bash_count']}")
                    lines.append("")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Export squad data for unified interfaces",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export all data as JSON
  squad-export --include-learnings --include-tools

  # Export specific agents
  squad-export --agents archimedes,marcus

  # Export recent learnings
  squad-export --include-learnings --days 7

  # Export as Markdown
  squad-export --format markdown --output squad.md
        """
    )

    parser.add_argument("--format", choices=["json", "markdown"],
                    default="json", help="Output format (default: json)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--since", help="Filter learnings by date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int,
                    help="Include learnings from last N days")
    parser.add_argument("--agents", help="Comma-separated agent names")
    parser.add_argument("--include-learnings", action="store_true",
                    help="Include learnings in export")
    parser.add_argument("--include-tools", action="store_true",
                    help="Include tool inventory in export")
    parser.add_argument("--workspace", help="Path to workspace")
    parser.add_argument("--learnings", help="Path to learnings directory")

    args = parser.parse_args()

    exporter = SquadExport(args.workspace, args.learnings)

    # Generate export
    if args.format == "json":
        output = exporter.export_json(
            agents=args.agents,
            since=args.since,
            days=args.days,
            include_learnings=args.include_learnings,
            include_tools=args.include_tools
        )
    else:  # markdown
        output = exporter.export_markdown(
            agents=args.agents,
            since=args.since,
            days=args.days,
            include_learnings=args.include_learnings,
            include_tools=args.include_tools
        )

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Exported to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
