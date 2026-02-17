# claude-analyzer — Claude Code Session Analyzer

Analyze Claude Code session logs and identify inefficiencies. Get actionable insights into your coding sessions.

**Location:** `~/workspace/tools/claude-code-analyzer/`

**Install:** Symlink to `~/.local/bin/claude-analyzer`

```bash
ln -s ~/workspace/tools/claude-code-analyzer/claude-analyzer.py ~/.local/bin/claude-analyzer
chmod +x ~/workspace/tools/claude-code-analyzer/claude-analyzer.py
```

## Features

- **Session Summary** — Turn count, tool usage, token efficiency
- **File Access Analysis** — Most frequently accessed files
- **Anti-Pattern Detection** — Duplicate reads, sensitive files
- **Context Usage Patterns** — Compaction events
- **Tool Usage Statistics** — Most used tools
- **Insights** — Actionable recommendations

## Key Commands

- `claude-analyzer` — Analyze latest session
- `claude-analyzer <session-file>` — Analyze specific session
- `claude-analyzer --list` — List available sessions
- `claude-analyzer --detailed` — Show detailed analysis
- `claude-analyzer --session-dir <path>` — Override session directory

## Examples

### Analyze Latest Session

```bash
claude-analyzer

# Output:
# ======================================================================
# 📊 Claude Code Session Analysis
# ======================================================================
#
# 📋 Session Summary:
#   Turns: 45
#   Tool calls: 128
#   Unique files: 23
#   Context compactions: 2
#   Total tokens: 156,780
#   Avg tokens/turn: 3,484
#
# 💡 Insights & Anti-Patterns:
#   ⚠️  File read 5 times: src/utils/api.py
#   ⚠️  File read 3 times: src/components/Header.tsx
#   📦 Context compacted 2 times — consider shorter sessions
#   🔧 'read' used 45 times — consider batching operations
```

### Analyze Specific Session

```bash
claude-analyzer session-2026-02-16.jsonl
```

### List Available Sessions

```bash
claude-analyzer --list

# Output:
# 📁 Available Sessions:
#
#   1. session-2026-02-16-14:30.jsonl (2026-02-16 14:30)
#   2. session-2026-02-16-12:15.jsonl (2026-02-16 12:15)
#   3. session-2026-02-15-16:45.jsonl (2026-02-15 16:45)
```

### Detailed Analysis

```bash
claude-analyzer --detailed

# Output:
# ... (includes file access patterns and tool usage)
#
# 📁 File Access Patterns:
#    5x  src/utils/api.py
#    3x  src/components/Header.tsx
#    2x  package.json
#    2x  tsconfig.json
#
# 🔧 Tool Usage:
#   45x  read
#   23x  write
#   12x  exec
#    8x  browser
#    5x  search
```

### Custom Session Directory

```bash
claude-analyzer --session-dir /path/to/sessions
```

## Anti-Patterns Detected

### Duplicate File Reads

```
⚠️  File read 5 times: src/utils/api.py
```

**What it means:** The same file was read multiple times in one session.

**Recommendation:** Consider reading the file once and keeping it in memory, or structure your session to reduce redundant reads.

### Sensitive File Access

```
🔒 Sensitive file accessed: .env
```

**What it means:** A sensitive configuration file was accessed.

**Recommendation:** Be careful with sensitive files. Avoid exposing secrets or API keys.

### Excessive Context Compactions

```
📦 Context compacted 3 times — consider shorter sessions
```

**What it means:** The session's context was compacted multiple times to manage token limits.

**Recommendation:** Break long sessions into shorter, more focused sessions. This improves performance and reduces token usage.

### High Tool Usage

```
🔧 'read' used 45 times — consider batching operations
```

**What it means:** A tool was used many times, which may indicate inefficient operations.

**Recommendation:** Batch operations when possible. For example, read multiple related files at once instead of one at a time.

## Metrics Explained

### Turn Count

Number of turns (user message + Claude response) in the session.

### Tool Calls

Total number of tool invocations in the session.

### Unique Files

Number of unique files accessed during the session.

### Context Compactions

Number of times the session context was compacted to stay within token limits.

### Token Usage

- **Total tokens:** Sum of all tokens used in the session
- **Avg tokens/turn:** Average tokens used per turn

## Use Cases

### Analyze Coding Session

```bash
# Analyze your latest session
claude-analyzer

# Identify inefficiencies
# Get recommendations for improvement
```

### Compare Sessions

```bash
# List recent sessions
claude-analyzer --list

# Analyze each
claude-analyzer session-2026-02-16-14:30.jsonl
claude-analyzer session-2026-02-16-12:15.jsonl

# Compare insights and patterns
```

### Optimize Workflow

```bash
# Get detailed analysis
claude-analyzer --detailed

# Identify:
# - Which files are accessed most frequently
# - Which tools are used most
# - Where context compactions happen
# - Anti-patterns in your session

# Use insights to:
# - Structure sessions better
# - Reduce redundant operations
# - Improve token efficiency
```

### Token Usage Analysis

```bash
# Check token efficiency
claude-analyzer

# If avg tokens/turn is high:
# - Break into shorter sessions
# - Be more concise in messages
# - Provide more context upfront
```

## Best Practices

### Session Structure

**Keep sessions focused:**
```bash
# Analyze sessions
claude-analyzer --detailed

# If context is compacted >2 times:
# - Split into multiple focused sessions
# - Each session should tackle one main task
```

### File Access

**Minimize duplicate reads:**
```bash
# Identify duplicate reads
claude-analyzer

# For files read 3+ times:
# - Read once and reference it
# - Provide context upfront
# - Use --detailed to see patterns
```

### Tool Usage

**Batch operations:**
```bash
# Check tool usage
claude-analyzer --detailed

# For tools used 20+ times:
# - Consider batching
# - Structure requests differently
# - Use more focused prompts
```

### Token Efficiency

**Optimize token usage:**
```bash
# Check avg tokens/turn
claude-analyzer

# If avg > 5,000:
# - Be more concise
# - Provide focused prompts
# - Break into shorter sessions
```

## Integration with Other Tools

### With notes (note taking)

```bash
# Note session insights
claude-analyzer | notes add "Session analysis insights"

# Note specific issues
claude-analyzer --detailed | notes add "File access patterns"
```

### With fsearch (file search)

```bash
# Find files accessed frequently
claude-analyzer --detailed | grep "File Access" -A 10

# Search for specific file
fsearch src/utils/api.py
```

### With timer (time tracking)

```bash
# Track session time
timer --stopwatch

# After session, analyze
claude-analyzer

# Compare time vs insights
```

### With tick (task tracker)

```bash
# Track tasks
tick add "Analyze Claude session patterns"

# After analysis
tick done --note "Found 3 duplicate file reads"
```

### With run (command runner)

```bash
# Store analysis command
run add analyze-claude "claude-analyzer --detailed"

# Run analysis
run analyze-claude
```

## Output Format

### Basic Report

```
======================================================================
📊 Claude Code Session Analysis
======================================================================

📋 Session Summary:
  Turns: 45
  Tool calls: 128
  Unique files: 23
  Context compactions: 2
  Total tokens: 156,780
  Avg tokens/turn: 3,484

💡 Insights & Anti-Patterns:
  ⚠️  File read 5 times: src/utils/api.py
  ⚠️  File read 3 times: src/components/Header.tsx
  📦 Context compacted 2 times — consider shorter sessions
```

### Detailed Report

Includes:
- File access patterns (top 10 files)
- Tool usage (top 10 tools)
- All basic report content

## Technical Details

**Session Format:**
- JSONL (one JSON object per line)
- Located in `~/.claude/` by default
- Can be overridden with `--session-dir`

**Metrics Tracked:**
- Turn count
- Tool calls per tool
- File access frequency
- Context compaction events
- Token usage (if available)

**Analysis Features:**
- Anti-pattern detection
- File access pattern analysis
- Token efficiency calculation
- Tool usage statistics

## Requirements

- Python 3.6+
- Claude Code session logs in JSONL format
- Works on Linux, macOS, Windows

## Limitations

- MVP — basic analysis only
- Focuses on common anti-patterns
- Does not analyze prompt quality
- Limited to what's in session logs
- Token usage depends on Claude Code logging

## Future Improvements

- Advanced pattern detection
- Session comparison
- Trend analysis over time
- Recommendations for optimization
- Integration with Claude Code API
- Export analysis to JSON
- Custom rule configuration

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Analyze. Optimize. Improve.**

Actionable insights for better Claude Code sessions.
