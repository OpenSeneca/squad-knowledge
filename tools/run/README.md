# run — Command Runner and Launcher

Store, organize, and run frequently used shell commands with names, tags, and descriptions.

**Location:** `~/workspace/tools/run/`

**Install:** Symlink to `~/.local/bin/run`

```bash
ln -s ~/workspace/tools/run/run.py ~/.local/bin/run
chmod +x ~/.local/bin/run
```

## Features

- **Named Commands** — Store complex commands with memorable names
- **Groups** — Organize commands by project or context
- **Tags** — Categorize commands for easy filtering
- **History** — Track command execution history
- **Search** — Find commands by name, description, or command
- **Dry Run** — Preview commands before executing
- **Import/Export** — Backup and share command collections
- **Zero Dependencies** — Pure Python, no external packages required

## Key Commands

### Managing Commands

- `run add <name> <command>` — Add a new command
- `run remove <name>` — Remove a command
- `run show <name>` — Show command details
- `run list` — List all commands
- `run list -g <group>` — List commands in a group
- `run list -t <tag>` — List commands with tag

### Running Commands

- `run <name>` — Run a stored command
- `run run <name>` — Run with options
- `run run <name> --dry-run` — Show command without executing

### Searching and History

- `run search <query>` — Search commands
- `run groups` — List all command groups
- `run history` — Show recent command history
- `run history -n 20` — Show last 20 entries

### Import/Export

- `run export <file>` — Export commands to JSON
- `run import <file>` — Import commands (replace)
- `run import <file> --merge` — Import commands (merge)

## Examples

### Add Commands

```bash
# Simple command
run add deploy "npm run build && ./deploy.sh"

# With description and group
run add deploy-dev "npm run build && ./deploy.sh dev" -d "Deploy to dev env" -g deployment

# With tags
run add docker-prune "docker system prune -f" -d "Clean Docker" -t docker cleanup

# Complex multi-step command
run add full-deploy "npm run test && npm run build && ./deploy.sh prod" -d "Full deployment pipeline" -g deployment -t ci
```

### List Commands

```bash
# List all commands
run list

# List commands in deployment group
run list -g deployment

# List commands with docker tag
run list -t docker
```

### Run Commands

```bash
# Run a command
run deploy-dev

# Dry run (preview)
run run deploy-dev --dry-run

# Direct execution (no shell)
run run simple-command --no-shell
```

### Search Commands

```bash
# Search by name
run search deploy

# Search by description
run search "clean"

# Search by command content
run search docker
```

### Show Details

```bash
# Show command details
run show deploy-dev

# Output:
# 📝 Command: deploy-dev
#
#   Command: npm run build && ./deploy.sh dev
#   Description: Deploy to dev env
#   Group: deployment
#   Tags: None
#   Runs: 5
#   Created: 2026-02-16T04:30:00
```

### History

```bash
# Show recent history
run history

# Show last 20 entries
run history -n 20

# Output:
# 📜 Recent command history (last 5):
#
#   ✅ 2026-02-16 04:35 — deploy-dev
#      npm run build && ./deploy.sh dev
#
#   ❌ 2026-02-16 04:32 — deploy-prod
#      npm run build && ./deploy.sh prod
```

### Import/Export

```bash
# Export commands
run export commands-backup.json

# Import commands (replace)
run import commands-backup.json

# Import commands (merge)
run import commands-backup.json --merge
```

## Storage

Commands are stored in `~/.run/commands.json` as JSON:

```json
{
  "deploy-dev": {
    "command": "npm run build && ./deploy.sh dev",
    "description": "Deploy to dev env",
    "tags": [],
    "group": "deployment",
    "created": "2026-02-16T04:30:00",
    "runs": 5
  }
}
```

History is stored in `~/.run/history.jsonl` (one JSON line per execution).

## Use Cases

### DevOps Automation

```bash
# Add deployment commands
run add deploy-dev "./deploy.sh dev" -g deployment -t ci
run add deploy-staging "./deploy.sh staging" -g deployment -t ci
run add deploy-prod "./deploy.sh prod" -g deployment -t ci

# Run deployment
run deploy-dev
```

### Docker Management

```bash
# Add Docker commands
run add docker-clean "docker system prune -f" -t docker cleanup
run add docker-restart "docker-compose restart" -t docker
run add docker-logs "docker-compose logs -f" -t docker

# Clean up
run docker-clean
```

### Development Workflow

```bash
# Add development commands
run add test "pytest -xvs" -g dev
run add lint "eslint src/" -g dev
run add build "npm run build" -g dev

# Run full dev workflow
run test && run lint && run build
```

### System Administration

```bash
# Add admin commands
run add disk-usage "df -h" -g sysadmin
run add top-processes "ps aux | sort -nk4 | tail -5" -g sysadmin
run add service-status "systemctl status nginx" -g sysadmin

# Check system
run disk-usage
```

## Advanced Usage

### Group Management

```bash
# List all groups
run groups

# Filter by group
run list -g deployment

# Common groups: dev, deployment, sysadmin, docker, testing
```

### Tag Filtering

```bash
# Multiple tags filter
run list -t docker cleanup

# Tag combinations (AND logic)
run list -t docker testing
```

### Command Composition

```bash
# Combine commands with shell operators
run add full-test "npm test && npm run coverage && npm run lint"

# Pipeline commands
run add log-check "docker logs app | grep -i error"

# Background processes
run add start-server "npm run start &"
```

## Tips

1. **Naming Conventions** — Use kebab-case: `deploy-dev`, `docker-clean`
2. **Descriptive Names** — Include action: `start-server`, `stop-server`
3. **Groups** — Organize by context: `dev`, `deployment`, `sysadmin`
4. **Tags** — Use multiple tags: `docker cleanup`, `testing integration`
5. **Dry Run** — Always test with `--dry-run` first for risky commands
6. **Backup** — Regularly export commands: `run export backup-$(date +%Y%m%d).json`

## Troubleshooting

### Command Not Found

```bash
# List all commands
run list

# Search for command
run search <name>
```

### Command Execution Failed

```bash
# Check history
run history

# Try dry run first
run run <name> --dry-run

# Show command details
run show <name>
```

### Import Issues

```bash
# Validate JSON file
cat commands-backup.json | jq .

# Use merge to avoid conflicts
run import commands-backup.json --merge
```

## Data Locations

- **Commands:** `~/.run/commands.json`
- **History:** `~/.run/history.jsonl`
- **Config Directory:** `~/.run/`

## Integration

### With Other Tools

```bash
# Use with tick for task tracking
run add deploy-tick "tick add 'Deploy to prod' -p high -t deployment && run deploy-prod"

# Use with snip for code snippets
run add run-tests "pytest && snip add test-results '$(pytest --tb=no)'"

# Use with squad-setup for SSH commands
run add ssh-marcus "ssh marcus-squad 'openclaw status'" -t ssh squad
```

### Shell Integration

Add to `~/.bashrc` for tab completion:

```bash
_run_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local commands=$(run list | grep '• ' | awk '{print $2}' | cut -d'[' -f1)
    COMPREPLY=($(compgen -W "$commands" -- "$cur"))
}
complete -F _run_completion run
```

## Best Practices

1. **Test Locally** — Dry run commands before running in production
2. **Document Well** — Use descriptions for complex commands
3. **Group Logically** — Organize by project or environment
4. **Tag Generously** — Makes filtering easier
5. **Regular Backup** — Export commands periodically
6. **Version Control** — Consider committing exported JSON to repo
7. **Review History** — Check history to find frequently used commands
8. **Keep Simple** — If a command is too complex, consider a script

## Comparison to Alternatives

### vs Shell Aliases
- **run:** Persistent, organized, searchable, grouped
- **aliases:** Limited to current shell, hard to organize

### vs Shell Scripts
- **run:** Quick and simple, built-in history
- **scripts:** More powerful, but requires file management

### vs Make
- **run:** Command-focused, no Makefile syntax
- **make:** File-focused, dependency management

### vs npm scripts
- **run:** Language-agnostic, system-wide
- **npm:** Node.js specific, project-scoped

## Security

- Commands are stored in plain text JSON
- No password or sensitive data in commands
- Use environment variables for secrets:
  ```bash
  run add deploy "export $TOKEN && ./deploy.sh"
  ```

## Performance

- Instant command lookup (JSON file)
- No startup overhead (pure Python)
- Minimal disk I/O (single file read)

## License

MIT License — Part of the OpenClaw Workspace Toolset

---

**Version:** 1.0.0
**Last Updated:** February 16, 2026
**Dependencies:** None (pure Python)
