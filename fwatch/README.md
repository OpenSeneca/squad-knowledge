# watch — File Watcher and Runner

Watch files and directories for changes, then run commands automatically. Perfect for development workflows: tests, builds, linters, servers.

**Location:** `~/workspace/tools/watch/`

**Install:** Symlink to `~/.local/bin/watch`

```bash
ln -s ~/workspace/tools/watch/watch.py ~/.local/bin/watch
chmod +x ~/workspace/tools/watch/watch.py
```

## Features

- **File Watching** — Monitor files and directories for changes
- **Automatic Commands** — Run commands when files change
- **Pattern Filtering** — Watch specific file patterns (extensions, paths)
- **Exclude Patterns** — Exclude files/directories from watching
- **Debounce Control** — Control how quickly commands run after changes
- **Polling** — No external dependencies (uses polling)
- **Event Types** — Different commands for create/modify/delete
- **Recursive Watching** — Watch subdirectories
- **Oneshot Mode** — Run once and exit
- **Initial Run** — Run command on startup
- **Logging** — Log events to file
- **Config Files** — Save/load configurations

## Key Commands

### Basic Watching

- `watch -c <command>` — Watch current directory, run command on changes
- `watch -d <dir> -c <command>` — Watch specific directory
- `watch -p <patterns> -c <command>` — Watch specific patterns
- `watch -p <patterns> -c <command> --initial-run` — Run on startup

### Pattern Filtering

- `watch -p ".py" -c "pytest"` — Watch Python files
- `watch -p ".js,.ts,.jsx,.tsx" -c "npm test"` — Watch JS/TS files
- `watch -p "src/" -c "npm run build"` — Watch specific directory

### Exclusions

- `watch -x "node_modules" -c "npm test"` — Exclude directories
- `watch -x "node_modules,dist,.git" -c "pytest"` — Exclude multiple

### Event-Specific Commands

- `watch --on-create <cmd>` — Run on file creation
- `watch --on-modify <cmd>` — Run on file modification
- `watch --on-delete <cmd>` — Run on file deletion

### Configuration

- `watch --save-config <file>` — Save configuration to file
- `watch --load-config <file>` — Load configuration from file

### Options

- `--debounce <ms>` — Set debounce time (default: 300ms)
- `--poll <seconds>` — Set poll interval (default: 1.0s)
- `--no-recurse` — Don't watch subdirectories
- `--oneshot` — Run once and exit
- `--show-events` — Show all file events
- `--log-file <file>` — Log events to file

## Examples

### Auto-Run Tests

```bash
# Run tests when Python files change
watch -p ".py" -c "pytest"

# Run tests when JS/TS files change
watch -p ".js,.ts,.jsx,.tsx" -c "npm test"

# Run tests with initial run
watch -p ".py" -c "pytest" --initial-run
```

### Auto-Build

```bash
# Build when source files change
watch -c "npm run build" --exclude node_modules

# Build TypeScript
watch -p ".ts,.tsx" -c "npm run build" --exclude node_modules

# Build Python package
watch -p ".py" -c "python setup.py build"
```

### Auto-Format/Lint

```bash
# Auto-format Python files on save
watch -p ".py" -c "black ."

# Auto-lint JavaScript files
watch -p ".js" -c "eslint ."

# Auto-format and lint
watch -p ".py" -c "black . && flake8 ."
```

### Auto-Restart Servers

```bash
# Restart Node.js server on changes
watch -p ".js" -c "pm2 restart myapp"

# Restart Python server
watch -p ".py" -c "systemctl restart myserver"

# Kill and restart process
watch -p ".py" -c "pkill -f myapp; python myapp.py"
```

### Auto-Generate Documentation

```bash
# Generate docs when Markdown files change
watch -p ".md" -c "make docs"

# Generate API docs
watch -p ".py" -c "sphinx-build -b html docs docs/_build"
```

### Watch Multiple Directories

```bash
# Watch src and tests
watch -d src -d tests -p ".py" -c "pytest"

# Watch specific paths
watch -d ./src -d ./lib -c "npm run build"
```

### Exclude Files

```bash
# Exclude node_modules and dist
watch -x "node_modules,dist" -p ".js" -c "npm test"

# Exclude multiple patterns
watch -x "node_modules,dist,.git,coverage" -p ".py" -c "pytest"
```

### Event-Specific Commands

```bash
# Run different commands for different events
watch -p ".py" --on-modify "pytest" --on-delete "rm -rf .pytest_cache"

# Run on file creation only
watch -p ".md" --on-create "make docs"
```

### Oneshot Mode

```bash
# Run once and exit (useful for CI)
watch -p ".py" -c "pytest" --oneshot --initial-run

# Watch for changes, run once found, then exit
watch -p ".json" -c "echo 'Config changed'" --oneshot
```

### Show Events

```bash
# Show all file events
watch -p ".py" -c "pytest" --show-events

# Show events with logging
watch -p ".js" -c "npm test" --show-events --log-file watch.log
```

### Save/Load Configuration

```bash
# Save configuration
watch -p ".py" -c "pytest" --initial-run --save-config .watchrc

# Load configuration
watch --load-config .watchrc

# Example .watchrc file:
{
  "watch_dirs": ["src", "tests"],
  "watch_patterns": [".py"],
  "exclude_patterns": ["__pycache__"],
  "command": "pytest",
  "initial_run": true,
  "debounce_ms": 300,
  "poll_interval": 1.0,
  "recurse": true
}
```

### Custom Poll Interval

```bash
# Poll every 2 seconds (slower but less CPU)
watch -p ".py" -c "pytest" --poll 2.0

# Poll every 0.5 seconds (faster but more CPU)
watch -p ".js" -c "npm test" --poll 0.5
```

### Custom Debounce

```bash
# Wait 1 second before running command
watch -p ".py" -c "pytest" --debounce 1000

# Run immediately on change
watch -p ".js" -c "npm run build" --debounce 0
```

### Non-Recursive Watching

```bash
# Watch only top-level files
watch -p ".py" -c "pytest" --no-recurse

# Watch specific directory, not subdirectories
watch -d src -p ".py" -c "pytest" --no-recurse
```

## Use Cases

### Development Workflow

```bash
# Watch and test automatically
watch -p ".py" -c "pytest -x" --initial-run

# Watch and build automatically
watch -p ".ts" -c "npm run build" --exclude node_modules

# Watch and format automatically
watch -p ".py" -c "black . && flake8 ."
```

### Continuous Integration

```bash
# Run once in CI (watch for changes, run, exit)
watch -p ".py" -c "pytest" --oneshot --initial-run
```

### Documentation Generation

```bash
# Auto-regenerate docs
watch -p "docs/*.md" -c "make html"

# Auto-generate API docs
watch -p "src/**/*.py" -c "sphinx-build docs build"
```

### Server Auto-Restart

```bash
# Restart Python server on changes
watch -p "server.py" -c "pkill -f server.py; python server.py"

# Restart Node.js server with PM2
watch -p "*.js" -c "pm2 restart myapp"
```

### Lint and Format

```bash
# Auto-lint on save
watch -p ".js" -c "eslint . --fix"

# Auto-format Python files
watch -p ".py" -c "black ."

# Run linters
watch -p ".py,.js,.ts" -c "npm run lint"
```

### Deployment Automation

```bash
# Build and deploy on changes
watch -p "src/**" -c "npm run build && rsync -av dist/ user@server:/var/www/"

# Watch production files
watch -p "production/**" -c "./deploy.sh"
```

### Asset Optimization

```bash
# Optimize images on save
watch -p "*.png" -c "optipng *.png"

# Minify CSS
watch -p "src/*.css" -c "cssnano src/*.css dist/"
```

### Database Migration

```bash
# Run migrations on schema changes
watch -p "migrations/*.sql" -c "psql -f migrations/*.sql"

# Run Alembic migrations
watch -p "alembic/versions/*.py" -c "alembic upgrade head"
```

## Integration with Other Tools

### With notes (note taking)

```bash
# Note test failures
watch -p ".py" -c "pytest --tb=short 2>&1 | notes add -c debug"

# Note build errors
watch -c "npm run build 2>&1" --show-events | notes add -c debug
```

### With run (command runner)

```bash
# Store watch command
run add test-watch "watch -p '.py' -c 'pytest' --initial-run"

# Run stored watch command
run test-watch
```

### With focus (session tracker)

```bash
# Start session
focus start "Test-driven development"

# Watch and run tests
watch -p ".py" -c "pytest"

# End session when done
focus end
```

### With snip (snippet manager)

```bash
# Save watch command as snippet
snip add watch-py-tests "watch -p '.py' -c 'pytest' --initial-run"

# Use snippet later
watch $(snip get watch-py-tests)
```

### With git-helper (Git automation)

```bash
# Watch and commit automatically
watch -p ".py" --on-modify "git add . && git commit -m 'Auto-commit'"

# Watch and push
watch -p ".py" -c "git add . && git commit -m 'WIP' && git push"
```

## Best Practices

### Debouncing

**Use appropriate debounce times:**
```bash
# Fast tools (lint, format): low debounce
watch -p ".py" -c "black ." --debounce 100

# Slow tools (builds, tests): higher debounce
watch -p ".py" -c "pytest" --debounce 1000
```

### Poll Interval

**Balance speed and CPU usage:**
```bash
# Fast feedback (more CPU)
watch -p ".py" -c "pytest" --poll 0.5

# Lower CPU usage (slower feedback)
watch -p ".py" -c "pytest" --poll 2.0
```

### Exclusions

**Exclude unnecessary directories:**
```bash
# Node.js projects
watch -x "node_modules,dist,.next" -p ".js" -c "npm test"

# Python projects
watch -x "__pycache__,.pytest_cache,venv,.venv" -p ".py" -c "pytest"

# Multiple languages
watch -x "node_modules,dist,__pycache__,.git" -c "npm run build"
```

### Initial Run

**Run on startup for immediate feedback:**
```bash
# Run tests immediately
watch -p ".py" -c "pytest" --initial-run

# Build immediately
watch -c "npm run build" --initial-run
```

### Logging

**Log for debugging:**
```bash
# Log all events
watch -p ".py" -c "pytest" --show-events --log-file watch.log

# Log errors only
watch -p ".py" -c "pytest" --log-file watch.log
```

## Configuration Files

### Example .watchrc

```json
{
  "watch_dirs": ["src", "tests"],
  "watch_patterns": [".py"],
  "exclude_patterns": ["__pycache__", ".pytest_cache"],
  "command": "pytest -x",
  "debounce_ms": 500,
  "poll_interval": 1.0,
  "recurse": true,
  "initial_run": true,
  "show_events": false,
  "log_file": null
}
```

### Example for JavaScript Projects

```json
{
  "watch_dirs": ["src"],
  "watch_patterns": [".js", ".ts", ".jsx", ".tsx"],
  "exclude_patterns": ["node_modules", "dist", ".next"],
  "command": "npm test",
  "debounce_ms": 300,
  "poll_interval": 1.0,
  "recurse": true,
  "initial_run": true
}
```

### Example for Documentation

```json
{
  "watch_dirs": ["docs"],
  "watch_patterns": [".md", ".rst"],
  "command": "make html",
  "debounce_ms": 1000,
  "poll_interval": 2.0,
  "recurse": true,
  "initial_run": true
}
```

## Troubleshooting

### Command Not Running

**Check patterns:**
```bash
# Too restrictive
watch -p "test_*.py" -c "pytest"  # Won't match non-test files

# Broader pattern
watch -p ".py" -c "pytest"  # Matches all Python files
```

**Check exclusions:**
```bash
# Excluding too much
watch -x "src" -p ".py" -c "pytest"  # Excludes src/

# Check exclusions list
watch -x "node_modules" -p ".py" -c "pytest"  # Only exclude node_modules
```

### Too Many Commands Running

**Increase debounce:**
```bash
# Too fast
watch -p ".py" -c "pytest" --debounce 100  # Runs frequently

# Slower
watch -p ".py" -c "pytest" --debounce 1000  # Waits 1 second
```

**Increase poll interval:**
```bash
# Too fast (high CPU)
watch -p ".py" -c "pytest" --poll 0.5

# Slower (lower CPU)
watch -p ".py" -c "pytest" --poll 2.0
```

### Changes Not Detected

**Check patterns:**
```bash
# Pattern doesn't match
watch -p "*.py" -c "pytest"  # Won't match files in subdirs

# Use dot prefix for extensions
watch -p ".py" -c "pytest"  # Matches all .py files
```

**Check recursion:**
```bash
# Not watching subdirectories
watch -p ".py" -c "pytest" --no-recurse

# Watch all subdirectories
watch -p ".py" -c "pytest"  # Default: recursive
```

### High CPU Usage

**Increase poll interval:**
```bash
# Reduce CPU usage
watch -p ".py" -c "pytest" --poll 2.0  # Poll every 2 seconds
```

**Use patterns to reduce files:**
```bash
# Watch fewer files
watch -p "test_*.py" -c "pytest"  # Only test files
```

## Performance Tips

**For large projects:**
- Use specific patterns (not all files)
- Increase poll interval
- Exclude unnecessary directories
- Use higher debounce

**For fast feedback:**
- Use shorter poll interval
- Use lower debounce
- Watch only relevant files
- Exclude build artifacts

## Comparison to Alternatives

**vs `nodemon`:**
- `nodemon`: Node.js specific
- `watch`: Works with any language

**vs `watchexec`:**
- `watchexec`: More features, external dependency
- `watch`: Pure Python, zero dependencies

**vs `entr`:**
- `entr`: Very fast, Linux only
- `watch`: Cross-platform, polling

## Technical Details

**Polling vs Events:**
- Uses polling for compatibility (no external dependencies)
- Poll interval defaults to 1 second
- Debounce prevents rapid-fire commands
- Checks file mtime and size for changes

**File Detection:**
- Detects creates, modifies, deletes
- Uses os.stat() for file metadata
- Tracks state between polls
- Compares old vs new state

## Requirements

- Python 3.6+
- No external dependencies (pure Python)
- Polling-based (no inotify/fsevents)

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Watch. React. Automate.**

Automate your development workflow with intelligent file watching.
