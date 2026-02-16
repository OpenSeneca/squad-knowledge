#!/usr/bin/env python3
"""
proc — Process Manager

View, search, filter, and manage processes. Enhanced ps alternative.
"""

import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional, Set
import subprocess
import signal
import os
import json
from datetime import datetime


class ProcessManager:
    """Process manager and viewer."""

    def __init__(self):
        self.colors = {
            'pid': '\033[36m',     # Cyan
            'user': '\033[32m',   # Green
            'cpu': '\033[33m',    # Yellow
            'mem': '\033[35m',    # Magenta
            'time': '\033[90m',   # Gray
            'cmd': '\033[37m',    # White
            'header': '\033[1;34m', # Bold Blue
            'reset': '\033[0m',
        }

    def get_processes(self) -> List[Dict]:
        """Get process list."""
        try:
            # Use ps command for comprehensive info
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                timeout=10
            )

            lines = result.stdout.strip().split('\n')
            if not lines:
                return []

            # Parse header and data
            headers = lines[0].split(None, 10)
            processes = []

            for line in lines[1:]:
                parts = line.split(None, 10)
                if len(parts) < 11:
                    continue

                process = {
                    'user': parts[0],
                    'pid': int(parts[1]),
                    'cpu': float(parts[2]),
                    'mem': float(parts[3]),
                    'vsz': int(parts[4]),
                    'rss': int(parts[5]),
                    'tty': parts[6],
                    'stat': parts[7],
                    'start': parts[8],
                    'time': parts[9],
                    'cmd': parts[10] if len(parts) > 10 else '',
                }

                processes.append(process)

            return processes

        except Exception as e:
            print(f"Error getting processes: {e}", file=sys.stderr)
            return []

    def search_processes(self,
                       pattern: str = None,
                       user: str = None,
                       pid: int = None,
                       command: str = None,
                       min_cpu: float = None,
                       min_mem: float = None) -> List[Dict]:
        """Search and filter processes."""
        processes = self.get_processes()
        results = []

        for proc in processes:
            # Pattern match
            if pattern:
                text = f"{proc['user']} {proc['cmd']}"
                if not re.search(pattern, text, re.IGNORECASE):
                    continue

            # User filter
            if user and proc['user'] != user:
                continue

            # PID filter
            if pid and proc['pid'] != pid:
                continue

            # Command filter
            if command and command not in proc['cmd']:
                continue

            # CPU filter
            if min_cpu and proc['cpu'] < min_cpu:
                continue

            # Memory filter
            if min_mem and proc['mem'] < min_mem:
                continue

            results.append(proc)

        return results

    def kill_process(self, pid: int, signal: str = 'SIGTERM') -> bool:
        """Kill a process."""
        try:
            sig = getattr(signal, signal, signal.SIGTERM)
            os.kill(pid, sig)
            return True
        except ProcessLookupError:
            print(f"Process {pid} not found", file=sys.stderr)
            return False
        except PermissionError:
            print(f"Permission denied to kill process {pid}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Error killing process {pid}: {e}", file=sys.stderr)
            return False

    def kill_processes(self, pids: List[int], signal: str = 'SIGTERM') -> Dict:
        """Kill multiple processes."""
        results = {
            'killed': [],
            'failed': [],
        }

        for pid in pids:
            if self.kill_process(pid, signal):
                results['killed'].append(pid)
            else:
                results['failed'].append(pid)

        return results

    def format_process(self, proc: Dict, show_details: bool = False,
                       color: bool = True) -> str:
        """Format process for output."""
        if color:
            pid_str = f"{self.colors['pid']}{proc['pid']}{self.colors['reset']}"
            user_str = f"{self.colors['user']}{proc['user']:<8}{self.colors['reset']}"
            cpu_str = f"{self.colors['cpu']}{proc['cpu']:5.1f}{self.colors['reset']}"
            mem_str = f"{self.colors['mem']}{proc['mem']:5.1f}{self.colors['reset']}"
            time_str = f"{self.colors['time']}{proc['time']:8}{self.colors['reset']}"
            cmd_str = f"{self.colors['cmd']}{proc['cmd'][:80]}{self.colors['reset']}"
        else:
            pid_str = str(proc['pid'])
            user_str = f"{proc['user']:<8}"
            cpu_str = f"{proc['cpu']:5.1f}"
            mem_str = f"{proc['mem']:5.1f}"
            time_str = f"{proc['time']:8}"
            cmd_str = proc['cmd'][:80]

        if show_details:
            return f"{pid_str} {user_str} {cpu_str}% {mem_str}% {time_str} {cmd_str}"
        else:
            return f"{pid_str} {user_str} {cpu_str}% {mem_str}% {time_str} {cmd_str}"

    def print_processes(self, processes: List[Dict], show_details: bool = False,
                      color: bool = True, limit: int = None):
        """Print process list."""
        if not processes:
            print("No processes found")
            return

        # Sort by CPU usage (descending)
        processes = sorted(processes, key=lambda x: x['cpu'], reverse=True)

        # Limit results
        if limit:
            processes = processes[:limit]

        # Print header
        if color:
            header = f"{self.colors['header']}{'PID':>7} {'USER':<8} {'CPU%':>5} {'MEM%':>5} {'TIME':<8} {'COMMAND'}{self.colors['reset']}"
        else:
            header = f"{'PID':>7} {'USER':<8} {'CPU%':>5} {'MEM%':>5} {'TIME':<8} {'COMMAND'}"

        print(header)
        print("-" * 100)

        # Print processes
        for proc in processes:
            print(self.format_process(proc, show_details, color))

    def stats(self, processes: List[Dict]) -> Dict:
        """Calculate process statistics."""
        if not processes:
            return {}

        total_cpu = sum(p['cpu'] for p in processes)
        total_mem = sum(p['mem'] for p in processes)
        users = set(p['user'] for p in processes)

        return {
            'total': len(processes),
            'total_cpu': total_cpu,
            'total_mem': total_mem,
            'users': len(users),
            'avg_cpu': total_cpu / len(processes),
            'avg_mem': total_mem / len(processes),
            'top_cpu': max(processes, key=lambda x: x['cpu']) if processes else None,
            'top_mem': max(processes, key=lambda x: x['mem']) if processes else None,
        }


def main():
    parser = argparse.ArgumentParser(
        description='proc — Process Manager'
    )

    # List options
    parser.add_argument('--top', type=int, metavar='N',
                      help='Show top N processes by CPU')
    parser.add_argument('--search', '-s', metavar='PATTERN',
                      help='Search for processes (regex)')
    parser.add_argument('--user', '-u', metavar='USER',
                      help='Filter by user')
    parser.add_argument('--pid', type=int, metavar='PID',
                      help='Filter by PID')
    parser.add_argument('--command', '-c', metavar='CMD',
                      help='Filter by command')
    parser.add_argument('--min-cpu', type=float, metavar='CPU',
                      help='Filter by minimum CPU %%')
    parser.add_argument('--min-mem', type=float, metavar='MEM',
                      help='Filter by minimum memory %%')

    # Management options
    parser.add_argument('--kill', nargs='+', type=int, metavar='PID',
                      help='Kill process(es) by PID')
    parser.add_argument('--force', action='store_true',
                      help='Force kill (SIGKILL instead of SIGTERM)')

    # Output options
    parser.add_argument('--stats', action='store_true',
                      help='Show statistics')
    parser.add_argument('--json', action='store_true',
                      help='Output as JSON')
    parser.add_argument('--no-color', action='store_true',
                      help='Disable color output')

    args = parser.parse_args()

    manager = ProcessManager()
    color = not args.no_color and sys.stdout.isatty()

    # Kill processes
    if args.kill:
        sig = 'SIGKILL' if args.force else 'SIGTERM'
        results = manager.kill_processes(args.kill, sig)

        print(f"Killed: {len(results['killed'])} process(es)")
        print(f"Failed: {len(results['failed'])} process(es)")

        if results['failed']:
            print(f"Failed PIDs: {', '.join(map(str, results['failed']))}")

        return 0

    # Get processes
    processes = manager.search_processes(
        pattern=args.search,
        user=args.user,
        pid=args.pid,
        command=args.command,
        min_cpu=args.min_cpu,
        min_mem=args.min_mem
    )

    # Statistics
    if args.stats:
        stats = manager.stats(processes)
        print(f"📊 Process Statistics\n")
        print(f"Total processes: {stats['total']}")
        print(f"Total CPU: {stats['total_cpu']:.1f}%")
        print(f"Total Memory: {stats['total_mem']:.1f}%")
        print(f"Unique users: {stats['users']}")
        print(f"Average CPU: {stats['avg_cpu']:.1f}%")
        print(f"Average Memory: {stats['avg_mem']:.1f}%")

        if stats['top_cpu']:
            print(f"\n🔥 Top CPU: PID {stats['top_cpu']['pid']} ({stats['top_cpu']['cpu']:.1f}%)")
        if stats['top_mem']:
            print(f"💾 Top Memory: PID {stats['top_mem']['pid']} ({stats['top_mem']['mem']:.1f}%)")

        return 0

    # JSON output
    if args.json:
        output = []
        for proc in processes:
            output.append(proc)
        print(json.dumps(output, indent=2))
        return 0

    # Print processes
    manager.print_processes(processes, show_details=True, color=color, limit=args.top)

    return 0


if __name__ == '__main__':
    sys.exit(main())
