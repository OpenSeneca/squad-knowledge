#!/usr/bin/env python3
"""
crew - CrewAI Execution Engine
Run and manage AI crews created with crw
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Constants
CREW_DIR = Path.home() / ".crew"
CREWS_FILE = CREW_DIR / "crews.json"

def list_crews():
    """List all available crews"""
    if not CREW_DIR.exists():
        print("❌ No crew directory found. Run 'crw init' first.")
        sys.exit(1)

    if not CREWS_FILE.exists():
        print("❌ No crews registry found. Run 'crw init' first.")
        sys.exit(1)

    crews = json.loads(CREWS_FILE.read_text())

    if not crews:
        print("📭 No crews found. Create one with: crw create <name>")
        return

    print(f"📋 Available crews ({len(crews)}):")
    print()
    for crew_id, crew_info in crews.items():
        crew_dir = Path(crew_info["path"])
        crew_yaml = crew_dir / "crew.yaml"

        status = "✅ Ready" if crew_yaml.exists() else "⚠️  Missing config"

        print(f"  • {crew_id}")
        print(f"    {crew_info.get('description', 'No description')}")
        print(f"    Status: {status}")
        print(f"    Path: {crew_dir}")
        print()

def simulate_crew(name: str, verbose: bool = False):
    """Simulate crew execution (without CrewAI)"""
    if not CREW_DIR.exists():
        print("❌ No crew directory found")
        sys.exit(1)

    if not CREWS_FILE.exists():
        print("❌ No crews registry found")
        sys.exit(1)

    crews = json.loads(CREWS_FILE.read_text())

    if name not in crews:
        print(f"❌ Crew '{name}' not found")
        sys.exit(1)

    crew_dir = Path(crews[name]["path"])
    crew_yaml = crew_dir / "crew.yaml"

    if not crew_yaml.exists():
        print(f"❌ Crew configuration not found: {crew_yaml}")
        sys.exit(1)

    # Read and parse YAML
    try:
        import yaml
        config = yaml.safe_load(crew_yaml.read_text())
    except ImportError:
        print("❌ PyYAML not installed. Install with: pip install pyyaml")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading crew.yaml: {e}")
        sys.exit(1)

    # Display crew info
    print(f"🚀 Simulating crew execution: {name}")
    print(f"📝 Description: {config.get('name', name)}")
    print()

    # Display agents
    agents = config.get('agents', [])
    print(f"👥 Agents ({len(agents)}):")
    for agent in agents:
        print(f"  • {agent.get('name')} ({agent.get('role')})")
        if verbose:
            print(f"      Goal: {agent.get('goal')}")
            print(f"      LLM: {agent.get('llm', 'default')}")
            print(f"      Tools: {len(agent.get('tools', []))}")
    print()

    # Display tasks
    tasks = config.get('tasks', [])
    print(f"📋 Tasks ({len(tasks)}):")
    for task in tasks:
        agent_id = task.get('agent', 'unknown')
        agent_name = next((a.get('name') for a in agents if a.get('id') == agent_id), agent_id)
        deps = task.get('depends_on', [])
        deps_str = f" (depends on: {', '.join(deps)})" if deps else ""

        print(f"  • {task.get('name')} - {agent_name}{deps_str}")
        if verbose:
            print(f"      Description: {task.get('description')}")
            print(f"      Expected: {task.get('expected_output', 'N/A')}")
    print()

    # Display execution mode
    execution = config.get('execution', {})
    process = execution.get('process', 'sequential')
    print(f"⚙️  Execution mode: {process}")
    if verbose:
        print(f"   Manager LLM: {execution.get('manager_llm', 'default')}")
        print(f"   Verbose: {execution.get('verbose', True)}")
    print()

    # Simulate execution
    print("🔄 Executing tasks...")
    print()

    # Determine execution order
    task_map = {t.get('id'): t for t in tasks}

    def get_task_order(task_id: str, visited: set) -> list:
        """Get tasks in dependency order"""
        if task_id in visited:
            return []
        visited.add(task_id)

        task = task_map.get(task_id)
        if not task:
            return []

        order = []
        for dep in task.get('depends_on', []):
            order.extend(get_task_order(dep, visited))
        order.append(task_id)
        return order

    # Get all task IDs in order
    ordered_tasks = []
    visited = set()
    for task_id in task_map:
        ordered_tasks.extend(get_task_order(task_id, visited))

    # Remove duplicates while preserving order
    seen = set()
    ordered_tasks = [t for t in ordered_tasks if not (t in seen or seen.add(t))]

    # Execute tasks
    output_dir = crew_dir / "output"
    output_dir.mkdir(exist_ok=True)

    for i, task_id in enumerate(ordered_tasks, 1):
        task = task_map[task_id]
        agent_id = task.get('agent')
        agent = next((a for a in agents if a.get('id') == agent_id), None)

        print(f"[{i}/{len(ordered_tasks)}] {task.get('name')}")
        print(f"    Agent: {agent.get('name') if agent else 'Unknown'}")
        print(f"    Status: Executing...")

        # Simulate output
        output_file = output_dir / f"{task_id}.txt"
        output_content = f"""Task: {task.get('name')}
Agent: {agent.get('name') if agent else 'Unknown'}
Description: {task.get('description')}
Expected Output: {task.get('expected_output', 'N/A')}
Timestamp: {datetime.now().isoformat()}

Note: This is a simulation. Install CrewAI for real execution:
pip install crewai
"""
        output_file.write_text(output_content)

        print(f"    Status: ✅ Complete")
        print(f"    Output: {output_file}")
        print()

    print(f"✅ Crew '{name}' execution complete!")
    print(f"📂 Output directory: {output_dir}")

def run_crew(name: str, verbose: bool = False):
    """Run crew with CrewAI (if installed)"""
    try:
        # Check if CrewAI is available
        import crewai
        print(f"✅ CrewAI detected, running '{name}'...")
        # Real implementation would go here
        print("⚠️  Full CrewAI integration pending development")
        print("   Use 'crew simulate' to preview crew structure")
    except ImportError:
        print("⚠️  CrewAI not installed")
        print()
        print("Install CrewAI with: pip install crewai")
        print()
        print("For now, use simulation mode:")
        print(f"   crew simulate {name}")

def validate_crew(name: str):
    """Validate crew configuration"""
    if not CREW_DIR.exists():
        print("❌ No crew directory found")
        sys.exit(1)

    if not CREWS_FILE.exists():
        print("❌ No crews registry found")
        sys.exit(1)

    crews = json.loads(CREWS_FILE.read_text())

    if name not in crews:
        print(f"❌ Crew '{name}' not found")
        sys.exit(1)

    crew_dir = Path(crews[name]["path"])
    crew_yaml = crew_dir / "crew.yaml"

    if not crew_yaml.exists():
        print(f"❌ Crew configuration not found: {crew_yaml}")
        sys.exit(1)

    # Read and parse YAML
    try:
        import yaml
        config = yaml.safe_load(crew_yaml.read_text())
    except ImportError:
        print("⚠️  PyYAML not installed")
        sys.exit(1)

    errors = []
    warnings = []

    # Validate structure
    if 'agents' not in config:
        errors.append("Missing 'agents' section")
    elif not isinstance(config['agents'], list):
        errors.append("'agents' must be a list")

    if 'tasks' not in config:
        errors.append("Missing 'tasks' section")
    elif not isinstance(config['tasks'], list):
        errors.append("'tasks' must be a list")

    # Validate agents
    agent_ids = set()
    for i, agent in enumerate(config.get('agents', [])):
        if 'id' not in agent:
            errors.append(f"Agent {i}: missing 'id'")
        else:
            agent_id = agent['id']
            if agent_id in agent_ids:
                errors.append(f"Duplicate agent ID: {agent_id}")
            agent_ids.add(agent_id)

        if 'name' not in agent:
            errors.append(f"Agent {i}: missing 'name'")

    # Validate tasks
    task_ids = set()
    for i, task in enumerate(config.get('tasks', [])):
        if 'id' not in task:
            errors.append(f"Task {i}: missing 'id'")
        else:
            task_id = task['id']
            if task_id in task_ids:
                errors.append(f"Duplicate task ID: {task_id}")
            task_ids.add(task_id)

        if 'name' not in task:
            errors.append(f"Task {i}: missing 'name'")

        if 'agent' not in task:
            errors.append(f"Task {i}: missing 'agent'")
        elif task['agent'] not in agent_ids:
            errors.append(f"Task {i}: agent '{task['agent']}' not defined")

        # Validate dependencies
        for dep in task.get('depends_on', []):
            if dep not in task_ids:
                errors.append(f"Task {i}: dependency '{dep}' not found")

    # Display results
    if errors:
        print(f"❌ Validation failed: {len(errors)} error(s)")
        print()
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)
    else:
        print(f"✅ Crew '{name}' is valid!")
        print()
        print(f"👥 Agents: {len(config.get('agents', []))}")
        print(f"📋 Tasks: {len(config.get('tasks', []))}")
        print(f"⚙️  Execution: {config.get('execution', {}).get('process', 'sequential')}")

def export_python(name: str, output: str = None):
    """Export crew to Python script"""
    if not CREW_DIR.exists():
        print("❌ No crew directory found")
        sys.exit(1)

    if not CREWS_FILE.exists():
        print("❌ No crews registry found")
        sys.exit(1)

    crews = json.loads(CREWS_FILE.read_text())

    if name not in crews:
        print(f"❌ Crew '{name}' not found")
        sys.exit(1)

    crew_dir = Path(crews[name]["path"])
    crew_yaml = crew_dir / "crew.yaml"

    if not crew_yaml.exists():
        print(f"❌ Crew configuration not found: {crew_yaml}")
        sys.exit(1)

    # Read and parse YAML
    try:
        import yaml
        config = yaml.safe_load(crew_yaml.read_text())
    except ImportError:
        print("❌ PyYAML not installed")
        sys.exit(1)

    # Generate Python script
    agents_code = []
    for agent in config.get('agents', []):
        agents_code.append(f'''
agents['{agent['id']}'] = Agent(
    role="{agent['role']}",
    goal="{agent['goal']}",
    backstory="{agent.get('backstory', '')}",
    verbose={agent.get('verbose', True)}
)
''')

    tasks_code = []
    for task in config.get('tasks', []):
        deps = task.get('depends_on', [])
        if deps:
            deps_list = '[' + ', '.join([f"tasks['{dep}']" for dep in deps]) + ']'
        else:
            deps_list = '[]'

        tasks_code.append(f'''
tasks['{task['id']}'] = Task(
    description="{task['description']}",
    expected_output="{task.get('expected_output', '')}",
    agent=agents['{task['agent']}'],
    context={deps_list}
)
''')

    script = f'''#!/usr/bin/env python3
"""
CrewAI Crew: {name}
Generated from crew.yaml on {datetime.now().isoformat()}
"""

from crewai import Agent, Task, Crew, Process

# Define Agents
{''.join(agents_code)}

# Define Tasks
{''.join(tasks_code)}

# Create Crew
crew = Crew(
    agents=list(agents.values()),
    tasks=list(tasks.values()),
    process=Process.{config.get('execution', {}).get('process', 'sequential').lower()},
    verbose=True
)

# Run Crew
result = crew.kickoff()
print(result)
'''

    if output:
        Path(output).write_text(script)
        print(f"✅ Exported crew to: {output}")
    else:
        print(script)

def main():
    parser = argparse.ArgumentParser(
        description="crew - CrewAI Execution Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  crew list               List all crews
  crew simulate my-crew   Simulate crew execution
  crew run my-crew        Run crew with CrewAI
  crew validate my-crew    Validate crew configuration
  crew export my-crew      Export to Python script
  crew export my-crew -o crew.py
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    subparsers.add_parser("list", help="List all crews")

    # simulate command
    simulate_parser = subparsers.add_parser("simulate", help="Simulate crew execution")
    simulate_parser.add_argument("name", help="Crew name")
    simulate_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # run command
    run_parser = subparsers.add_parser("run", help="Run crew with CrewAI")
    run_parser.add_argument("name", help="Crew name")
    run_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate crew configuration")
    validate_parser.add_argument("name", help="Crew name")

    # export command
    export_parser = subparsers.add_parser("export", help="Export crew to Python")
    export_parser.add_argument("name", help="Crew name")
    export_parser.add_argument("-o", "--output", help="Output file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == "list":
        list_crews()
    elif args.command == "simulate":
        simulate_crew(args.name, args.verbose)
    elif args.command == "run":
        run_crew(args.name, args.verbose)
    elif args.command == "validate":
        validate_crew(args.name)
    elif args.command == "export":
        export_python(args.name, args.output)

if __name__ == "__main__":
    main()
