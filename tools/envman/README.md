# env — Environment Variable Manager

Manage .env files, switch between environments, and securely handle secrets.

**Location:** `~/workspace/tools/env/`

**Install:** Symlink to `~/.local/bin/env`

```bash
ln -s ~/workspace/tools/env/env.py ~/.local/bin/env
chmod +x ~/workspace/tools/env/env.py
```

## Features

- **Environment Management** — Add, remove, and switch between environments
- **Variable Operations** — Set, get, unset environment variables
- **Secret Masking** — Automatically masks secret values (passwords, keys, secrets)
- **Import/Export** — Import from files, export to shell format
- **Project Detection** — Automatically finds project root and .env files
- **Safe Switching** — Backs up current .env before switching

## Key Commands

### Environment Management

- `env list` — List all environments
- `env add <name>` — Add environment (uses ./.env by default)
- `env add <name> <path>` — Add environment with specific path
- `env remove <name>` — Remove environment
- `env remove <name> --keep-file` — Remove but keep .env file
- `env switch <name>` — Switch active environment

### Variable Operations

- `env set <key> <value>` — Set environment variable
- `env get <key>` — Get environment variable
- `env unset <key>` — Unset environment variable
- `env show` — Show all variables (with secret masking)
- `env show -e <name>` — Show variables for specific environment
- `env show --no-mask` — Show all values (including secrets)

### Import/Export

- `env export <name> <output>` — Export to shell format
- `env import <input>` — Import from file
- `env import <input> -e <name>` — Import to specific environment

## Examples

### Environment Management

```bash
# Add development environment
env add dev

# Add environment with custom path
env add prod ~/projects/myapp/.env.production

# Add with description
env add staging ./config/.env.staging -d "Staging environment"

# List all environments
env list

# Switch to development environment
env switch dev

# Remove environment
env remove old-env

# Remove but keep file
env remove old-env --keep-file
```

### Variable Operations

```bash
# Set variable
env set API_KEY "my-secret-key"

# Set variable in specific environment
env set DATABASE_URL "postgresql://localhost/mydb" -e prod

# Get variable
env get API_KEY

# Get variable from specific environment
env get DATABASE_URL -e prod

# Unset variable
env unset DEBUG

# Unset variable in specific environment
env unset TEST_MODE -e dev

# Show all variables
env show

# Show variables for specific environment
env show -e prod

# Show with no masking (use with caution!)
env show --no-mask
```

### Import/Export

```bash
# Export to shell script
env export dev shell-vars.sh

# Source the exported file
source shell-vars.sh

# Import from file
env import config/.env.example

# Import to specific environment
env import backup/.env.backup -e prod

# Import from production template
env import .env.template -e dev
```

## Environment Switching

**How it works:**

1. **Backup current .env** (if exists)
   - Creates .env.backup before switching

2. **Copy new environment** to project root
   - Copies source .env to ./.env

3. **Set as active** (for next switch)

```bash
# Setup environments
env add dev ./.env.development
env add staging ./.env.staging
env add prod ./.env.production

# Switch to development
env switch dev
# Copied: ./.env.development → ./.env

# Work with dev config...
# .env file now has development variables

# Switch to production
env switch prod
# Backup: ./.env → ./.env.backup
# Copied: ./.env.production → ./.env
```

## Project Detection

**Automatic detection:**
The tool automatically finds the project root by looking for:
- `.env` file
- `package.json` (Node.js)
- `.git` directory (Git repo)

**Fallback:** Uses current directory if no markers found.

```bash
# From anywhere in project
cd ~/projects/myapp/src/components
env set API_KEY "test"

# Automatically finds project root (~/projects/myapp/)
# Sets variable in ~/projects/myapp/.env
```

## Secret Masking

**Automatic masking:**
Variables with these keywords in the name are automatically masked:
- `secret`
- `key`
- `password`

```bash
# Set secret variable
env set DATABASE_PASSWORD "super-secret"

# Get shows masked value
env get DATABASE_PASSWORD
# DATABASE_PASSWORD=***

# List with values shows masked
env list -v
# DATABASE_PASSWORD=***

# Show all values (be careful!)
env show --no-mask
# DATABASE_PASSWORD=super-secret
```

## Use Cases

### Multi-Environment Projects

```bash
# Setup
env add dev ./.env.development
env add staging ./.env.staging
env add prod ./.env.production

# Development
env switch dev
npm run dev

# Staging
env switch staging
npm run build && npm run deploy:staging

# Production
env switch prod
npm run build && npm run deploy:prod
```

### Secret Management

```bash
# Add secret (automatically masked in displays)
env set STRIPE_SECRET_KEY "sk_live_..."
env set DATABASE_PASSWORD "..."
env set JWT_SECRET "..."

# Safe to list
env show
# All secrets shown as ***

# Export for deployment
env export prod deploy-vars.sh
# All values exported (unmasked) for actual use
```

### Team Onboarding

```bash
# Create template environment
cat > .env.example << 'EOF'
API_KEY=
DATABASE_URL=
DEBUG=false
EOF

# New team member imports template
env import .env.example -e dev

# Then sets their own values
env set API_KEY "their-key"
env set DATABASE_URL "postgresql://..."
```

### Local Development

```bash
# Add local environment
env add local

# Set local variables
env set DEBUG=true
env set LOG_LEVEL=verbose
env set DATABASE_URL="postgresql://localhost/mydb"

# Work locally
env switch local
npm run dev

# Done working, switch back
env switch dev
```

### Configuration Management

```bash
# Save configuration as environment
env set APP_NAME "My App"
env set APP_VERSION="1.0.0"
env set APP_ENV="production"

# Use in application
# process.env.APP_NAME
# process.env.APP_VERSION
# process.env.APP_ENV
```

## Integration with Other Tools

**With run (command runner):**
```bash
# Run command with specific environment
run add dev-build "env switch dev && npm run build"
run add prod-build "env switch prod && npm run build"

# Execute
run dev-build
```

**With focus (session tracker):**
```bash
# Start session with environment
focus start "Configure dev environment"
env switch dev
env set API_KEY "test-key"
focus end
```

**With git (version control):**
```bash
# Add .env to .gitignore
echo ".env" >> .gitignore
echo ".env.backup" >> .gitignore

# Commit .env.example instead
env export dev .env.example
git add .env.example
git commit "Add environment template"
```

**With squad-setup (for deployment):**
```bash
# Setup deployment environment
env add production ~/projects/squad-dashboard/.env.prod

# Set production variables
env set FORGE_HOST="100.93.69.117" -e production
env set FORGE_PORT="8080" -e production
env set SSH_USER="forge" -e production

# Export for deployment
env export production deploy-vars.sh
```

## Best Practices

### Security

**Never commit secrets:**
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.backup" >> .gitignore
echo "*.key" >> .gitignore
```

**Use .env.example:**
```bash
# Create template
cp .env .env.example
# Replace secrets with placeholders
# API_KEY=your-api-key-here
```

**Secure storage:**
```bash
# Set proper permissions
chmod 600 .env

# Only owner can read/write
```

### Environment Organization

**Naming conventions:**
- `dev` or `development` — Local development
- `staging` — Pre-production testing
- `prod` or `production` — Production
- `test` — Testing environment
- `local` — Local-only settings

**File organization:**
```
project/
├── .env                    # Active (gitignored)
├── .env.development        # Dev config
├── .env.staging            # Staging config
├── .env.production         # Production config
├── .env.example           # Template (committed)
└── .gitignore            # Ignores .env files
```

### Variable Naming

**Use prefixes:**
```bash
# App-specific
env set APP_NAME "My App"
env set APP_VERSION "1.0.0"

# Database
env set DB_HOST="localhost"
env set DB_PORT="5432"

# API
env set API_KEY="..."
env set API_URL="https://api.example.com"
```

**Use uppercase:**
```bash
# Good
env set DATABASE_URL="..."
env set API_KEY="..."

# Avoid (case-sensitive issues)
env set database_url="..."
env set api_key="..."
```

## Troubleshooting

### "Environment not found"

Environment doesn't exist in configuration.

```bash
# List available environments
env list

# Add missing environment
env add dev
```

### ".env file not found"

Target .env file doesn't exist.

```bash
# Create file first
touch .env

# Or add with automatic creation
env add dev
```

### "Cannot remove active environment"

Trying to remove currently active environment.

```bash
# Switch to another environment first
env switch dev

# Then remove
env remove old-env
```

### Variable not persisting

Setting variable in wrong environment.

```bash
# Check current directory
pwd

# List current variables
env show

# Set in current directory's .env
env set API_KEY "test"

# Or specify environment
env set API_KEY "test" -e prod
```

### Switching overwrites .env

This is expected behavior. Backups are created.

```bash
# Before switching
ls -la .env*

# After switching
# .env (new environment)
# .env.backup (previous environment)

# Restore if needed
cp .env.backup .env
```

## Data Storage

**Configuration:** `~/.env-manager/`
```
~/.env-manager/
├── environments.json     # Environment configurations
└── current            # Active environment name
```

**Environment file:** `~/.env-manager/environments.json`
```json
{
  "dev": {
    "path": "/home/user/projects/myapp/.env.development",
    "description": "Development environment",
    "created": "2026-02-16T06:30:00"
  },
  "prod": {
    "path": "/home/user/projects/myapp/.env.production",
    "description": "Production environment",
    "created": "2026-02-16T06:30:00"
  }
}
```

**.env file format:**
```bash
API_KEY=my-secret-key
DATABASE_URL=postgresql://localhost/mydb
DEBUG=true
LOG_LEVEL=verbose
```

## Shell Integration

**Auto-load .env:**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
# Auto-load .env if exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi
```

**Load on cd:**
```bash
cd() {
    builtin cd "$@"
    if [ -f .env ]; then
        export $(cat .env | xargs)
    fi
}
```

**Environment-specific aliases:**
```bash
alias dev='env switch dev && npm run dev'
alias staging='env switch staging && npm run build'
alias prod='env switch prod && npm run build && npm run deploy'
```

## Comparison to Alternatives

**vs Manual .env management:**
```bash
# Manual
cp .env.development .env
# Edit...
cp .env.production .env

# env
env switch dev
env switch prod
```

**vs dotenv (Node.js):**
- `env`: Works with any language
- `env`: Shell-native, no dependencies
- `dotenv`: Node.js specific, requires npm install

**vs direnv:**
- `env`: Simple, explicit switching
- `direnv`: Auto-load on cd (more complex)
- `env`: Easier for multiple environments

## Future Enhancements

- **Environment validation** — Check required variables are set
- **Variable encryption** — Encrypt secrets in .env files
- **Variable inheritance** — Common variables shared across environments
- **Environment diffs** — Show differences between environments
- **Variable history** — Track changes to variables
- **Team sharing** — Sync environments across team members
- **Cloud sync** — Store environments in secure cloud storage

## Requirements

- Python 3.6+
- No external dependencies
- Storage: `~/.env-manager/` (auto-created)

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Simple. Secure. Organized.**

Manage environment variables across development, staging, and production environments.
