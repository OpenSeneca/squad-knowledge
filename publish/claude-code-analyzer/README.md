# claude-code-analyzer

Analyze Claude Code session logs and identify inefficiencies. Get actionable insights into your coding sessions.

## What It Does

The Claude Code Session Analyzer parses Claude Code session logs (JSONL format) and provides:

- **Session Summary** — Turn count, tool usage, token efficiency
- **File Access Analysis** — Most frequently accessed files
- **Anti-Pattern Detection** — Duplicate reads, sensitive files
- **Context Usage Patterns** — Compaction events, token efficiency
- **Actionable Insights** — Clear recommendations with "why this matters" and "what to do"

## Installation

### Option 1: Symlink (Linux/macOS)

```bash
# Clone the repo
git clone https://github.com/OpenSeneca/claude-code-analyzer.git
cd claude-code-analyzer

# Symlink to ~/.local/bin
ln -s $(pwd)/claude-analyzer.py ~/.local/bin/claude-analyzer
chmod +x claude-analyzer.py
```

### Option 2: Global Install (Python)

```bash
pip install git+https://github.com/OpenSeneca/claude-code-analyzer.git
```

### Option 3: Run Directly

```bash
python claude-analyzer.py
```

## Requirements

- Python 3.6+
- Claude Code session logs in JSONL format
- `~/.claude/` directory with session files (or custom path)

## Usage

### Analyze Latest Session

```bash
claude-analyzer
```

### Analyze Specific Session

```bash
claude-analyzer session-2026-02-16.jsonl
```

### List Available Sessions

```bash
claude-analyzer --list
```

### Detailed Analysis

```bash
claude-analyzer --detailed
```

### Custom Session Directory

```bash
claude-analyzer --session-dir /path/to/sessions
```

## Examples

### Basic Session Analysis

```bash
$ claude-analyzer

Loading session: session-2026-02-16.jsonl

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
  🔧 'read' used 45 times — consider batching operations
```

### List Sessions

```bash
$ claude-analyzer --list

📁 Available Sessions:

  1. session-2026-02-16.jsonl (2026-02-16 14:30)
  2. session-2026-02-16-12:15.jsonl (2026-02-16 12:15)
  3. session-2026-02-15.jsonl (2026-02-15 16:45)
```

### Detailed Analysis

```bash
$ claude-analyzer --detailed

... (includes file access patterns and tool usage)

📁 File Access Patterns:
   5x  src/utils/api.py
   3x  src/components/Header.tsx
   2x  package.json

🔧 Tool Usage:
  45x  read
  23x  write
  12x  exec
```

## Insights Explained

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

## Troubleshooting

### "No sessions found"

**Check:**
```bash
# Verify session directory exists
ls -la ~/.claude/

# Check for JSONL files
ls ~/.claude/*.jsonl

# Use custom path if needed
claude-analyzer --session-dir /path/to/sessions
```

### "Error loading session"

**Check:**
```bash
# Verify file is valid JSONL
head -1 ~/.claude/session-xxx.jsonl

# Should be valid JSON
```

## Features

- ✅ Session summary (turns, tools, tokens)
- ✅ File access frequency analysis
- ✅ Anti-pattern detection (duplicate reads, sensitive files)
- ✅ Context usage patterns (compactions, token efficiency)
- ✅ Actionable insights and recommendations
- ✅ List available sessions
- ✅ Detailed analysis mode
- ✅ Custom session directory support

## Limitations

- MVP — basic analysis only
- Focuses on common anti-patterns
- Does not analyze prompt quality
- Limited to what's in session logs
- Token usage depends on Claude Code logging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b my-amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin my-amazing-feature`)
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) file for details.

## Author

Built as part of OpenClaw Workspace Toolset

- Repository: https://github.com/openclaw/openclaw
- Tools directory: https://github.com/openclaw/openclaw/tree/main/tools

## See Also

- [OpenSeneca/cli-tools](https://github.com/OpenSeneca/cli-tools) — More CLI tools
- [OpenSeneca/awesome-openclaw-tools](https://github.com/OpenSeneca/awesome-openclaw-tools) — Tool registry

---

**Analyze. Optimize. Improve.**

Actionable insights for better Claude Code sessions.
