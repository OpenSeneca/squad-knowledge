# openclaw-session-analyzer

Analyze OpenClaw session logs and evaluate skill effectiveness.

## What It Does

The OpenClaw Session Analyzer parses OpenClaw session logs (JSONL format) and provides:

- **Skill Activation Tracking** — Which skills are used and how often
- **Token Usage Analysis** — Token cost per skill activation
- **Success/Failure Rates** — Tool result status tracking
- **Performance Rankings** — Most/least used skills
- **Aggregated Reports** — Compare across multiple sessions

## Installation

```bash
pip install openclaw-session-analyzer
```

Or symlink:

```bash
ln -s $(pwd)/openclaw-session-analyzer.py ~/.local/bin/openclaw-analyzer
chmod +x openclaw-session-analyzer.py
```

## Quick Start

```bash
# Analyze latest session
openclaw-analyzer

# List available sessions
openclaw-analyzer --list

# Analyze all sessions
openclaw-analyzer --all

# Detailed analysis
openclaw-analyzer --detailed
```

## Examples

### Analyze Latest Session

```bash
$ openclaw-analyzer

📁 Analyzing: c34b89de-3bab-4506-bee5-846904d4ccef.jsonl

======================================================================
📊 OpenClaw Session Analysis
======================================================================

📋 Session Summary:
  Session ID: c34b89de-3bab...
  Start Time: 2026-02-16T04:42:35.413Z
  End Time: 2026-02-16T10:41:12.123Z
  Total Turns: 45
  Total Tokens: 156,780
  Avg Tokens/Turn: 3,484

🔧 Skills Used: 3
  • Coding-agent: 23 activations, 52,345 tokens
  • Github: 12 activations, 34,567 tokens
  • Weather: 8 activations, 18,902 tokens
```

### List Sessions

```bash
$ openclaw-analyzer --list

📁 Available Sessions:

  1. c34b89de-3bab-4506-bee5-846904d4ccef.jsonl (1.9 MB, 2026-02-16 10:41)
  2. b2990682-9e0e-4b91-b304-1693d3d976e8.jsonl (943 KB, 2026-02-16 04:02)
```

### Analyze All Sessions

```bash
$ openclaw-analyzer --all

📁 Found 2 session(s)

[1/2] Analyzing c34b89de-3bab-4506-bee5-846904d4ccef.jsonl...
[2/2] Analyzing b2990682-9e0e-4b91-b304-1693d3d976e8.jsonl...

======================================================================
📊 OpenClaw Sessions - Aggregated Report
======================================================================

📋 Overview:
  Total Sessions: 2
  Total Turns: 78
  Total Tokens: 312,560
```

### Detailed Analysis

```bash
$ openclaw-analyzer --detailed

... (includes detailed metrics)

📈 Detailed Skill Metrics:

  Coding-agent:
    Activations: 45
    Total Tokens: 104,690
    Avg Tokens/Activation: 2326
    Success Rate: 95.6% (43/45)

  Github:
    Activations: 24
    Total Tokens: 69,134
    Avg Tokens/Activation: 2880
    Success Rate: 91.7% (22/24)

💡 Insights:
  ⭐ Most Used: Coding-agent (45 activations)
  📉 Least Used: Weather (8 activations)
  💰 High Token Cost: Coding-agent, Github
  ⚠️  Low Success Rate: None
```

## Metrics Explained

### Skill Activation Count

How many times a skill was activated during the session.

**Interpretation:**
- High count = frequently used skill
- Low count = rarely used skill

**Use case:** Identify which skills get the most use.

### Token Cost

Total tokens consumed by skill activations.

**Interpretation:**
- High cost = expensive skill (consider optimization)
- Low cost = efficient skill

**Use case:** Track token usage and cost.

### Success Rate

Percentage of successful tool results per skill.

**Interpretation:**
- High rate = reliable skill
- Low rate = skill may have issues

**Use case:** Identify problematic skills.

## Evaluation Criteria (Paper Benchmark)

**Question:** What "paper benchmark" should we use?

**Current Implementation:**
- Built-in evaluation criteria
- Success/failure rate tracking
- Token efficiency metrics
- Activation frequency analysis

**Potential Benchmarks:**
1. **Custom benchmark** — Define specific success criteria for each skill type
2. **Academic benchmarks** — Use published AI agent evaluation frameworks
3. **Industry standards** — Compare against industry-wide agent performance

**Recommendation:**
Start with built-in criteria. If specific academic/industry benchmarks are needed, we can:
- Add benchmark definitions per skill
- Calculate benchmark compliance scores
- Compare against published results

**To specify a benchmark:**
1. Define skill categories (e.g., coding, research, infrastructure)
2. Set success criteria per category
3. Define token efficiency thresholds
4. Specify performance targets

**Example:**
```yaml
benchmarks:
  coding:
    success_rate_min: 0.95
    tokens_per_task_max: 5000
  research:
    success_rate_min: 0.90
    tokens_per_task_max: 3000
```

## Features

- ✅ Skill activation tracking
- ✅ Token usage analysis
- ✅ Success/failure rate calculation
- ✅ Performance rankings
- ✅ Multi-session aggregation
- ✅ Detailed metrics
- ✅ List available sessions
- ✅ Custom session directory

## Limitations

- Skill detection is heuristic-based (may miss some activations)
- Tool-to-skill mapping is simplified
- Success rate depends on proper tool result tracking
- No prompt quality analysis
- Limited to what's in session logs

## Contributing

Contributions welcome! Submit a Pull Request.

## License

MIT License

## Author

OpenClaw Workspace Toolset

## See Also

- [claude-code-analyzer](https://github.com/OpenSeneca/claude-code-analyzer) — Claude Code session analyzer
- [OpenSeneca/cli-tools](https://github.com/OpenSeneca/cli-tools) — More CLI tools

---

**Analyze. Evaluate. Improve.**

Skill effectiveness metrics for OpenClaw sessions.
