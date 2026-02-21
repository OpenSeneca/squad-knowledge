# Obsidian Skills Manager

A CLI tool to help squad agents manage, validate, and test Obsidian skills. Ensures skills are properly structured, have required metadata, and are ready for use in the squad.

## Why This Matters

Justin's vault is the squad's knowledge base. Obsidian skills let agents interact with that vault (Markdown, Bases, JSON Canvas, CLI). This tool ensures:

- Skills have proper metadata (name, description, location)
- Required fields are present
- Documentation is complete
- Examples are provided
- Skills are ready for deployment

## Installation

```bash
cd ~/.openclaw/workspace/tools/obsidian-skills
chmod +x obsidian-skills
ln -sf $(pwd)/obsidian-skills ~/.local/bin/obsidian-skills
```

## Usage

### Validate a Single Skill

Check if a skill has all required fields:

```bash
obsidian-skills validate ~/.openclaw/skills/github/SKILL.md
```

Output:
```
🔷 Obsidian Skills Manager
   Manage and validate Obsidian agent skills

🔍 Validation Results:
  📄 File: /home/exedev/.openclaw/skills/github/SKILL.md
  ✓ name: github
  ✓ description: GitHub operations via gh CLI
  ✓ location: /usr/lib/node_modules/openclaw/skills/github/SKILL.md
  📊 Size: 3.24 KB
  💻 Code blocks: 12

✅ Valid
```

### Check Skill Structure

Detailed check of a skill including directory structure:

```bash
obsidian-skills check ~/.openclaw/skills/github/SKILL.md
```

This shows:
- Validation results
- Directory structure (scripts, files)
- Usage section check
- Examples check

### List All Skills

Scan a directory for all skills:

```bash
obsidian-skills list ~/.openclaw/skills
```

Output:
```
🔷 Obsidian Skills Manager
   Manage and validate Obsidian agent skills

📚 Found 6 skill(s):

1. github
   GitHub operations via gh CLI
   📂 /home/exedev/.openclaw/skills/github/SKILL.md

2. tmux
   Remote-control tmux sessions for interactive CLIs
   📂 /home/exedev/.openclaw/skills/tmux/SKILL.md
```

### Test a Skill

Run tests and checks on a skill:

```bash
obsidian-skills test ~/.openclaw/skills/github/SKILL.md
```

This:
- Validates the skill
- Checks for test scripts
- Looks for example usage
- Reports overall status

## Required Fields

Every Obsidian skill must have:

- `name`: Skill identifier (e.g., "github")
- `description`: What the skill does
- `location`: Path to SKILL.md file

Recommended fields:

- `version`: Skill version
- `author`: Who created it
- `metadata`: Additional context

## Skill Structure

A well-structured skill:

```
~/.openclaw/skills/github/
├── SKILL.md              # Main skill file (required)
├── scripts/              # Helper scripts (optional)
│   ├── setup.sh
│   └── test.sh
└── examples/             # Example outputs (optional)
    └── workflow.md
```

## For the Squad

**Marcus**: Use this to validate skills before documenting AI workflows
**Galen**: Check that research skills are properly structured
**Archimedes**: Use this when building new squad tools that need Obsidian integration

## Common Issues

### Missing Required Fields

```
❌ Missing required field: location
```

Fix: Add frontmatter or ensure header has location info.

### No Usage Section

```
⚠️  No usage section found
```

Fix: Add `## Usage` section to SKILL.md with examples.

### TODO Comments Found

```
⚠️  Contains 3 TODO/FIXME comment(s)
```

Fix: Complete or remove TODO comments before deployment.

## Integration with Squad

Use this in squad workflows:

```bash
# Before deploying a new skill
obsidian-skills validate new-skill/SKILL.md

# Audit all skills monthly
obsidian-skills list ~/.openclaw/skills | while read line; do
  obsidian-skills check "$(echo $line | awk '{print $NF}')"
done
```

## License

MIT
