#!/usr/bin/env python3
"""
flow - Development Workflow Orchestrator
Orchestrate tools like prj, agt, tick, snip, crw for streamlined workflows
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import yaml

# Constants
FLOW_DIR = Path.home() / ".flow"
FLOWS_FILE = FLOW_DIR / "flows.json"
WORKFLOW_TEMPLATE = """# Development Workflow Configuration

name: {workflow_name}
description: {workflow_description}

# Workflow stages
stages:
  - id: setup
    name: "Setup Project"
    description: "Initialize project structure"
    commands:
      - tool: prj
        action: create
        args: ["{{project_name}}", "--type", "{{project_type}}"]
      - tool: snip
        action: add
        args: ["{{project_name}}-start", "# {{project_name}} project", "-t", "project"]

  - id: develop
    name: "Development"
    description: "Develop the application"
    commands:
      - tool: tick
        action: add
        args: ["Implement core features for {{project_name}}", "-p", "high"]
      - tool: agt
        action: create
        args: ["{{project_name}}-agent", "--template", "code"]

  - id: test
    name: "Testing"
    description: "Test and validate"
    commands:
      - tool: snip
        action: add
        args: ["{{project_name}}-test", "pytest tests/", "-t", "test"]

  - id: deploy
    name: "Deployment"
    description: "Deploy to production"
    commands:
      - tool: tick
        action: done
        args: ["{{task_id}}"]
"""

def init():
    """Initialize the flow directory structure"""
    FLOW_DIR.mkdir(parents=True, exist_ok=True)
    if not FLOWS_FILE.exists():
        FLOWS_FILE.write_text(json.dumps({}, indent=2))
    print(f"✅ Initialized flow directory: {FLOW_DIR}")

def list_workflows():
    """List all available workflows"""
    if not FLOWS_FILE.exists():
        init()

    flows = json.loads(FLOWS_FILE.read_text())

    if not flows:
        print("📭 No workflows found. Create one with: flow create <name>")
        return

    print(f"📋 Available workflows ({len(flows)}):")
    print()
    for flow_id, flow_info in flows.items():
        print(f"  • {flow_id}")
        print(f"    {flow_info.get('description', 'No description')}")
        print(f"    Stages: {len(flow_info.get('stages', []))}")
        print()

def create_workflow(name, description="", template="default"):
    """Create a new workflow"""
    if not FLOWS_FILE.exists():
        init()

    flows = json.loads(FLOWS_FILE.read_text())

    if name in flows:
        print(f"❌ Workflow '{name}' already exists")
        sys.exit(1)

    # Create workflow directory
    workflow_dir = FLOW_DIR / name
    workflow_dir.mkdir(parents=True, exist_ok=True)

    # Create workflow.yaml
    workflow_yaml = WORKFLOW_TEMPLATE.format(
        workflow_name=name,
        workflow_description=description or f"Auto-generated workflow: {name}"
    )
    (workflow_dir / "workflow.yaml").write_text(workflow_yaml)

    # Register workflow
    flows[name] = {
        "description": description or f"Auto-generated workflow: {name}",
        "created": datetime.now().isoformat(),
        "path": str(workflow_dir),
        "template": template
    }
    FLOWS_FILE.write_text(json.dumps(flows, indent=2))

    print(f"✅ Created workflow: {name}")
    print(f"📂 Location: {workflow_dir}")
    print(f"📝 Config: {workflow_dir / 'workflow.yaml'}")
    print(f"🚀 Run: flow run {name}")

def show_workflow(name):
    """Show workflow details"""
    if not FLOWS_FILE.exists():
        init()

    flows = json.loads(FLOWS_FILE.read_text())

    if name not in flows:
        print(f"❌ Workflow '{name}' not found")
        sys.exit(1)

    flow_info = flows[name]
    workflow_dir = Path(flow_info["path"])

    print(f"📋 Workflow: {name}")
    print(f"📝 {flow_info['description']}")
    print(f"📅 Created: {flow_info['created']}")
    print(f"📂 Location: {workflow_dir}")
    print()

    # Show workflow.yaml contents
    workflow_yaml = workflow_dir / "workflow.yaml"
    if workflow_yaml.exists():
        print("📄 Configuration (workflow.yaml):")
        print("-" * 60)
        try:
            config = yaml.safe_load(workflow_yaml.read_text())
            print(f"Name: {config.get('name', 'N/A')}")
            print(f"Stages: {len(config.get('stages', []))}")
            print()
            print("Stages:")
            for stage in config.get('stages', []):
                commands = stage.get('commands', [])
                print(f"  • {stage.get('name')} ({stage.get('id')})")
                print(f"    {stage.get('description')}")
                print(f"    Commands: {len(commands)}")
        except Exception as e:
            print(f"⚠️  Error parsing YAML: {e}")

def run_workflow(name, dry_run=False):
    """Run a workflow"""
    if not FLOWS_FILE.exists():
        init()

    flows = json.loads(FLOWS_FILE.read_text())

    if name not in flows:
        print(f"❌ Workflow '{name}' not found")
        sys.exit(1)

    workflow_dir = Path(flows[name]["path"])
    workflow_yaml = workflow_dir / "workflow.yaml"

    if not workflow_yaml.exists():
        print(f"❌ Workflow configuration not found: {workflow_yaml}")
        sys.exit(1)

    print(f"🚀 Running workflow: {name}")
    if dry_run:
        print("🔍 Dry run mode - showing commands without executing")
    print()

    try:
        config = yaml.safe_load(workflow_yaml.read_text())
        stages = config.get('stages', [])

        for stage in stages:
            print(f"\n📍 Stage: {stage.get('name')} ({stage.get('id')})")
            print(f"   {stage.get('description')}")
            print()

            commands = stage.get('commands', [])
            for i, cmd in enumerate(commands, 1):
                tool = cmd.get('tool')
                action = cmd.get('action')
                args = cmd.get('args', [])

                # Build command
                cmd_str = f"{tool} {action}"
                if args:
                    cmd_str += f" {' '.join(str(a) for a in args)}"

                print(f"   {i}. {cmd_str}")

                if not dry_run:
                    # Execute command
                    try:
                        result = subprocess.run(
                            cmd_str,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if result.returncode != 0:
                            print(f"      ⚠️  Command failed: {result.stderr}")
                    except subprocess.TimeoutExpired:
                        print(f"      ⚠️  Command timed out")
                    except Exception as e:
                        print(f"      ⚠️  Error: {e}")

        print(f"\n✅ Workflow '{name}' complete!" if not dry_run else f"\n✅ Dry run complete!")
    except Exception as e:
        print(f"❌ Error running workflow: {e}")
        sys.exit(1)

def delete_workflow(name):
    """Delete a workflow"""
    if not FLOWS_FILE.exists():
        init()

    flows = json.loads(FLOWS_FILE.read_text())

    if name not in flows:
        print(f"❌ Workflow '{name}' not found")
        sys.exit(1)

    # Remove workflow directory
    workflow_dir = Path(flows[name]["path"])
    if workflow_dir.exists():
        subprocess.run(["rm", "-rf", str(workflow_dir)])

    # Remove from registry
    del flows[name]
    FLOWS_FILE.write_text(json.dumps(flows, indent=2))

    print(f"🗑️  Deleted workflow: {name}")

def main():
    parser = argparse.ArgumentParser(
        description="flow - Development Workflow Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  flow init               Initialize flow directory
  flow create my-flow     Create a new workflow
  flow list               List all workflows
  flow show my-flow       Show workflow details
  flow run my-flow        Run a workflow
  flow run my-flow --dry-run  Show commands without executing
  flow delete my-flow     Delete a workflow

Workflow Configuration:
Workflows are defined in ~/.flow/<name>/workflow.yaml
Each workflow has stages with commands that use tools like:
  prj  - Project scaffolding
  agt  - Agent scaffolding
  tick - Task tracking
  snip - Snippet management
  crw  - Crew orchestration
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    subparsers.add_parser("init", help="Initialize flow directory")

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new workflow")
    create_parser.add_argument("name", help="Workflow name")
    create_parser.add_argument("-d", "--description", help="Workflow description")
    create_parser.add_argument("-t", "--template", default="default", help="Workflow template")

    # list command
    subparsers.add_parser("list", help="List all workflows")

    # show command
    show_parser = subparsers.add_parser("show", help="Show workflow details")
    show_parser.add_argument("name", help="Workflow name")

    # run command
    run_parser = subparsers.add_parser("run", help="Run a workflow")
    run_parser.add_argument("name", help="Workflow name")
    run_parser.add_argument("--dry-run", action="store_true", help="Show commands without executing")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a workflow")
    delete_parser.add_argument("name", help="Workflow name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == "init":
        init()
    elif args.command == "create":
        create_workflow(args.name, args.description, args.template)
    elif args.command == "list":
        list_workflows()
    elif args.command == "show":
        show_workflow(args.name)
    elif args.command == "run":
        run_workflow(args.name, args.dry_run)
    elif args.command == "delete":
        delete_workflow(args.name)

if __name__ == "__main__":
    main()
