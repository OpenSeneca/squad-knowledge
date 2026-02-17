# squad-eval — Squad Agent Evaluation Tool

Evaluate squad agent performance with role-specific metrics.

## What It Does

The squad-eval tool evaluates agents based on their role and outputs detailed performance metrics:

**Research Agents (Marcus/Galen):**
- Learning frequency (last 7 days)
- Learning depth score (avg file size)
- Sources/references cited
- Business relevance score

**Ops Agents (Argus):**
- Uptime status
- Health checks performed
- Alerts sent
- Response time

**Build Agents (Archimedes):**
- Tools shipped
- Fixes deployed
- Tests run
- Code quality (documentation coverage)

## Installation

Symlink from workspace:

```bash
ln -s /path/to/squad-eval.py ~/.local/bin/squad-eval
chmod +x ~/.local/bin/squad-eval
```

Already symlinked in this workspace: `~/.local/bin/squad-eval`

## Usage

### Evaluate All Agents

```bash
squad-eval --all
```

### Evaluate Single Agent

```bash
squad-eval marcus
squad-eval galen
squad-eval argus
squad-eval archimedes
```

### JSON Output

```bash
squad-eval --all --json
squad-eval archimedes --json
```

## Examples

### Evaluate All Agents

```bash
$ squad-eval --all

======================================================================
📊 Squad Evaluation Summary
======================================================================

1. Marcus — 🟡 62.5/100 (Research)
2. Archimedes — 🟡 65.4/100 (Build)
3. Galen — 🟢 78.3/100 (Research)
4. Argus — 🟢 85.7/100 (Ops)
```

### Evaluate Single Agent

```bash
$ squad-eval archimedes

✅ Archimedes (Build)
   Score: 🟡 65.4/100
   Status: ACTIVE
   Last Learning: seed-squad-tools-ideas.md
   Last Output: 2026-02-16-summary.md
   🔧 Tools: 35
   🔨 Fixes: 228
   🧪 Tests: 0
   📖 Documentation: 32/35 tools documented
```

### Research Agent Evaluation

```bash
$ squad-eval marcus

✅ Marcus (Research)
   Score: 🟢 78.3/100
   Status: ACTIVE
   Last Learning: 2026-02-16-biopharma-ai.md
   Last Output: 2026-02-16.md
   📚 Recent Learnings: 12 in last 7 days
   📏 Avg Size: 42.5 KB
   🔗 Sources: 18
   💼 Business Relevance: 7 keyword matches
```

### Ops Agent Evaluation

```bash
$ squad-eval argus

✅ Argus (Ops)
   Score: 🟢 85.7/100
   Status: ACTIVE
   Last Learning: system-monitoring-improvements.md
   Last Output: 2026-02-17.md
   🩺 Health Checks: 23
   🚨 Alerts: 3
   📡 Service: UP
```

### JSON Output

```bash
$ squad-eval archimedes --json

{
  "agent_name": "Archimedes",
  "role": "build",
  "score": 65.4,
  "metrics": {
    "tools_shipped": 35,
    "fixes_deployed": 228,
    "tests_run": 0,
    "code_quality": 91.4
  },
  "details": {
    "tools": "35",
    "fixes": "228",
    "tests": "0",
    "documentation": "32/35 tools documented"
  },
  "status": "active",
  "last_learning": "seed-squad-tools-ideas.md",
  "last_output": "2026-02-16-summary.md"
}
```

## Metrics Explained

### Research Agents

**Learning Frequency (25% of score)**
- Number of learnings created in last 7 days
- Benchmark: 14 (2 per day)

**Learning Depth (25% of score)**
- Average size of learning files
- Indicates research thoroughness
- Benchmark: 50 KB

**Sources Cited (25% of score)**
- Number of URLs/references in learnings
- Indicates research quality
- Benchmark: 20 sources

**Business Relevance (25% of score)**
- Keyword matches to relevant topics
- Topics: biopharma, AI, drug, clinical, FDA, etc.
- Benchmark: 10 keyword matches

### Ops Agents

**Uptime (40% of score)**
- OpenClaw service status via systemctl
- Binary: UP/DOWN

**Health Checks (20% of score)**
- Number of health checks in last hour
- From journal logs
- Benchmark: 10 checks

**Alerts Sent (20% of score)**
- Number of alerts/warnings/errors
- From journal logs
- Fewer is generally better
- Benchmark: 5 alerts

**Response Time (20% of score)**
- Placeholder for future implementation
- Will track actual request times

### Build Agents

**Tools Shipped (25% of score)**
- Number of tools in workspace/tools/
- Indicates productivity
- Benchmark: 50 tools

**Fixes Deployed (25% of score)**
- Number of fixes/deployments in memory
- Indicates maintenance activity
- Benchmark: 20 fixes

**Tests Run (25% of score)**
- Number of test files in tools
- Indicates testing coverage
- Benchmark: 10 tests

**Code Quality (25% of score)**
- Documentation coverage (README.md per tool)
- Indicates maintainability
- Benchmark: 100%

## Scoring

**Score Ranges:**
- 🟢 75-100: Excellent
- 🟡 50-74: Good
- 🔴 0-49: Needs Improvement

**Status Codes:**
- ACTIVE: Agent produced output in last 2 days
- INACTIVE: No recent output
- DOWN: Service not running (ops agents)
- UNKNOWN: Cannot determine status

## Data Sources

### Directory Search

The tool checks **both** `learnings/` and `outputs/` directories:

- `~/.openclaw/learnings/` — Research learnings and seed files
- `~/.openclaw/workspace/outputs/` — Generated outputs
- `~/.openclaw/workspace/memory/` — Daily summaries

### SSH Access

For remote agents, uses SSH to:
- Check systemctl status (uptime)
- Read journal logs (health checks, alerts)

**Hostnames:**
- marcus-squad (100.98.223.103)
- galen-squad (100.123.121.125)
- archimedes-squad (100.100.56.102)
- argus-squad (100.108.219.91)

## Troubleshooting

### SSH Connection Failed

```bash
# Test SSH connection
ssh marcus-squad

# Check Tailscale IP
tailscale ip -4
```

### No Learnings Found

```bash
# Check learnings directory
ls -la ~/.openclaw/learnings/

# Check outputs directory
ls -la ~/.openclaw/workspace/outputs/
```

### Wrong Metrics

Ensure the agent ID is correct:
- `marcus` (research)
- `galen` (research)
- `argus` (ops)
- `archimedes` (build)

## Features

- ✅ Role-specific evaluation criteria
- ✅ Checks both learnings/ and outputs/ directories
- ✅ SSH to remote agents for status
- ✅ JSON output for automation
- ✅ Color-coded scores and status
- ✅ Detailed metrics per role
- ✅ Aggregate summary for all agents

## Limitations

- Some metrics are heuristic-based (not precise)
- Requires SSH access to remote agents
- Business relevance uses keyword matching (simplistic)
- Response time not yet implemented (placeholder)
- Success rate depends on proper logging

## Contributing

To add new metrics or improve existing ones:

1. Edit `squad-eval.py`
2. Add new metric to role-specific evaluation function
3. Update score normalization
4. Test on all 4 agents

## License

MIT License — see LICENSE file

## Author

Built for OpenSeneca Squad

---

**Evaluate. Score. Improve.**

Role-specific metrics for squad agent performance.
