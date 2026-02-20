#!/usr/bin/env python3
"""
AI Model Picker - Quick CLI for choosing the right AI model for your task.

Based on February 2026 rankings from LogRocket, helps you quickly compare
AI models across key metrics: SWE-bench, context window, pricing, features.

Usage:
    ai-model-picker [options]

Options:
    --task TYPE       Task type: coding, multimodal, video, reasoning, analysis
    --budget BUDGET    Monthly budget: free, low, medium, high
    --output FORMAT    Output format: table, json (default: table)
    --top N           Show top N models (default: 5)

Examples:
    ai-model-picker --task coding --budget medium
    ai-model-picker --task video --top 3
    ai-model-picker --task multimodal --budget free --output json
"""

import argparse
import json


# February 2026 AI Model Rankings (from LogRocket research)
AI_MODELS = {
    "claude-4.6-opus": {
        "name": "Claude 4.6 Opus",
        "ranking": 1,
        "swe_bench": 80.8,
        "context_window": 1000000,  # 1M
        "context_output": 131072,  # 128K
        "pricing": {"free": False, "monthly": 5, "per_1m": 5},
        "open_source": False,
        "features": ["coding", "reasoning", "tool_use", "autonomous_agent"],
        "multimodal": {"text": True, "image": True, "video": False, "audio": False},
        "best_for": ["coding", "reasoning", "autonomous_agents"]
    },
    "claude-4.5-opus": {
        "name": "Claude 4.5 Opus",
        "ranking": 2,
        "swe_bench": 80.9,
        "context_window": 200000,  # 200K
        "context_output": 65536,  # 64K
        "pricing": {"free": False, "monthly": 5, "per_1m": 5},
        "open_source": False,
        "features": ["coding", "reasoning", "tool_use", "autonomous_agent"],
        "multimodal": {"text": True, "image": True, "video": False, "audio": False},
        "best_for": ["coding", "reasoning", "autonomous_agents"]
    },
    "kimi-k2.5": {
        "name": "Kimi K2.5",
        "ranking": 3,
        "swe_bench": 76.8,
        "context_window": 256000,  # 256K
        "context_output": 1048576,  # 1M
        "pricing": {"free": True, "monthly": 0, "per_1m": 0},
        "open_source": True,
        "license": "Modified MIT",
        "features": ["coding", "reasoning", "agent_swarm", "video_processing", "multimodal"],
        "multimodal": {"text": True, "image": True, "video": True, "audio": False},
        "best_for": ["video", "multimodal", "agent_swarm", "open_source"]
    },
    "gemini-3-pro": {
        "name": "Gemini 3 Pro",
        "ranking": 4,
        "swe_bench": 74.2,
        "context_window": 1000000,  # 1M
        "context_output": 131072,  # 128K
        "pricing": {"free": True, "monthly": 2.4, "per_1m": 2.4},
        "open_source": False,
        "features": ["coding", "reasoning", "video_processing", "multimodal", "voice_input"],
        "multimodal": {"text": True, "image": True, "video": True, "audio": True},
        "best_for": ["video", "multimodal", "voice", "large_context"]
    },
    "gpt-5.2": {
        "name": "GPT-5.2",
        "ranking": 5,
        "swe_bench": 69.0,
        "context_window": 400000,  # 400K
        "context_output": 131072,  # 128K
        "pricing": {"free": True, "monthly": 1.75, "per_1m": 1.75},
        "open_source": False,
        "features": ["coding", "reasoning", "multimodal", "batch_processing"],
        "multimodal": {"text": True, "image": True, "video": True, "audio": True},
        "best_for": ["large_context", "multimodal", "batch_processing"]
    },
    "glm-4.6": {
        "name": "GLM-4.6",
        "ranking": 6,
        "swe_bench": 65.0,
        "context_window": 131072,  # 128K
        "context_output": 65536,  # 64K
        "pricing": {"free": True, "monthly": 0.35, "per_1m": 0.39},
        "open_source": True,
        "license": "MIT",
        "features": ["coding", "reasoning", "tool_use"],
        "multimodal": {"text": True, "image": True, "video": False, "audio": False},
        "best_for": ["open_source", "cost_effective"]
    }
}


def format_number(num):
    """Format numbers with K/M suffix."""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000}K"
    return str(num)


def rank_models(task_type, budget, top_n=5):
    """Rank models based on task type and budget."""

    scored_models = []

    for model_id, model in AI_MODELS.items():
        score = 0
        reasons = []

        # Task type scoring
        if task_type in model["best_for"]:
            score += 30
            reasons.append("Optimal for task type")
        elif task_type in model["features"]:
            score += 15
            reasons.append("Supports task type")

        # Budget scoring
        if budget == "free" and model["pricing"]["free"]:
            score += 25
            reasons.append("Free tier available")
        elif budget == "low" and model["pricing"]["per_1m"] <= 1:
            score += 20
            reasons.append("Low cost")
        elif budget == "medium" and model["pricing"]["per_1m"] <= 3:
            score += 15
            reasons.append("Medium cost")
        elif budget == "high":
            # High budget can afford anything
            score += 10
            reasons.append("Affordable")

        # Performance scoring (SWE-bench)
        score += model["swe_bench"] / 2  # Max 50 points

        # Context window bonus
        if task_type in ["coding", "reasoning"] and model["context_window"] >= 200000:
            score += 10
            reasons.append(f"Large context ({format_number(model['context_window'])})")

        # Multimodal bonus
        if task_type == "multimodal":
            modal_count = sum(model["multimodal"].values())
            if modal_count >= 3:
                score += 15
                reasons.append(f"Strong multimodal ({modal_count} modalities)")

        # Video processing bonus
        if task_type == "video" and model["multimodal"]["video"]:
            score += 25
            reasons.append("Video processing")

        # Open source bonus
        if model["open_source"]:
            score += 10
            reasons.append("Open source")

        scored_models.append({
            "id": model_id,
            "name": model["name"],
            "score": round(score, 2),
            "ranking": model["ranking"],
            "swe_bench": model["swe_bench"],
            "context": model["context_window"],
            "pricing": model["pricing"],
            "open_source": model["open_source"],
            "reasons": reasons
        })

    # Sort by score (descending), then by original ranking
    scored_models.sort(key=lambda x: (-x["score"], x["ranking"]))

    return scored_models[:top_n]


def print_table(models):
    """Print models as formatted table."""

    if not models:
        print("No models found matching criteria.")
        return

    # Header
    print("\n" + "="*120)
    print(f"{'Rank':<6} {'Model':<25} {'Score':<8} {'SWE':<6} {'Context':<10} {'Price/1M':<10} {'Open Src':<9}")
    print("="*120)

    # Rows
    for i, model in enumerate(models, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""
        open_src = "✅" if model["open_source"] else "❌"
        price = "Free" if model["pricing"]["free"] else f"${model['pricing']['per_1m']}"

        print(f"{emoji} {i:<4} {model['name']:<25} {model['score']:<8.2f} "
              f"{model['swe_bench']:<6.1f}% {format_number(model['context']):<10} "
              f"{price:<10} {open_src:<9}")

        print(f"{'':6} {'Reasons':<25} {', '.join(model['reasons'][:2])}")
        print("-"*120)

    # Footer
    print(f"\nTop {len(models)} models ranked by fit for your task type and budget")
    print("\n💡 Use these models in: Claude Code, Kimi Code, Cursor IDE, Windsurf")
    print("📊 Full rankings: https://blog.logrocket.com/ai-dev-tool-power-rankings/\n")


def print_json(models):
    """Print models as JSON."""
    print(json.dumps([{
        "rank": i+1,
        "model": m["name"],
        "score": m["score"],
        "swe_bench": m["swe_bench"],
        "context": m["context"],
        "pricing": m["pricing"],
        "open_source": m["open_source"],
        "reasons": m["reasons"]
    } for i, m in enumerate(models)], indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="AI Model Picker - Choose the right AI model for your task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Best model for coding, medium budget
  ai-model-picker --task coding --budget medium

  # Top 3 models for video processing
  ai-model-picker --task video --top 3

  # Free tier models for multimodal tasks (JSON output)
  ai-model-picker --task multimodal --budget free --output json

Task Types:
  coding       - Code generation, debugging, refactoring
  multimodal   - Text + image + video processing
  video        - Video analysis, processing, generation
  reasoning    - Complex logic, math, analysis
  analysis     - Data analysis, patterns, insights

Budget Levels:
  free         - Must have free tier
  low          - <= $1 per 1M tokens
  medium       - <= $3 per 1M tokens
  high         - Any pricing acceptable
        """
    )

    parser.add_argument("--task", choices=["coding", "multimodal", "video", "reasoning", "analysis"],
                    help="Task type (default: coding)")
    parser.add_argument("--budget", choices=["free", "low", "medium", "high"],
                    help="Monthly budget (default: high)")
    parser.add_argument("--output", choices=["table", "json"],
                    default="table", help="Output format (default: table)")
    parser.add_argument("--top", type=int, default=5,
                    help="Show top N models (default: 5)")

    args = parser.parse_args()

    # Default values
    task_type = args.task or "coding"
    budget = args.budget or "high"

    # Rank models
    models = rank_models(task_type, budget, args.top)

    # Output
    if args.output == "json":
        print_json(models)
    else:
        print_table(models)


if __name__ == "__main__":
    main()
