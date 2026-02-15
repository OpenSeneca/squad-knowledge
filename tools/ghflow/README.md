# ghflow — Convert flow Workflows to GitHub Agentic Workflows

Convert flow (YAML) workflows to GitHub Agentic Workflows (Markdown).

## Installation

```bash
# Link to PATH
ln -s $(pwd)/ghflow.sh ~/.local/bin/ghflow

# Or add to PATH manually
export PATH="$PATH:$(pwd)"
```

## Prerequisites

- [flow](../flow/) — Flow workflow orchestrator
- [gh aw](https://github.com/github/gh-aw) — GitHub Agentic Workflows CLI
- (Optional) [jq](https://stedolan.github.io/jq/) — For JSON parsing

## Usage

### List Available Flow Workflows

```bash
ghflow list
```

### Convert a Flow Workflow

```bash
ghflow convert my-workflow
```

Converts `~/.flow/my-workflow/workflow.yaml` to `.github/workflows/my-workflow.md`

### Convert All Workflows

```bash
ghflow convert-all
```

### Show Generated Workflow

```bash
ghflow show my-workflow
```

### Validate Flow Workflow

```bash
ghflow validate my-workflow
```

## Options

- `-o, --output <dir>` — Output directory (default: `.github/workflows`)
- `-t, --trigger <type>` — Trigger type: `manual`, `schedule`, `push`, `pr`
- `-f, --force` — Overwrite existing files

### Examples

```bash
# Custom output directory
ghflow convert deploy -o ./workflows

# Push trigger
ghflow convert ci -t push

# Force overwrite
ghflow convert deploy --force
```

## Workflow Format

### Input: flow YAML (`~/.flow/<name>/workflow.yaml`)

```yaml
name: "Deploy Application"
description: "Build and deploy application"

stages:
  - id: setup
    name: "Setup Project"
    description: "Initialize project structure"
    commands:
      - tool: prj
        action: create
        args: ["my-app", "--type", "typescript"]
```

### Output: GitHub Agentic Workflow (Markdown)

```markdown
# Deploy Application

Build and deploy application

## Trigger

This workflow is triggered on manual.

---

## Workflow Goals

### Stage 1: Setup Project

Initialize project structure

**Tool:** `prj`
**Action:** create
**Arguments:** my-app --type typescript
```

## Tool Mapping

| Flow Tool | GitHub Equivalent |
|-----------|------------------|
| `prj create` | Create new repository/files |
| `agt create` | Create agent repository structure |
| `tick add` | Create GitHub issue |
| `snip add` | Add to project wiki or documentation |
| `crw run` | Execute agent workflow in GitHub Actions |

## Compiling to GitHub Actions

After converting, compile the Markdown to a GitHub Actions YAML:

```bash
gh aw compile .github/workflows/my-workflow.md
```

This generates a standard GitHub Actions workflow file.

## Example Workflow

```bash
# 1. Create a flow workflow
flow init
flow create deploy-pipeline -d "Build and deploy application"

# 2. Convert to GitHub Agentic Workflow
ghflow convert deploy-pipeline

# 3. Review the generated workflow
ghflow show deploy-pipeline

# 4. Compile to GitHub Actions
gh aw compile .github/workflows/deploy-pipeline.md

# 5. Commit to repository
git add .github/workflows/
git commit -m "Add deploy-pipeline GitHub Agentic Workflow"
```

## Features

- Validates flow workflow structure
- Converts YAML to natural language Markdown
- Generates GitHub Actions YAML template
- Maps flow tools to GitHub operations
- Supports multiple trigger types
- Batch conversion of all workflows

## Integration with flow

ghflow works seamlessly with the [flow](../flow/) tool:

- Reads flow workflows from `~/.flow/`
- Preserves workflow structure
- Maintains stage ordering
- Maps commands to GitHub equivalents

## GitHub Agentic Workflows

GitHub Agentic Workflows let you write automation in Markdown instead of YAML.
The AI agent figures out how to execute the workflow.

Learn more: [GitHub Agentic Workflows Documentation](https://github.github.com/gh-aw/)

## License

MIT
