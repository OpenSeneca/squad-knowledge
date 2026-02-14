#!/usr/bin/env python3
"""
Project Scaffolding Tool (prj)

Create new projects with best-practice structure, Git config, and documentation.
Fast, clean, production-ready.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Templates
GITIGNORE = '''# Dependencies
node_modules/
venv/
env/
.venv/
__pycache__/
*.py[cod]
*$py.class
*.so

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Build outputs
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
*.key
*.pem

# OS
.DS_Store
Thumbs.db
'''

README_MD = f'''# {{project_name}}

{{description}}

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```bash
# Add your environment variables here
API_KEY=your_api_key_here
```

## Usage

```bash
python -m {{project_name}}.main
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
# Python
black .

# TypeScript (if using)
npm run lint
```

## License

MIT

## Author

Your Name <your.email@example.com>
'''

REQUIREMENTS_TXT = '''# Dependencies
# Add your project dependencies here
'''

ENV_EXAMPLE = '''# Environment Variables
# Copy this file to .env and add your values

# Example configuration
API_KEY=your_api_key_here
DEBUG=false
'''

MAIN_PY = f'''"""Main entry point for {{project_name}}"""

def main():
    """Main function."""
    print("Hello, {{project_name}}!")
    # TODO: Implement your main logic here


if __name__ == "__main__":
    main()
'''

PROJECT_TYPES = {
    "python": {
        "description": "Python project with virtual env setup",
        "files": [
            ("__init__.py", ""),
            ("main.py", MAIN_PY),
        ]
    },
    "typescript": {
        "description": "TypeScript project with build setup",
        "files": [
            ("index.ts", "console.log('Hello, {{project_name}}!');"),
            ("tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
"""),
            ("package.json", """{
  "name": "{{project_name}}",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "start": "node dist/index.js"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
"""),
        ]
    },
    "web": {
        "description": "Web project with HTML/CSS/JS",
        "files": [
            ("index.html", f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{project_name}}}}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Hello, {{{{project_name}}}}!</h1>
    <script src="app.js"></script>
</body>
</html>
'''),
            ("styles.css", """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    line-height: 1.5;
}
"""),
            ("app.js", f"""console.log('Hello, {{{{project_name}}}}!');

// Add your JavaScript here
"""),
        ]
    },
    "cli": {
        "description": "CLI tool with argparse",
        "files": [
            ("main.py", f'''#!/usr/bin/env python3
"""{{{{project_name}}}} - CLI tool

A command-line tool for {{{{project_name}}}}.
"""\n\nimport argparse\nimport sys\n\n\ndef main():\n    """Main function."""\n    parser = argparse.ArgumentParser(\n        description="{{{{project_name}}}} - CLI tool",\n        epilog="Example: python main.py --help"\n    )\n\n    parser.add_argument(\n        "--verbose", "-v",\n        action="store_true",\n        help="Enable verbose output"\n    )\n\n    args = parser.parse_args()\n\n    if args.verbose:\n        print("Verbose mode enabled")\n\n    print("Hello, {{{{project_name}}}}!")\n\n\nif __name__ == "__main__":\n    main()\n'''),
        ]
    },
}


def create_project(name: str, project_type: str = "python", description: str = None):
    """Create a new project."""
    if project_type not in PROJECT_TYPES:
        print(f"❌ Invalid project type. Choose from: {', '.join(PROJECT_TYPES.keys())}")
        return

    # Get project type data
    type_data = PROJECT_TYPES[project_type]
    desc = description or f"A {project_type} project"

    # Create project directory
    project_dir = Path(name)
    project_dir.mkdir(exist_ok=True)

    # Create src directory if python/typescript
    src_dir = project_dir / name if project_type in ["python", "typescript"] else project_dir
    if project_type in ["python", "typescript"]:
        src_dir.mkdir(exist_ok=True)

    # Create common files
    common_files = {
        ".gitignore": GITIGNORE,
        "README.md": README_MD,
        "requirements.txt": REQUIREMENTS_TXT if project_type == "python" else None,
        ".env.example": ENV_EXAMPLE,
    }

    for filename, content in common_files.items():
        if content:
            (project_dir / filename).write_text(content)

    # Create project-specific files
    for filename, content in type_data["files"]:
        file_path = src_dir / filename
        if isinstance(content, str):
            file_path.write_text(content)

    print(f"✅ Project '{name}' created successfully!")
    print(f"\n📁 Location: {project_dir.absolute()}")
    print(f"\n🚀 Next steps:")
    print(f"   cd {name}")
    if project_type == "python":
        print(f"   python -m venv venv")
        print(f"   source venv/bin/activate")
        print(f"   pip install -r requirements.txt")
        print(f"   # Edit .env with your environment variables")
    elif project_type == "typescript":
        print(f"   npm install")
        print(f"   npm run dev")
        print(f"   # Edit .env with your environment variables")
    elif project_type == "web":
        print(f"   # Open index.html in your browser")


def list_types():
    """List available project types."""
    print("📋 Available Project Types:")
    print()
    for key, data in PROJECT_TYPES.items():
        print(f"  • {key:10} - {data['description']}")
    print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Project scaffolding tool - Create new projects with best practices",
        epilog="Example: prj create my-project --type python"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument(
        "name",
        help="Project name (e.g., my-project)"
    )
    create_parser.add_argument(
        "-t", "--type",
        choices=list(PROJECT_TYPES.keys()),
        default="python",
        help="Project type to create (default: python)"
    )
    create_parser.add_argument(
        "-d", "--description",
        help="Custom description for the project"
    )

    # Types command
    subparsers.add_parser("types", help="List available project types")

    args = parser.parse_args()

    if args.command == "create":
        create_project(args.name, args.type, args.description)
    elif args.command == "types":
        list_types()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
