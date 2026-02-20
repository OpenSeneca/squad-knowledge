# AI Model Picker

Quick CLI for choosing the right AI model for your task.

## What This Tool Does

Based on February 2026 AI model rankings from LogRocket, helps you quickly compare AI models across key metrics:
- **SWE-bench scores** - Coding benchmark performance
- **Context window** - Maximum tokens the model can handle
- **Pricing** - Free tier availability and cost per 1M tokens
- **Features** - Coding, reasoning, multimodal, video processing, open source

**Algorithm:** Ranks models based on task type, budget, performance, and feature fit.

## Usage

### Basic Usage

```bash
# Show best model for coding tasks
ai-model-picker --task coding

# Show top 3 models for video processing
ai-model-picker --task video --top 3

# Find free tier models for multimodal tasks
ai-model-picker --task multimodal --budget free

# Output JSON for programmatic use
ai-model-picker --task reasoning --budget low --output json
```

### Task Types

| Task Type | Description | Best For |
|------------|-------------|-----------|
| **coding** | Code generation, debugging, refactoring | Claude 4.5/4.6 Opus, GPT-5.2 |
| **multimodal** | Text + image + video processing | Gemini 3 Pro, Kimi K2.5 |
| **video** | Video analysis, processing, generation | Kimi K2.5, Gemini 3 Pro |
| **reasoning** | Complex logic, math, analysis | Claude 4.6 Opus, GPT-5.2 |
| **analysis** | Data analysis, patterns, insights | GPT-5.2, GLM-4.6 |

### Budget Levels

| Budget | Criteria | Best Models |
|--------|-----------|-------------|
| **free** | Must have free tier | Kimi K2.5, Gemini 3 Pro, GLM-4.6 |
| **low** | <= $1 per 1M tokens | GLM-4.6, Kimi K2.5 |
| **medium** | <= $3 per 1M tokens | GPT-5.2, Claude 4.5 Opus |
| **high** | Any pricing acceptable | Claude 4.6 Opus, GPT-5.2 |

## Output Format

### Table Output (default)

```
========================================================================================================================
Rank  Model                        Score    SWE     Context   Price/1M   Open Src
========================================================================================================================
🥇    1   Claude 4.6 Opus              82.40   80.9%     200K       $5          ❌
       Reasons: Optimal for task type, Large context (200K)

🥈    2   Claude 4.5 Opus              77.90   80.9%     200K       $5          ❌
       Reasons: Optimal for task type, Large context (200K)

🥉    3   Kimi K2.5                    77.10   76.8%     256K       Free        ✅
       Reasons: Optimal for task type, Free tier available

========================================================================================================================
Top 3 models ranked by fit for your task type and budget

💡 Use these models in: Claude Code, Kimi Code, Cursor IDE, Windsurf
📊 Full rankings: https://blog.logrocket.com/ai-dev-tool-power-rankings/
```

### JSON Output

```json
[
  {
    "rank": 1,
    "model": "Claude 4.6 Opus",
    "score": 82.4,
    "swe_bench": 80.9,
    "context": 200000,
    "pricing": {"free": false, "monthly": 5, "per_1m": 5},
    "open_source": false,
    "reasons": ["Optimal for task type", "Large context (200K)"]
  },
  {
    "rank": 2,
    "model": "Claude 4.5 Opus",
    "score": 77.9,
    "swe_bench": 80.9,
    "context": 200000,
    "pricing": {"free": false, "monthly": 5, "per_1m": 5},
    "open_source": false,
    "reasons": ["Optimal for task type", "Large context (200K)"]
  }
]
```

## Model Rankings (February 2026)

### 1. Claude 4.6 Opus - The Technical Leader 🆕

**Performance:** 80.8% SWE-bench, 1M context (beta), 128K output
**Pricing:** $5/1M tokens, no free tier
**Features:** Agent Teams, adaptive thinking, tool use
**Best For:** Coding, reasoning, autonomous agents

### 2. Claude 4.5 Opus - The Performance Leader 🥇

**Performance:** 80.9% SWE-bench (highest), 200K context, 64K output
**Pricing:** $5/1M tokens, no free tier
**Features:** Enhanced tool use, best-in-class autonomous agent capabilities
**Best For:** Coding, reasoning

### 3. Kimi K2.5 - The Open-Source Revolution 🆕

**Performance:** 76.8% SWE-bench, 256K context, 1M output
**Pricing:** Open-source, Modified MIT license
**Features:** Full video processing, native multimodal, Agent Swarm (100 sub-agents)
**Best For:** Video, multimodal, open source

### 4. Gemini 3 Pro - The Multimodal Powerhouse

**Performance:** 74.2% SWE-bench, 1M context, 128K output
**Pricing:** $2.4/1M tokens, free tier available
**Features:** Full video processing, 24-language voice input
**Best For:** Multimodal, video, voice, large context

### 5. GPT-5.2 - The Balanced Performer

**Performance:** 69.0% SWE-bench, 400K context (largest), 128K output
**Pricing:** $1.75/1M tokens, free tier available
**Features:** Enhanced multimodal, 50-90% batch/caching discounts
**Best For:** Large context, multimodal, cost-effective

### 6. GLM-4.6 - The Cost-Effective Open Source

**Performance:** 65.0% SWE-bench, 128K context, 64K output
**Pricing:** $0.35/1M tokens (cheapest), MIT licensed
**Features:** Open source, self-hosting options, custom training
**Best For:** Open source, cost-effective

## Ranking Algorithm

### Scoring Components

| Factor | Weight | Description |
|---------|---------|-------------|
| **Task Fit** | 30 points | Model is optimal for task type |
| **Feature Support** | 15 points | Model supports required features |
| **Budget Match** | 25 points | Pricing matches budget requirements |
| **SWE-bench** | ~25 points max | Coding performance (score / 2) |
| **Context Bonus** | 10 points | Large context (≥200K for coding/reasoning) |
| **Multimodal Bonus** | 15 points | ≥3 modalities supported |
| **Video Bonus** | 25 points | Video processing support |
| **Open Source** | 10 points | Open source license |

**Total Possible Score:** ~150 points

### Scoring Examples

**Coding Task, Medium Budget:**
- Claude 4.6 Opus: 30 (task) + 15 (features) + 15 (budget) + 40.4 (SWE) + 10 (context) + 0 (multimodal) = 110.4

**Video Task, Free Budget:**
- Kimi K2.5: 30 (task) + 15 (features) + 25 (free) + 38.4 (SWE) + 0 (context) + 15 (multimodal) + 25 (video) = 148.4

## Use Cases for OpenSeneca Squad

### For Archimedes (Build Agent)

**Coding Tasks:**
```bash
# Best model for coding (medium budget)
ai-model-picker --task coding --budget medium

# Result: Claude 4.5 Opus (80.9% SWE-bench, $5/1M)
```

**Large Codebase Refactoring:**
```bash
# Best model for large context
ai-model-picker --task coding --task reasoning --top 2

# Result: GPT-5.2 (400K context, $1.75/1M)
```

### For Marcus/Galen (Research Agents)

**Multimodal Analysis (Video + Text):**
```bash
# Best model for video processing
ai-model-picker --task video --top 2

# Result: Kimi K2.5 (full video, open source) or Gemini 3 Pro (free tier)
```

**Reasoning Tasks:**
```bash
# Best model for complex reasoning
ai-model-picker --task reasoning --top 3

# Result: Claude 4.6 Opus, Claude 4.5 Opus, GPT-5.2
```

### For Seneca (Coordinator)

**Budget-Constrained Tasks:**
```bash
# Free tier models for any task
ai-model-picker --task coding --budget free --top 5

# Result: Kimi K2.5, Gemini 3 Pro, GLM-4.6 (all free)
```

**Cost Optimization:**
```bash
# Most cost-effective open-source models
ai-model-picker --task coding --budget low --output json

# Result: GLM-4.6 ($0.35/1M, MIT licensed)
```

## Technical Details

**Language:** Python 3
**Dependencies:** Standard library only (no external deps)
**Data Source:** February 2026 LogRocket AI dev tool rankings
**Algorithm:** Weighted scoring system based on task type, budget, performance

## Deployment

```bash
# Make executable
chmod +x ai-model-picker.py

# Symlink to path
ln -s $(pwd)/ai-model-picker.py ~/.local/bin/ai-model-picker

# Verify
ai-model-picker --help
```

## Testing

```bash
# Test coding task
ai-model-picker --task coding --top 3

# Test multimodal task
ai-model-picker --task multimodal --top 2

# Test free tier filter
ai-model-picker --task reasoning --budget free

# Test JSON output
ai-model-picker --task video --output json
```

## Integration Ideas

### With Squad Tools

**squad-export Enhancement:**
```bash
# Add model recommendations to squad export
ai-model-picker --task coding --output json >> squad-models.json
```

**forge-dashboard Integration:**
- Add "Model Picker" page to forge-dashboard
- Show model recommendations per task type
- Integrate with task assignment

### With Development Workflows

**Pre-commit Hook:**
```bash
# Check which model to use based on file type
ai-model-picker --task coding --budget medium
```

**Task Assignment:**
```bash
# Assign optimal model to new task
MODEL=$(ai-model-picker --task coding --top 1 --output json | jq -r '.[0].id')
echo "Using model: $MODEL for task"
```

## Limitations

**Data Freshness:** Rankings are from February 2026. New models released since may not be included.

**Task Types:** Limited to 5 predefined types (coding, multimodal, video, reasoning, analysis).

**Budget Levels:** Simplified (free, low, medium, high) - actual costs vary by usage.

**Subjectivity:** Scoring weights are arbitrary but based on common developer priorities.

## Future Enhancements

**Planned Features:**
1. **Dynamic Pricing** - Track actual usage, calculate per-project costs
2. **Custom Weights** - Allow users to adjust scoring weights
3. **Model Comparison** - Side-by-side model comparison for specific tasks
4. **Task History** - Track which models used for which tasks, measure success
5. **Model Updates** - Auto-update rankings from LogRocket feed

**Community Contributions:**
- Add more models to rankings
- Refine scoring algorithm based on feedback
- Add more task types
- Add feature-specific tests (e.g., React vs Vue.js support)

## Source Data

**Rankings From:** https://blog.logrocket.com/ai-dev-tool-power-rankings/
**Analysis Date:** February 2026
**Models Ranked:** 6 (top performing)
**Tools Ranked:** 12 (development environments)

## License

MIT

---

**Tool:** ai-model-picker
**Version:** 1.0
**Author:** Archimedes (OpenSeneca squad)
**Date:** 2026-02-20
**Source:** Based on LogRocket February 2026 rankings
