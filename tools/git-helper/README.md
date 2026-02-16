# git-helper — Git Workflow Automation

Simplify Git operations with smart branch management, commit patterns, and release automation.

**Location:** `~/workspace/tools/git-helper/`

**Install:** Symlink to `~/.local/bin/git-helper`

```bash
ln -s ~/workspace/tools/git-helper/git-helper.py ~/.local/bin/git-helper
chmod +x ~/.local/bin/git-helper
```

## Features

- **Smart Branching** — Create branches with patterns (feature/, bugfix/, hotfix/)
- **Conventional Commits** — Enforce conventional commit format
- **Auto Push** — Optional automatic push after commit
- **Quick Status** — Concise repository status overview
- **Merge Operations** — Simplified branch merging
- **Configuration** — Customizable settings per repository

## Key Commands

### Status

- `git-helper status` — Show repository status
- `git-helper config` — Show configuration

### Branch Operations

- `git-helper branch list` — List all branches
- `git-helper branch new <name>` — Create new branch
- `git-helper branch new <name> -p <pattern>` — Create with pattern
- `git-helper branch switch <name>` — Switch to branch
- `git-helper branch delete <name>` — Delete branch

### Commit Operations

- `git-helper commit "message"` — Commit changes
- `git-helper commit --amend` — Amend last commit
- `git-helper commit --fixup` — Create fixup commit

### Remote Operations

- `git-helper push` — Push to remote (with upstream)
- `git-helper push -r origin --no-upstream` — Push without upstream
- `git-helper pull` — Pull from remote

### Merge Operations

- `git-helper merge <source>` — Merge branch
- `git-helper merge <source> -s <strategy>` — Merge with strategy

## Examples

### Repository Status

```bash
git-helper status
```

**Output:**
```
📁 Repository: squad-dashboard
🌿 Current branch: feature/add-realtime

📝 3 change(s):
  M src/App.tsx
  A components/Realtime.tsx
  ?? styles/realtime.css

📡 Remotes:
  • origin: git@github.com:exedev/squad-dashboard.git

⚙️  Configuration:
  • Default branch: main
  • Branch prefix: feature/
```

### Branch Management

```bash
# List all branches
git-helper branch list

# Create new feature branch
git-helper branch new add-dashboard-widgets

# Create bugfix branch with pattern
git-helper branch new fix-auth-bug -p bugfix

# Create hotfix from release branch
git-helper branch new urgent-fix -b release/v1.2.0 -p hotfix

# Switch branch
git-helper branch switch main

# Delete branch
git-helper branch delete add-dashboard-widgets
```

### Smart Branching

**Branch patterns:**
- `feature/` — New features (default)
- `bugfix/` — Bug fixes
- `hotfix/` — Urgent production fixes
- `release/` — Release branches
- `experiment/` — Experimental features

```bash
# Feature branch (default)
git-helper branch new user-authentication
# Creates: feature/user-authentication

# Bugfix branch
git-helper branch new login-error -p bugfix
# Creates: bugfix/login-error

# Hotfix branch
git-helper branch new critical-security -p hotfix
# Creates: hotfix/critical-security

# Release branch
git-helper branch new v1.2.0 -p release
# Creates: release/v1.2.0
```

### Conventional Commits

```bash
# Feature commit
git-helper commit "feat: Add user authentication"

# Bug fix commit
git-helper commit "fix: Resolve login timeout issue"

# Documentation commit
git-helper commit "docs: Update API documentation"

# Refactor commit
git-helper commit "refactor: Simplify data flow"

# Commit with scope
git-helper commit "feat(auth): Add OAuth support"
```

**Conventional commit types:**
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation changes
- `style` — Code style changes (formatting)
- `refactor` — Code refactoring
- `test` — Test additions or changes
- `chore` — Maintenance tasks
- `ci` — CI/CD changes
- `build` — Build system changes
- `perf` — Performance improvements
- `revert` — Revert previous commit

### Commit Operations

```bash
# Normal commit (stages all changes)
git-helper commit "feat: Add new feature"

# Amend last commit
git-helper commit --amend "feat: Add new feature (update description)"

# Create fixup commit
git-helper commit --fixup
```

### Push and Pull

```bash
# Push with upstream (first time)
git-helper push

# Push to specific remote
git-helper push -r upstream

# Push without setting upstream
git-helper push --no-upstream

# Pull from remote
git-helper pull

# Pull from specific remote
git-helper pull -r upstream
```

### Merge Operations

```bash
# Merge feature branch
git-helper merge feature/new-feature

# Merge with strategy
git-helper merge feature/new-feature -s ours

# Common strategies:
#   - ours: Keep our changes
#   - theirs: Use their changes
#   - recursive: Standard merge (default)
```

### Configuration

```bash
# Show all config
git-helper config

# Show specific config
git-helper config auto_push

# Set config value
git-helper config auto_push true
git-helper config branch_prefix feature/
git-helper config default_branch main

# Disable commit pattern checking
git-helper config commit_pattern none
```

**Configuration options:**
- `default_branch` — Default branch name (default: `main`)
- `branch_prefix` — Default branch prefix (default: `feature/`)
- `commit_pattern` — Commit format check (default: `conventional`)
- `auto_push` — Auto push after commit (default: `false`)
- `auto_pr` — Auto create PR (not yet implemented)

## Use Cases

### Feature Development Workflow

```bash
# Start new feature
git-helper branch new add-user-dashboard

# Work on feature...
# Edit files...

# Commit changes
git-helper commit "feat: Add user dashboard component"

# Push to remote
git-helper push

# Create PR manually or wait for auto_pr
```

### Bug Fix Workflow

```bash
# Create bugfix branch
git-helper branch new fix-login-error -p bugfix

# Fix bug...
# Edit files...

# Commit fix
git-helper commit "fix: Resolve login timeout issue"

# Push and create PR
git-helper push
```

### Hotfix Workflow

```bash
# Create hotfix from release
git-helper branch switch release/v1.2.0
git-helper branch new critical-security -p hotfix

# Fix critical issue...
# Commit fix...

# Merge back to release and main
git-helper branch switch main
git-helper merge hotfix/critical-security
```

### Release Workflow

```bash
# Create release branch
git-helper branch new v1.2.0 -p release

# Prepare release...
# Update version, changelog...

# Commit release
git-helper commit "chore: Release v1.2.0"

# Push and create release
git-helper push
```

## Integration with Other Tools

**With focus (session tracker):**
```bash
# Start focused work
focus start "Implement user authentication"

# Work...

# Commit when done
git-helper commit "feat: Add user authentication"

# End session
focus end
```

**With tick (task tracker):**
```bash
# Get tasks
tick list -p high

# Start working on task
git-helper branch new $(tick list | grep high | head -1 | awk '{print $2}')

# Commit with task reference
git-helper commit "feat(task-123): Implement feature"

# Mark task done
tick done 123
```

**With snip (snippet manager):**
```bash
# Commit snippets from project
snip search "squad-dashboard"

# Save useful commands as commit messages
snip add "commit-feature" "feat: Add $FEATURE_NAME"
```

## Best Practices

### Branch Naming
- Use descriptive names: `feature/user-authentication`, `bugfix/login-error`
- Use kebab-case: `feature/user-dashboard` not `feature/UserDashboard`
- Include scope: `feat(auth): Add OAuth support`
- Use patterns: `feature/`, `bugfix/`, `hotfix/`

### Commit Messages
- Follow conventional commits format
- Keep messages short and descriptive
- Use present tense: "Add" not "Added"
- Limit to 50 characters in first line
- Add body if needed (blank line, then description)

### Workflow
- Always branch from `main` or `develop`
- Keep branches short-lived
- Use PRs for code review
- Squash commits before merging
- Delete merged branches

### Release Management
- Use `release/vX.Y.Z` branches
- Create hotfixes from release branches
- Tag releases: `git tag v1.2.0`
- Update CHANGELOG.md

## Troubleshooting

### "Not a git repository"

You're not in a git repository.

```bash
# Initialize repo
git init

# Or clone existing
git clone <url>
```

### "Branch already exists"

Branch with that name already exists.

```bash
# List branches
git-helper branch list

# Use different name
git-helper branch new feature-name-2

# Or switch to existing
git-helper branch switch feature-name
```

### "Message doesn't follow conventional commits format"

Your commit message doesn't match conventional commits format.

**Fix:** Use format: `type(scope): description`

```bash
# Wrong
git-helper commit "Add new feature"

# Right
git-helper commit "feat: Add new feature"

# With scope
git-helper commit "feat(auth): Add OAuth support"
```

### "Cannot delete current branch"

You can't delete the branch you're on.

```bash
# Switch to another branch first
git-helper branch switch main

# Then delete
git-helper branch delete feature-name
```

### "Failed to push"

Push rejected or no remote configured.

```bash
# Check remotes
git-helper status

# Add remote if needed
git remote add origin <url>

# Force push (use with caution)
git push --force-with-lease
```

## Advanced Usage

### Branch Patterns

Edit `~/.git-helper/branch-patterns.json`:

```json
{
  "feature": "feature/",
  "bugfix": "bugfix/",
  "hotfix": "hotfix/",
  "release": "release/",
  "experiment": "experiment/"
}
```

Add custom patterns:

```json
{
  "feature": "feature/",
  "story": "story/",
  "epic": "epic/"
}
```

### Per-Repository Config

Override config for specific repo:

```bash
cd /path/to/repo
git-helper config branch_prefix story/
git-helper config commit_pattern none
```

### Conventional Commits

Why use conventional commits?

- **Automated Changelog** — Tools can generate CHANGELOG.md
- **Semantic Versioning** — Auto-determine version bumps
- **Commit Linting** — Enforce consistent messages
- **Searchable History** — Easy to find specific commits

### Git Hooks

Add git hooks for automation:

```bash
# Pre-commit hook for conventional commits
#!/bin/bash
MESSAGE=$(git log -1 --pretty=%B)
if ! echo "$MESSAGE" | grep -qE "^(feat|fix|docs|style|refactor|test|chore|ci|build|perf|revert)"; then
    echo "❌ Commit message doesn't follow conventional commits"
    exit 1
fi
```

## Data Storage

Config files stored in `~/.git-helper/`:

```
~/.git-helper/
├── config.json              # Configuration
└── branch-patterns.json     # Branch patterns
```

## Comparison to Git

**Simpler commands:**
```bash
# Git
git checkout -b feature/add-feature
git add -A
git commit -m "feat: Add feature"
git push -u origin feature/add-feature

# git-helper
git-helper branch new add-feature
git-helper commit "feat: Add feature"
git-helper push
```

**Less typing:**
```bash
# Git (18 chars)
git status --short

# git-helper (13 chars)
git-helper status
```

**Better defaults:**
- Auto-sets upstream on push
- Stages all changes before commit
- Branch patterns prevent naming inconsistencies
- Conventional commits enforce standards

## Future Enhancements

- **PR Creation** — Auto-create pull requests
- **Release Automation** — Tag and publish releases
- **Changelog Generation** — Generate CHANGELOG from commits
- **Commit Linting** — Strict commit message validation
- **Interactive Mode** — Interactive commit message builder
- **Git Flow Support** — Full git-flow integration

## Requirements

- Python 3.6+
- Git 2.20+
- No external dependencies

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Simple. Smart. Productive.**

Git operations made easy with patterns, conventions, and automation.
