# snip — Simple Snippet Manager

Save, search, and retrieve code snippets with tags. Never lose that clever one-liner again.

## Installation

```bash
# Make it executable
chmod +x ~/workspace/tools/snip/snip.py

# Add to PATH (add to your ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$HOME/workspace/tools/snip"

# Or create a symlink
ln -s ~/workspace/tools/snip/snip.py ~/.local/bin/snip
```

## Usage

### Add a snippet

```bash
# Add from command line
snip add curl-json 'curl -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com' \
  -t http api -d "Curl with JSON body"

# Short form
snip add jq-filter 'jq ".[] | select(.status == \"active\")"' -t json
```

### Get a snippet

```bash
snip get curl-json
```

Output:
```
📌 curl-json
   Tags: http, api

curl -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com
```

### Search snippets

```bash
# Search by keyword (searches name, description, and content)
snip search curl

# Filter by tag
snip search --tag json

# Search within a tag
snip search api --tag http
```

### List all snippets

```bash
# List all
snip list

# Filter by tag
snip list --tag json
```

### Update a snippet

```bash
snip update curl-json -d 'Updated description'
snip update jq-filter -t json parsing -d "Filter JSON with jq"
```

### Edit in your editor

```bash
# Opens $EDITOR (defaults to vim)
snip edit curl-json
```

### Delete a snippet

```bash
snip delete old-snippet
```

### Export/Import

```bash
# Backup your snippets
snip export ~/backups/snippets.json

# Import from file
snip import ~/backups/snippets.json
```

## Data Location

Snippets are stored in `~/.snip/snippets.json` (JSON format, easy to edit manually if needed).

## Tips

1. **Tag thoughtfully** — Use consistent tags like `git`, `docker`, `python`, `regex`
2. **Descriptive names** — `curl-json` beats `snippet1`
3. **One-liners first** — Start with small useful commands
4. **Regular backups** — Export periodically

## Examples

```bash
# Git helpers
snip add git-clean-branches 'git branch --merged | grep -v main | xargs git branch -d' \
  -t git -d "Delete merged branches except main"

# Docker
snip add docker-cleanup 'docker system prune -a -f --volumes' -t docker

# Regex
snip add regex-email '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' \
  -t regex -d "Email address pattern"

# Python one-liner
snip add py-http-server 'python3 -m http.server 8000' -t python http
```

## Why This Exists

Because grep-ing through git history or digging through old projects to find that one perfect command is annoying. Snippets stay with you, not with a project.
