#!/usr/bin/env python3
"""
focus - Work Session and Focus Tracker

Track work sessions, take notes, and manage focus time.

Usage:
  focus start <task>            # Start a new session
  focus note <text>            # Add a note to current session
  focus end                      # End current session
  focus list                      # List all sessions
  focus today                     # Show today's sessions
  focus stats                     # Show session statistics
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
SESSIONS_DIR = Path.home() / '.focus'
CURRENT_SESSION = SESSIONS_DIR / 'current.json'
SESSIONS_LOG = SESSIONS_DIR / 'sessions.json'


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def print_color(color, text):
    """Print colored text."""
    print(f"{color}{text}{Colors.RESET}")


def init_focus_system():
    """Initialize focus system."""
    SESSIONS_DIR.mkdir(exist_ok=True)

    if not SESSIONS_LOG.exists():
        with open(SESSIONS_LOG, 'w') as f:
            json.dump([], f)


def get_current_session() -> dict:
    """Get current active session."""
    if CURRENT_SESSION.exists():
        with open(CURRENT_SESSION) as f:
            return json.load(f)
    return None


def save_current_session(session: dict):
    """Save current session state."""
    with open(CURRENT_SESSION, 'w') as f:
        json.dump(session, f, indent=2)


def start_session(task: str) -> bool:
    """Start a new focus session."""
    print_color(Colors.BOLD, f"\n🎯 Starting Focus Session")
    print("-" * 60)

    # Check if there's an active session
    current = get_current_session()
    if current:
        print_color(Colors.YELLOW, "⚠  A session is already active")
        print(f"  Current task: {current.get('task', 'Unknown')}")
        print(f"  Started at: {current.get('start_time', 'Unknown')}")
        print_color(Colors.CYAN, "\nUse: focus note <text> to add notes")
        print_color(Colors.CYAN, "Use: focus end to finish current session")
        return False

    # Create new session
    session = {
        'task': task,
        'start_time': datetime.now().isoformat(),
        'notes': [],
        'status': 'active',
    }

    save_current_session(session)

    print_color(Colors.GREEN, f"✓ Session started")
    print(f"  Task: {task}")
    print(f"  Started: {session['start_time']}")
    print_color(Colors.CYAN, "\nCommands:")
    print("  focus note <text>  - Add a note")
    print("  focus end           - End session")

    return True


def add_note(note: str) -> bool:
    """Add a note to current session."""
    print_color(Colors.BOLD, f"\n📝 Adding Note")
    print("-" * 60)

    current = get_current_session()
    if not current:
        print_color(Colors.RED, "✗ No active session")
        print_color(Colors.YELLOW, "  Use: focus start <task> to begin")
        return False

    # Add note with timestamp
    note_entry = {
        'text': note,
        'time': datetime.now().isoformat(),
    }

    current['notes'].append(note_entry)
    save_current_session(current)

    print_color(Colors.GREEN, f"✓ Note added")
    print(f"  {note}")

    # Show all notes
    print_color(Colors.CYAN, f"\n📋 Notes in this session ({len(current['notes'])}):")
    for i, note in enumerate(current['notes'], 1):
        time_str = note['time'][11:19]  # HH:MM:SS
        print(f"  {i}. [{time_str}] {note['text']}")

    return True


def end_session() -> bool:
    """End current focus session."""
    print_color(Colors.BOLD, f"\n🏁 Ending Focus Session")
    print("-" * 60)

    current = get_current_session()
    if not current:
        print_color(Colors.RED, "✗ No active session")
        print_color(Colors.YELLOW, "  Use: focus start <task> to begin")
        return False

    # Update session
    end_time = datetime.now()
    duration = (end_time - datetime.fromisoformat(current['start_time'])).total_seconds()

    # Create completed session object
    completed_session = current.copy()
    completed_session['end_time'] = end_time.isoformat()
    completed_session['duration_seconds'] = duration
    completed_session['status'] = 'completed'
    completed_session['duration_human'] = format_duration(duration)

    # Save to log
    # Read existing sessions
    with open(SESSIONS_LOG, 'r') as rf:
        sessions = json.load(rf)

    # Append new session
    sessions.append(completed_session)

    # Write back
    with open(SESSIONS_LOG, 'w') as wf:
        json.dump(sessions, wf, indent=2)

    # Clear current session
    CURRENT_SESSION.unlink()

    print_color(Colors.GREEN, "✓ Session ended")
    print(f"  Task: {current['task']}")
    print(f"  Duration: {completed_session['duration_human']}")
    print(f"  Notes: {len(current['notes'])} taken")
    print(f"  Start: {current['start_time']}")
    print(f"  End: {completed_session['end_time']}")

    return True


def format_duration(seconds: int) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}d {hours}h"


def list_sessions():
    """List all focus sessions."""
    print_color(Colors.BOLD, "\n📋 All Sessions")
    print("-" * 60)

    if not SESSIONS_LOG.exists():
        print_color(Colors.YELLOW, "No sessions recorded")
        return True

    with open(SESSIONS_LOG) as f:
        sessions = json.load(f)

    if not sessions:
        print_color(Colors.YELLOW, "No sessions recorded")
        return True

    # Reverse to show most recent first
    sessions.reverse()

    print(f"\n{'Task':<40} {'Date':<12} {'Duration':<12} {'Notes':<10} {'Status':<10}")
    print("-" * 60)

    for session in sessions:
        task = session.get('task', 'Unknown')[:38]
        date = session.get('start_time', '')[:10]
        duration = session.get('duration_human', 'N/A')
        notes = str(len(session.get('notes', [])))
        status = session.get('status', 'unknown')[:8]

        status_color = Colors.GREEN if status == 'completed' else Colors.YELLOW

        print(f"{task:<40} {date:<12} {duration:<12} {notes:<10} {status_color}{status}{Colors.RESET}")

    return True


def show_today():
    """Show today's sessions."""
    print_color(Colors.BOLD, "\n📅 Today's Sessions")
    print("-" * 60)

    if not SESSIONS_LOG.exists():
        print_color(Colors.YELLOW, "No sessions recorded")
        return True

    with open(SESSIONS_LOG) as f:
        sessions = json.load(f)

    if not sessions:
        print_color(Colors.YELLOW, "No sessions recorded")
        return True

    # Filter for today
    today = datetime.now().date().isoformat()
    today_sessions = [s for s in sessions if s.get('start_time', '').startswith(today)]

    if not today_sessions:
        print_color(Colors.YELLOW, "No sessions today")
        return True

    # Calculate total time
    total_seconds = sum(s.get('duration_seconds', 0) for s in today_sessions)
    total_human = format_duration(int(total_seconds))

    print_color(Colors.GREEN, f"\n✓ {len(today_sessions)} session(s) today")
    print(f"  Total focus time: {total_human}")

    print(f"\n{'Task':<40} {'Duration':<12}")
    print("-" * 60)

    for session in today_sessions:
        task = session.get('task', 'Unknown')[:38]
        duration = session.get('duration_human', 'N/A')
        print(f"{task:<40} {duration:<12}")

    return True


def show_stats():
    """Show session statistics."""
    print_color(Colors.BOLD, "\n📊 Focus Statistics")
    print("-" * 60)

    if not SESSIONS_LOG.exists():
        print_color(Colors.YELLOW, "No sessions recorded")
        return True

    with open(SESSIONS_LOG) as f:
        sessions = json.load(f)

    if not sessions:
        print_color(Colors.YELLOW, "No sessions recorded")
        return True

    # Calculate stats
    total_sessions = len(sessions)
    completed_sessions = sum(1 for s in sessions if s.get('status') == 'completed')
    total_notes = sum(len(s.get('notes', [])) for s in sessions)
    total_duration = sum(s.get('duration_seconds', 0) for s in sessions)
    avg_duration = total_duration / completed_sessions if completed_sessions > 0 else 0

    print(f"\nTotal sessions: {total_sessions}")
    print(f"Completed: {completed_sessions}")
    print(f"Total notes: {total_notes}")
    print(f"Total focus time: {format_duration(int(total_duration))}")
    if completed_sessions > 0:
        print(f"Average duration: {format_duration(int(avg_duration))}")

    # Find most productive day
    daily_totals = {}
    for session in sessions:
        date = session.get('start_time', '')[:10]
        daily_totals[date] = daily_totals.get(date, 0) + session.get('duration_seconds', 0)

    if daily_totals:
        best_day = max(daily_totals.items(), key=lambda x: x[1])
        print(f"\nMost productive day: {best_day[0]} ({format_duration(best_day[1])})")

    return True


def show_current():
    """Show current active session."""
    print_color(Colors.BOLD, "\n🎯 Current Session")
    print("-" * 60)

    current = get_current_session()
    if not current:
        print_color(Colors.YELLOW, "No active session")
        print_color(Colors.CYAN, "\nUse: focus start <task> to begin")
        return True

    task = current.get('task', 'Unknown')
    start_time = current.get('start_time', 'Unknown')
    notes = current.get('notes', [])

    print(f"  Task: {task}")
    print(f"  Started: {start_time}")

    # Calculate current duration
    start_dt = datetime.fromisoformat(start_time)
    duration = (datetime.now() - start_dt).total_seconds()

    print(f"  Duration: {format_duration(int(duration))}")
    print(f"  Notes: {len(notes)}")

    if notes:
        print_color(Colors.CYAN, f"\n📝 Notes:")
        for i, note in enumerate(notes, 1):
            time_str = note['time'][11:19]
            print(f"  {i}. [{time_str}] {note['text']}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Work Session and Focus Tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  focus start "Build squad dashboard"
  focus note "Remember to add error handling"
  focus end
  focus list
  focus today
  focus stats
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # start command
    start_parser = subparsers.add_parser('start', help='Start a new session')
    start_parser.add_argument('task', help='Task or project name')

    # note command
    note_parser = subparsers.add_parser('note', help='Add note to current session')
    note_parser.add_argument('text', help='Note text')

    # end command
    subparsers.add_parser('end', help='End current session')

    # list command
    subparsers.add_parser('list', help='List all sessions')

    # today command
    subparsers.add_parser('today', help="Show today's sessions")

    # stats command
    subparsers.add_parser('stats', help='Show session statistics')

    # current command
    subparsers.add_parser('current', help='Show current active session')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize
    init_focus_system()

    success = False

    if args.command == 'start':
        success = start_session(args.task)
    elif args.command == 'note':
        success = add_note(args.text)
    elif args.command == 'end':
        success = end_session()
    elif args.command == 'list':
        success = list_sessions()
    elif args.command == 'today':
        success = show_today()
    elif args.command == 'stats':
        success = show_stats()
    elif args.command == 'current':
        success = show_current()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
