# prj — Project Scaffolding Tool

Create new projects with best-practice structure, Git config, and documentation.

## Installation

The tool is already symlinked to `~/.local/bin/prj`

```bash
# Verify installation
prj --help
```

## Usage

### List Available Project Types

```bash
prj types
```

### Create a New Project

```bash
# Python project
prj create my-project --type python

# TypeScript project
prj create my-typescript-project --type typescript

# Web project
prj create my-website --type web

# CLI tool
prj create my-cli --type cli

# With custom description
prj create my-project -t python -d "My awesome project"

# Short options
prj create my-project -t typescript -d "Description"
```

### Project Structure

Every project includes:

```
my-project/
├── my-project/          # Source directory (python/typescript)
│   ├── __init__.py     # Python package marker
│   └── main.py         # Entry point
├── .gitignore          # Git ignore patterns
├── README.md           # Project documentation
├── requirements.txt     # Python dependencies
└── .env.example        # Environment template
```

### Getting Started

```bash
# 1. Create project
prj create my-project --type python

# 2. Navigate and setup
cd my-project
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env with your environment variables

# 5. Run
python -m my-project.main
```

## Project Types

### Python
```bash
prj create my-python-app --type python
```

**Includes:**
- Virtual environment setup instructions
- Python package structure (`__init__.py`)
- Main entry point
- `requirements.txt` for dependencies
- `.gitignore` for Python

### TypeScript
```bash
prj create my-ts-app --type typescript
```

**Includes:**
- `tsconfig.json` with best-practice compiler options
- `package.json` with build scripts
- Source directory structure
- `.gitignore` for Node.js/TypeScript

### Web
```bash
prj create my-website --type web
```

**Includes:**
- `index.html` with semantic structure
- `styles.css` with basic reset
- `app.js` entry point
- `.gitignore` for web projects

### CLI
```bash
prj create my-cli --type cli
```

**Includes:**
- `argparse` setup with help/epilog
- Main function with argument handling
- `.gitignore` for Python CLI
- Standard CLI patterns

## Features

### Standard Files

Every project gets:
- **`.gitignore`** — Configured for the project type
- **`README.md`** — Documentation template with setup instructions
- **`.env.example`** — Environment variable template
- **Project-specific files** — Based on project type

### Quick Start

Next steps are printed after project creation:
- Virtual environment setup
- Dependency installation
- Environment configuration
- Running instructions

### Project Types

Choose from 4 project types:
- `python` — Python with virtual env
- `typescript` — TypeScript with build setup
- `web` — HTML/CSS/JS website
- `cli` — Command-line tool with argparse

## Examples

### Create a Web API

```bash
prj create my-api --type python
cd my-api
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
# Edit main.py to add FastAPI code
```

### Create a TypeScript Package

```bash
prj create my-library --type typescript
cd my-library
npm install
npm run dev
```

### Create a CLI Tool

```bash
prj create my-tool --type cli
cd my-tool
python -m venv venv
source venv/bin/activate
pip install click
# Edit main.py to add your CLI logic
```

## Best Practices

### Git Ignore

`.gitignore` includes:
- Virtual environments (`venv/`, `env/`, `node_modules/`)
- Build outputs (`dist/`, `build/`)
- Python cache (`__pycache__/`, `*.pyc`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Sensitive files (`.env`, `*.key`, `*.pem`)

### Environment Variables

`.env.example` template includes:
- API key placeholders
- Debug flags
- Common configuration options
- Clear documentation

### README Documentation

`README.md` includes:
- Installation instructions
- Configuration guide
- Usage examples
- Development guide
- Code style suggestions

## Customization

### Add Your Own Project Type

Edit `prj.py` and add to `PROJECT_TYPES`:

```python
PROJECT_TYPES = {
    "python": {...},
    "typescript": {...},
    "web": {...},
    "cli": {...},
    "my_custom": {
        "description": "Custom project type",
        "files": [
            ("file1.py", "content"),
            ("file2.ts", "content"),
        ]
    }
}
```

### Modify Templates

The templates in `prj.py` are Python f-strings:
- `README_MD` — Documentation template
- `MAIN_PY` — Python entry point
- `GITIGNORE` — Git ignore patterns
- Easy to read and maintain

## Comparison with Other Tools

### agt (Agent Scaffolder)
- **agt**: Creates AI agent projects with role-based templates
- **prj**: Creates general-purpose projects with best practices
- **Use agt for** agents; **Use prj for** general projects

### Cookiecutter
- **Cookiecutter**: Powerful but requires template directory and Jinja2
- **prj**: Simple, single-file tool, no dependencies
- **Use Cookiecutter for** complex templates; **Use prj for** quick starts

### Django/React/etc CLIs
- **Framework CLIs**: Create projects for specific frameworks
- **prj**: General-purpose, works for any project type
- **Use framework CLIs for** framework-specific projects; **Use prj for** general projects

## Best Practices Observed

### From agt
- Template-based scaffolding is clean
- f-strings are simpler than external engines
- README and .env.example are essential

### From Cookiecutter
- Template separation makes code maintainable
- Best practices in templates reduce learning curve
- After-create guidance improves UX

### General Scaffolding
- `.gitignore` must be comprehensive
- README templates should include setup steps
- Virtual environments should be standard
- Environment variables need .example files

## Future Improvements

### 1. More Project Types
- `docker` — Dockerized applications
- `fastapi` — FastAPI web apps
- `react` — React + Vite projects
- `nextjs` — Next.js full-stack

### 2. Interactive Mode
```bash
prj create
# Prompts for name, type, description, etc.
```

### 3. Git Initialization
```bash
prj create my-project --git
# Automatically runs git init
# Adds initial commit
```

### 4. Pre-commit Hooks
```bash
prj create my-project --pre-commit
# Adds .pre-commit-config.yaml
# Installs pre-commit hooks
```

### 5. CI/CD Templates
```bash
prj create my-project --ci github
# Creates .github/workflows/ci.yml
# Sets up GitHub Actions
```

## License

MIT

---

**Ship small, iterate fast** — Create projects with confidence.
