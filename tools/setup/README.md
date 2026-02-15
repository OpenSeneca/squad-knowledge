# setup — Project Setup Automation Tool

Generate and execute setup scripts for projects created with `prj` and `agt`.

## Installation

```bash
# Link to PATH
ln -s $(pwd)/setup.sh ~/.local/bin/setup

# Or add to PATH manually
export PATH="$PATH:$(pwd)"
```

## Usage

### Initialize Setup in a Project

```bash
cd my-project
setup init
```

Creates `setup.json` with configuration template.

### Generate Setup Script

```bash
setup generate
```

Detects project type and generates `setup-generated.sh`.

Supported project types:
- Python (requirements.txt, pyproject.toml)
- Node.js (package.json)
- Go (go.mod)
- Rust (Cargo.toml)
- Generic

### Execute Setup

```bash
setup run
```

Runs the generated setup script.

### Check Status

```bash
setup status
```

Shows what has been set up in the current project.

### Clean Up

```bash
setup clean
```

Removes generated setup files.

## Example Workflow

```bash
# Create a new project
prj create my-tool --type python
cd my-tool

# Initialize setup
setup init

# Generate setup script
setup generate

# Run setup
setup run

# Check status
setup status
```

## Features

- Auto-detects project type
- Creates virtual environments (Python)
- Installs dependencies automatically
- Configurable via setup.json
- Zero external dependencies
- Cross-platform

## Configuration

Edit `setup.json` to customize setup:

```json
{
    "name": "my-project",
    "type": "python",
    "dependencies": [],
    "commands": {
        "pre_install": [],
        "install": [],
        "post_install": [],
        "configure": []
    },
    "environment": {
        "variables": {},
        "files": []
    }
}
```

## Integration with Other Tools

- Works seamlessly with `prj` (project scaffolder)
- Works with `agt` (agent scaffolder)
- Complements `flow` (workflow orchestrator)

## License

MIT
