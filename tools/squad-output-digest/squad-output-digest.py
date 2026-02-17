#!/usr/bin/env python3
"""squad-output-digest — Daily output digest for Justin."""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


AGENTS = {
    "seneca": {"name": "Seneca", "role": "Coordinator", "host": "lobster-1"},
    "marcus": {"name": "Marcus", "role": "Research", "host": "marcus-squad"},
    "galen": {"name": "Galen", "role": "Research", "host": "galen-squad"},
    "archimedes": {"name": "Archimedes", "role": "Build", "host": "archimedes-squad"},
    "argus": {"name": "Argus", "role": "Ops", "host": "argus-squad"},
}


def ssh_command(host, command):
    try:
        result = subprocess.run(
            ["ssh", host, command],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout.strip(), None
    except Exception as e:
        return None, str(e)


def get_learnings(agent_id, date):
    agent = AGENTS[agent_id]
    host = agent["host"]
    
    cmd = "ls -t ~/.openclaw/learnings/ 2>/dev/null | head -10"
    if date:
        date_str = date.strftime("%Y-%m-%d")
        cmd = "ls -t ~/.openclaw/learnings/ 2>/dev/null | grep " + date_str + " | head -10"

    output, error = ssh_command(host, cmd)
    if error or not output or "No such file" in output:
        return []
    return [f for f in output.split("\\n") if f.strip()]


def get_outputs(agent_id, date):
    agent = AGENTS[agent_id]
    host = agent["host"]
    
    cmd = "ls -t ~/.openclaw/workspace/outputs/ 2>/dev/null | head -5"
    if date:
        date_str = date.strftime("%Y-%m-%d")
        cmd = "ls -t ~/.openclaw/workspace/outputs/ 2>/dev/null | grep " + date_str + " | head -5"

    output, error = ssh_command(host, cmd)
    if error or not output or "No such file" in output:
        return []
    return [f for f in output.split("\\n") if f.strip()]


def get_memory(agent_id, date):
    agent = AGENTS[agent_id]
    host = agent["host"]
    
    if date:
        date_str = date.strftime("%Y-%m-%d")
        cmd = "ls -t ~/.openclaw/workspace/memory/ 2>/dev/null | grep " + date_str + " | head -1"
    else:
        cmd = "ls -t ~/.openclaw/workspace/memory/ 2>/dev/null | head -1"

    output, error = ssh_command(host, cmd)
    if error or not output:
        return None
    parts = output.split("\\n")
    return parts[0] if parts else None


def generate_digest(date=None, email=False):
    target_date = date or datetime.now()
    print("📊 Squad Output Digest - " + target_date.strftime("%Y-%m-%d") + "\\n")
    
    digest_lines = ["# Squad Output Digest - " + target_date.strftime("%B %d, %Y") + "\\n\\n"]

    for agent_id in AGENTS.keys():
        agent = AGENTS[agent_id]
        name = agent["name"]
        role = agent["role"]

        digest_lines.append("\\n## " + name + " (" + role + ")\\n")

        learnings = get_learnings(agent_id, target_date)
        if learnings:
            digest_lines.append("**Learnings:**\\n")
            for i, learning in enumerate(learnings[:10], 1):
                digest_lines.append("  " + str(i) + ". " + learning + "\\n")
            if len(learnings) > 10:
                digest_lines.append("  ... and " + str(len(learnings) - 10) + " more\\n")
        else:
            digest_lines.append("**Learnings:** None\\n")

        outputs = get_outputs(agent_id, target_date)
        if outputs:
            digest_lines.append("**Outputs:**\\n")
            for i, output in enumerate(outputs[:5], 1):
                digest_lines.append("  " + str(i) + ". " + output + "\\n")
            if len(outputs) > 5:
                digest_lines.append("  ... and " + str(len(outputs) - 5) + " more\\n")
        else:
            digest_lines.append("**Outputs:** None\\n")

        memory_file = get_memory(agent_id, target_date)
        if memory_file:
            digest_lines.append("**Daily Summary:** " + memory_file + "\\n")
        else:
            digest_lines.append("**Daily Summary:** None\\n")

    digest_lines.append("\\n---\\n")
    digest_lines.append("**Generated:** " + datetime.now().strftime("%H:%M UTC") + " on " + target_date.strftime("%Y-%m-%d") + "\\n")
    digest_lines.append("**Total Agents Queried:** " + str(len(AGENTS)) + "\\n")

    return "\\n".join(digest_lines)


def save_digest(content, date):
    if date:
        date_str = date.strftime("%Y-%m-%d")
        filename = "daily-digest-" + date_str + ".md"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = "daily-digest-" + date_str + ".md"

    output_dir = Path.home() / ".openclaw/workspace/outputs"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / filename
    output_path.write_text(content)
    print("✅ Saved: " + str(output_path))
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate daily output digest from all squad agents",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--date", help="Date to generate digest for (YYYY-MM-DD)")
    parser.add_argument("--email", action="store_true", help="Email digest to Justin")

    args = parser.parse_args()

    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format: " + args.date)
            print("   Use YYYY-MM-DD format")
            sys.exit(1)

    content = generate_digest(date=target_date)
    print(content)
    
    save_digest(content, target_date or datetime.now())
    print("\\n📁 Location: " + str(save_digest(content, target_date or datetime.now())))

    if args.email:
        print("📧 Email sending (placeholder)")
        print("   To: Justin (via Seneca)")
        print("   Subject: Squad Digest - " + (target_date or datetime.now()).strftime("%Y-%m-%d"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n⚠️  Digest generation interrupted")
        sys.exit(1)
    except Exception as e:
        print("\\n❌ Error: " + str(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)
