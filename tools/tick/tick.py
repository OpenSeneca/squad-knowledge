#!/usr/bin/env python3
"""
tick - Simple CLI task tracker
Track tasks, priorities, and completion status.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

TICK_FILE = Path.home() / ".tick" / "tasks.json"


def load_tasks():
    """Load tasks from file."""
    TICK_FILE.parent.mkdir(parents=True, exist_ok=True)
    if TICK_FILE.exists():
        with open(TICK_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """Save tasks to file."""
    TICK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TICK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title, priority=None, tags=None, description=""):
    """Add a new task."""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority or "medium",
        "tags": tags or [],
        "status": "todo",
        "created": datetime.now().isoformat(),
        "completed": None
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task #{task['id']} added: {title}")
    return task


def list_tasks(filter_status=None, filter_priority=None, filter_tag=None):
    """List all tasks with optional filters."""
    tasks = load_tasks()

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    if filter_priority:
        tasks = [t for t in tasks if t["priority"] == filter_priority]
    if filter_tag:
        tasks = [t for t in tasks if filter_tag.lower() in [tg.lower() for tg in t.get("tags", [])]]

    if not tasks:
        print("❌ No tasks found.")
        return

    print(f"\n📋 {len(tasks)} task(s):\n")

    for task in tasks:
        status_icon = "✓" if task["status"] == "done" else "○"
        priority_color = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }.get(task["priority"], "")

        tags_str = f" [{', '.join(task['tags'])}]" if task.get("tags") else ""
        desc_str = f"\n   {task['description']}" if task.get("description") else ""

        print(f"  {status_icon} #{task['id']}: {task['title']}{tags_str} {priority_color}{desc_str}")


def complete_task(task_id):
    """Mark a task as completed."""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        print(f"❌ Task #{task_id} not found.")
        return False

    if task["status"] == "done":
        print(f"⚠️  Task #{task_id} is already completed.")
        return False

    task["status"] = "done"
    task["completed"] = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"✅ Task #{task_id} completed: {task['title']}")
    return True


def uncomplete_task(task_id):
    """Mark a completed task as todo again."""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        print(f"❌ Task #{task_id} not found.")
        return False

    if task["status"] == "todo":
        print(f"⚠️  Task #{task_id} is already todo.")
        return False

    task["status"] = "todo"
    task["completed"] = None
    save_tasks(tasks)
    print(f"↩️  Task #{task_id} reopened: {task['title']}")
    return True


def update_task(task_id, title=None, priority=None, description=None):
    """Update task details."""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        print(f"❌ Task #{task_id} not found.")
        return False

    if title:
        task["title"] = title
    if priority:
        task["priority"] = priority
    if description is not None:
        task["description"] = description

    save_tasks(tasks)
    print(f"✅ Task #{task_id} updated")
    return True


def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        print(f"❌ Task #{task_id} not found.")
        return False

    tasks.remove(task)
    save_tasks(tasks)
    print(f"🗑️  Task #{task_id} deleted: {task['title']}")
    return True


def show_task(task_id):
    """Show full task details."""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        print(f"❌ Task #{task_id} not found.")
        return

    status_icon = "✓" if task["status"] == "done" else "○"
    priority_color = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }.get(task["priority"], "")

    print(f"\n📋 Task #{task['id']}")
    print(f"   Status: {status_icon} {task['status'].upper()}")
    print(f"   Priority: {priority_color} {task['priority'].upper()}")
    if task.get("tags"):
        print(f"   Tags: {', '.join(task['tags'])}")
    print(f"   Title: {task['title']}")
    if task.get("description"):
        print(f"   Description: {task['description']}")
    print(f"   Created: {task['created']}")
    if task.get("completed"):
        print(f"   Completed: {task['completed']}")


def clear_completed():
    """Delete all completed tasks."""
    tasks = load_tasks()
    completed_count = len([t for t in tasks if t["status"] == "done"])
    tasks = [t for t in tasks if t["status"] != "done"]
    save_tasks(tasks)
    print(f"🧹 Cleared {completed_count} completed task(s)")


def stats():
    """Show task statistics."""
    tasks = load_tasks()

    total = len(tasks)
    done = len([t for t in tasks if t["status"] == "done"])
    todo = total - done
    high = len([t for t in tasks if t["priority"] == "high" and t["status"] == "todo"])
    medium = len([t for t in tasks if t["priority"] == "medium" and t["status"] == "todo"])
    low = len([t for t in tasks if t["priority"] == "low" and t["status"] == "todo"])

    print(f"\n📊 Task Statistics")
    print(f"   Total: {total}")
    print(f"   Done: {done}")
    print(f"   Todo: {todo}")
    print(f"\n   By Priority (todo):")
    print(f"   🔴 High: {high}")
    print(f"   🟡 Medium: {medium}")
    print(f"   🟢 Low: {low}")


def main():
    parser = argparse.ArgumentParser(description="tick - Simple CLI task tracker")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add
    add = subparsers.add_parser("add", help="Add a new task")
    add.add_argument("title", help="Task title")
    add.add_argument("-p", "--priority", choices=["high", "medium", "low"], default="medium", help="Task priority")
    add.add_argument("-t", "--tags", nargs="+", help="Task tags")
    add.add_argument("-d", "--description", help="Task description")

    # List
    list_cmd = subparsers.add_parser("list", help="List tasks")
    list_cmd.add_argument("--status", choices=["todo", "done"], help="Filter by status")
    list_cmd.add_argument("--priority", choices=["high", "medium", "low"], help="Filter by priority")
    list_cmd.add_argument("--tag", help="Filter by tag")

    # Complete
    complete = subparsers.add_parser("done", help="Mark task as completed")
    complete.add_argument("id", type=int, help="Task ID")

    # Uncomplete
    uncomplete = subparsers.add_parser("undo", help="Mark completed task as todo")
    uncomplete.add_argument("id", type=int, help="Task ID")

    # Update
    update = subparsers.add_parser("update", help="Update task details")
    update.add_argument("id", type=int, help="Task ID")
    update.add_argument("-t", "--title", help="New title")
    update.add_argument("-p", "--priority", choices=["high", "medium", "low"], help="New priority")
    update.add_argument("-d", "--description", help="New description")

    # Delete
    delete = subparsers.add_parser("delete", help="Delete a task")
    delete.add_argument("id", type=int, help="Task ID")

    # Show
    show = subparsers.add_parser("show", help="Show task details")
    show.add_argument("id", type=int, help="Task ID")

    # Clear completed
    subparsers.add_parser("clear", help="Delete all completed tasks")

    # Stats
    subparsers.add_parser("stats", help="Show task statistics")

    args = parser.parse_args()

    if not args.command:
        list_tasks()
        return

    if args.command == "add":
        add_task(args.title, args.priority, args.tags, args.description)
    elif args.command == "list":
        list_tasks(args.status, args.priority, args.tag)
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "undo":
        uncomplete_task(args.id)
    elif args.command == "update":
        update_task(args.id, args.title, args.priority, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "show":
        show_task(args.id)
    elif args.command == "clear":
        clear_completed()
    elif args.command == "stats":
        stats()


if __name__ == "__main__":
    main()
