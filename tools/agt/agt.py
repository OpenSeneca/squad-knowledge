#!/usr/bin/env python3
"""
Agent Scaffolding Tool (agt)

Create new AI agent projects with best-practice structure.
Inspired by CrewAI and modern agent frameworks.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Templates
AGENT_PY = '''"""{agent_name} Agent

A {description} agent built with the agent framework.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class {class_name}(ABC):
    """
    Base class for {agent_name} agents.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {{}}
        self.agent_name = "{agent_name}"
        self.role = "{role}"
        self.description = "{description}"

    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input data and return results.

        Args:
            input_data: The input to process

        Returns:
            Dict containing results
        """
        pass

    def get_config(self) -> Dict[str, Any]:
        """Get agent configuration."""
        return {{
            "name": self.agent_name,
            "role": self.role,
            "description": self.description,
            "config": self.config
        }}

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the agent.

        Returns:
            Dict with health status
        """
        return {{
            "status": "healthy",
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat()
        }}


class {class_name}Impl({class_name}):
    """
    Concrete implementation of {agent_name} agent.
    """

    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input and return results.

        TODO: Implement your agent logic here
        """
        result = {{
            "status": "success",
            "agent": self.agent_name,
            "input": input_data,
            "output": "Processed result"
        }}

        return result
'''

MAIN_PY = '''"""Main entry point for {project_name}"""

import asyncio
from {project_name}.{agent_module} import {class_name}Impl
from {project_name}.config import Config


async def main():
    """Main function."""
    config = Config()

    # Initialize agent
    agent = {class_name}Impl(config.get_agent_config())

    # Process input
    input_data = {{"message": "Hello, {agent_name}!"}}

    try:
        result = await agent.process(input_data)
        print(f"Result: {{result}}")
    except Exception as e:
        print(f"Error: {{e}}")


if __name__ == "__main__":
    asyncio.run(main())
'''

CONFIG_PY = '''"""Configuration for {project_name}"""

import os
from typing import Dict, Any
from pathlib import Path


class Config:
    """Configuration management."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.load_env()

    def load_env(self):
        """Load environment variables."""
        # TODO: Load your environment variables
        pass

    def get_agent_config(self) -> Dict[str, Any]:
        """Get agent configuration."""
        return {{
            "model": os.getenv("MODEL", "gpt-4"),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("MAX_TOKENS", "2000")),
        }}

    def get_api_keys(self) -> Dict[str, str]:
        """Get API keys."""
        return {{
            "openai": os.getenv("OPENAI_API_KEY"),
            # Add more API keys as needed
        }}
'''

README_MD = '''# {project_name}

{description}

## Getting Started

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:

```bash
MODEL=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=2000
OPENAI_API_KEY=your_api_key_here
```

### Running

```bash
python -m {project_name}.main
```

## Project Structure

```
{project_name}/
├── {project_name}/
│   ├── __init__.py
│   ├── agent.py     # Agent implementation
│   ├── config.py    # Configuration
│   └── main.py     # Entry point
├── tests/
│   ├── __init__.py
│   └── test_agent.py
├── requirements.txt
├── README.md
└── .env.example
```

## Development

### Adding Tools

Create new tools in the `tools/` directory:

```python
from typing import Any

async def my_tool(input_data: Any) -> Dict[str, Any]:
    # Your tool logic here
    return {{"result": "success"}}
```

### Testing

```bash
pytest tests/
```

## License

MIT
'''

REQUIREMENTS_TXT = '''# Core dependencies
python-dotenv>=1.0.0
pydantic>=2.0.0

# Optional: Add LLM providers
# openai>=1.0.0
# anthropic>=0.18.0
'''

ENV_EXAMPLE = '''# API Configuration
MODEL=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=2000

# API Keys
OPENAI_API_KEY=your_api_key_here
'''

TEST_PY = '''"""Tests for {project_name}"""

import pytest
from {project_name}.{agent_module} import {class_name}Impl


@pytest.mark.asyncio
async def test_agent_process():
    """Test agent processing."""
    agent = {class_name}Impl({{}})

    result = await agent.process({{"test": "data"}})

    assert result["status"] == "success"
    assert "output" in result


@pytest.mark.asyncio
async def test_agent_health():
    """Test agent health check."""
    agent = {class_name}Impl({{}})

    health = await agent.health_check()

    assert health["status"] == "healthy"
    assert "agent" in health
'''

# Predefined agent templates
AGENT_TEMPLATES = {
    "research": {
        "role": "Research",
        "description": "AI agent for research and analysis tasks"
    },
    "code": {
        "role": "Code",
        "description": "AI agent for code generation and debugging"
    },
    "writer": {
        "role": "Writer",
        "description": "AI agent for content creation"
    },
    "analyst": {
        "role": "Analyst",
        "description": "AI agent for data analysis"
    },
    "custom": {
        "role": "Custom",
        "description": "Custom AI agent for your needs"
    }
}


def create_project(name: str, template: str = "custom", description: str = None):
    """Create a new agent project."""
    if template not in AGENT_TEMPLATES:
        print(f"❌ Invalid template. Choose from: {', '.join(AGENT_TEMPLATES.keys())}")
        return

    # Get template data
    template_data = AGENT_TEMPLATES[template]
    agent_name = name.title().replace("-", " ").replace("_", " ")
    class_name = "".join(word.capitalize() for word in name.split("-") + ["Agent"])
    agent_module = name.lower().replace("-", "_")

    # Override description if provided
    desc = description or template_data["description"]

    # Create project structure
    project_dir = Path(name)
    project_dir.mkdir(exist_ok=True)

    # Create directories
    (project_dir / name).mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)

    # Create __init__ files
    (project_dir / name / "__init__.py").touch()
    (project_dir / "tests" / "__init__.py").touch()

    # Write files
    files = {
        f"{name}/agent.py": AGENT_PY.format(
            agent_name=agent_name,
            class_name=class_name,
            description=desc,
            role=template_data["role"]
        ),
        f"{name}/config.py": CONFIG_PY.format(project_name=name),
        f"{name}/main.py": MAIN_PY.format(
            project_name=name,
            agent_name=agent_name,
            agent_module="agent",
            class_name=class_name
        ),
        "requirements.txt": REQUIREMENTS_TXT,
        "README.md": README_MD.format(
            project_name=name,
            description=desc
        ),
        ".env.example": ENV_EXAMPLE,
        "tests/test_agent.py": TEST_PY.format(
            project_name=name,
            agent_module="agent",
            class_name=class_name
        ),
    }

    for file_path, content in files.items():
        full_path = project_dir / file_path
        full_path.write_text(content)

    print(f"✅ Project '{name}' created successfully!")
    print(f"\n📁 Location: {project_dir.absolute()}")
    print(f"\n🚀 Next steps:")
    print(f"   cd {name}")
    print(f"   python -m venv venv")
    print(f"   source venv/bin/activate  # On Windows: venv\\\\Scripts\\\\activate")
    print(f"   pip install -r requirements.txt")
    print(f"   cp .env.example .env")
    print(f"   # Edit .env with your API keys")
    print(f"   python -m {name}.main")


def list_templates():
    """List available agent templates."""
    print("📋 Available Agent Templates:")
    print()
    for key, data in AGENT_TEMPLATES.items():
        print(f"  • {key:10} - {data['role']}: {data['description']}")
    print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Agent scaffolding tool - Create AI agent projects",
        epilog="Example: agt create my-research-agent --template research"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new agent project")
    create_parser.add_argument(
        "name",
        help="Project name (e.g., my-agent)"
    )
    create_parser.add_argument(
        "-t", "--template",
        choices=list(AGENT_TEMPLATES.keys()),
        default="custom",
        help="Agent template to use (default: custom)"
    )
    create_parser.add_argument(
        "-d", "--description",
        help="Custom description for the agent"
    )

    # Templates command
    subparsers.add_parser("templates", help="List available agent templates")

    args = parser.parse_args()

    if args.command == "create":
        create_project(args.name, args.template, args.description)
    elif args.command == "templates":
        list_templates()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
