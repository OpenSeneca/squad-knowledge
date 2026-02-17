#!/usr/bin/env python3
"""
blog-assistant — Generate blog post outlines from research

Input: Topic + research notes (from Marcus/Galen learnings)
Output: Blog post outline (section headers, key points, suggested data)

Matches Run Data Run style:
- 1800-2000 words
- Narrative arc (hook → problem → solution → data → conclusion)
- Specific numbers and quotes
- Engaging, conversational tone

Usage:
    blog-assistant --topic "AI in drug discovery" --notes research.md
    blog-assistant --topic "CRISPR" --learnings-from galen
    blog-assistant --topic "Edge AI" --notes ~/workspace/learnings/edge-ai.md
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def find_learnings(agent_name):
    """Find recent learnings from a specific agent."""
    workspace = Path.home() / ".openclaw/workspace"
    learnings_dir = workspace / "learnings"

    if not learnings_dir.exists():
        return []

    # Find files matching pattern
    pattern = re.compile(rf"seed-{agent_name.lower()}", re.IGNORECASE)
    learnings_files = [
        f for f in learnings_dir.glob("*.md")
        if pattern.search(f.name) or f.name.startswith(f"{agent_name.lower()}-")
    ]

    # If no specific agent files, look for recent ones
    if not learnings_files:
        # Get most recent 5 files
        learnings_files = sorted(learnings_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]

    # Read content
    content = []
    for f in learnings_files:
        try:
            with open(f) as file:
                content.append(f.read())
        except Exception as e:
            print(f"Warning: Could not read {f}: {e}")

    return "\n\n---\n\n".join(content)


def extract_key_points(notes):
    """Extract key points from research notes."""
    key_points = []

    # Look for numbered lists
    numbered_items = re.findall(r'^\s*\d+\.\s+(.+)$', notes, re.MULTILINE)
    key_points.extend(numbered_items)

    # Look for bullet points
    bullet_items = re.findall(r'^\s*[\-\*]\s+(.+)$', notes, re.MULTILINE)
    key_points.extend(bullet_items)

    # Look for sentences with keywords (finding, result, shows, data)
    keyword_sentences = re.findall(
        r'.{50,150}(?:finding|result|shows|data|found|demonstrated).{50,150}',
        notes,
        re.IGNORECASE
    )
    key_points.extend(keyword_sentences)

    # Clean and deduplicate
    key_points = [p.strip() for p in key_points if len(p.strip()) > 20]
    key_points = list(dict.fromkeys(key_points))

    return key_points[:15]  # Return up to 15 key points


def extract_quotes(notes):
    """Extract quotes from research notes."""
    quotes = re.findall(r'"([^"]+)"', notes)
    quotes.extend(re.findall(r'`([^`]+)`', notes))

    # Clean and filter
    quotes = [q.strip() for q in quotes if 20 < len(q) < 200]
    quotes = list(dict.fromkeys(quotes))

    return quotes[:10]  # Return up to 10 quotes


def extract_numbers(notes):
    """Extract statistics and numbers from research notes."""
    # Look for percentages, dollar amounts, large numbers
    patterns = [
        r'\d+(?:\.\d+)?%',  # Percentages
        r'\$\d+(?:,\d{3})*(?:\.\d+)?',  # Dollar amounts
        r'\b\d{3,}(?:,\d{3})*\b',  # Large numbers (100+)
        r'\b\d+\s*(?:billion|million|thousand)\b',  # Written numbers
    ]

    numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, notes, re.IGNORECASE)
        numbers.extend(matches)

    # Deduplicate
    numbers = list(dict.fromkeys(numbers))

    return numbers[:10]  # Return up to 10 numbers


def generate_outline(topic, notes, agent_source=None):
    """Generate blog post outline from topic and notes."""
    key_points = extract_key_points(notes)
    quotes = extract_quotes(notes)
    numbers = extract_numbers(notes)

    # Generate title options
    title_options = [
        f"How {topic} Is Changing Everything",
        f"The {topic} Revolution: What You Need to Know",
        f"Why {topic} Matters Now More Than Ever",
        f"Inside the {topic} Shift",
        f"{topic}: The Data-Driven Story",
    ]

    # Generate hook ideas
    hook_ideas = [
        f"Start with a surprising statistic about {topic}",
        f"Open with a real-world {topic} story",
        f"Hook with a common misconception about {topic}",
        f"Begin with the 'before' state of {topic}",
    ]

    # Build outline
    outline = f"""# Blog Post Outline: {topic}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Word count target:** 1800-2000 words
**Style:** Run Data Run (narrative, data-driven, conversational)

---

## Title Options

"""
    for i, title in enumerate(title_options, 1):
        outline += f"{i}. {title}\n"

    outline += f"""
## Hook Ideas (Choose One)

"""
    for i, hook in enumerate(hook_ideas, 1):
        outline += f"{i}. {hook}\n"

    outline += f"""
---

## Section 1: Introduction (200-250 words)

**Goal:** Grab attention, set context, state the main point

### Opening hook
{hook_ideas[0]}

### Context setting
- Briefly introduce {topic}
- Why this matters right now
- What readers will learn

### Thesis statement
[Insert 1-2 sentence thesis about {topic}]

**Suggested data points:** {', '.join(numbers[:3]) if numbers else 'Add relevant statistics'}

---

## Section 2: The Problem (300-350 words)

**Goal:** Set up the tension, show why {topic} is hard/interesting

### Current state
- What's the status quo with {topic}?
- What are the pain points?
- Who is affected?

### Specific challenge
- Pick ONE specific problem related to {topic}
- Show, don't tell (use data, examples)
- Make it concrete

### Stakes
- What happens if this problem isn't solved?
- Why should readers care?

**Key points to include:**
"""

    for i, point in enumerate(key_points[:3], 1):
        outline += f"- {point}\n"

    outline += f"""
**Suggested quotes:**
"""

    for quote in quotes[:2]:
        outline += f'- "{quote}"\n'

    outline += f"""

---

## Section 3: The Shift / Solution (400-450 words)

**Goal:** Show what's changing, introduce the solution

### What's different now
- Recent developments in {topic}
- New approaches or technologies
- Key inflection points

### How it works
- Explain the solution clearly
- Use analogies if helpful
- Keep it accessible but not dumbed down

### Early results
- What's working?
- What's surprising?
- Who's leading the charge?

**Key insights:**
"""

    for i, point in enumerate(key_points[3:6], 1):
        outline += f"- {point}\n"

    outline += f"""
**Suggested data:** {', '.join(numbers[3:6]) if len(numbers) > 3 else 'Add relevant statistics'}

---

## Section 4: The Data (350-400 words)

**Goal:** Back up claims with numbers

### Hard numbers
"""

    if numbers:
        for i, num in enumerate(numbers[:5], 1):
            outline += f"{i}. {num}\n"
    else:
        outline += "- [Add 3-5 specific numbers/statistics here]\n"

    outline += f"""
### Case studies
- [Real-world example 1: company/project/person]
- [Real-world example 2: company/project/person]
- [Real-world example 3: company/project/person]

### Comparisons
- Before vs after data
- {topic} vs alternatives
- Benchmarks and baselines

---

## Section 5: Practical Implications (300-350 words)

**Goal:** What does this mean for readers?

### Who should care
- [Target audience 1]
- [Target audience 2]
- [Target audience 3]

### What to do next
- [Action 1]
- [Action 2]
- [Action 3]

### Common mistakes
- [Mistake 1 to avoid]
- [Mistake 2 to avoid]
- [Mistake 3 to avoid]

---

## Section 6: The Future (200-250 words)

**Goal:** Where is this going?

### Near-term (6-12 months)
- [Prediction 1]
- [Prediction 2]

### Long-term (2-5 years)
- [Prediction 1]
- [Prediction 2]

### Open questions
- What's still unknown?
- What are we watching?

**Key insights:**
"""

    for i, point in enumerate(key_points[6:9], 1):
        outline += f"- {point}\n"

    outline += f"""

---

## Section 7: Conclusion (150-200 words)

**Goal:** Tie it all together, end strong

### Recap
- Restate thesis in new words
- Summarize key points (2-3 bullets)

### Final thought
- [One powerful closing line]

### Call to action
- [What should readers do next?]

---

## Style Notes (Run Data Run)

### Tone
- Conversational but not casual
- Data-driven but not dry
- Opinionated but fair

### Structure
- Narrative arc (hook → problem → solution → data → future)
- Short paragraphs (2-3 sentences max)
- Mix of sentence lengths

### To include
- Specific numbers and quotes
- Real examples (name names)
- Surprising facts
- Concrete takeaways

### To avoid
- Generic statements
- Passive voice
- Clichés
- Too much jargon

---

## Research Notes Summary

**Source:** {agent_source or 'Provided notes'}
**Key points extracted:** {len(key_points)}
**Quotes extracted:** {len(quotes)}
**Numbers/statistics:** {len(numbers)}

### Top 3 Key Points
"""

    for i, point in enumerate(key_points[:3], 1):
        outline += f"{i}. {point}\n"

    outline += f"""

### Top 2 Quotes
"""
    for quote in quotes[:2]:
        outline += f'- "{quote}"\n'

    outline += f"""

### Available Numbers
"""
    if numbers:
        outline += ', '.join(numbers[:8])
    else:
        outline += "[Add numbers from research notes]"

    outline += f"""

---

## Next Steps

1. ✅ Choose a title and hook
2. ✅ Fill in bracketed sections with research
3. ✅ Add 3-5 real-world examples
4. ✅ Verify all numbers and quotes
5. ✅ Write the first draft (aim for 1800-2000 words)
6. ✅ Edit for clarity and flow
7. ✅ Add links and references

---

*Generated by blog-assistant for the OpenSeneca squad*
"""

    return outline


def save_outline(content, topic):
    """Save outline to file."""
    # Generate filename from topic
    filename = topic.lower().replace(' ', '-')
    filename = re.sub(r'[^\w-]', '', filename)

    # Save to outputs/
    output_dir = Path.home() / ".openclaw/workspace/outputs"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / f"{filename}-outline.md"
    output_path.write_text(content)

    print(f"✅ Saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate blog post outline from research notes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate outline from notes file
  blog-assistant --topic "AI in drug discovery" --notes research.md

  # Generate from agent's learnings
  blog-assistant --topic "CRISPR" --learnings-from galen

  # Specify both topic and notes
  blog-assistant --topic "Edge AI" --notes ~/workspace/learnings/edge-ai.md

  # Save to file
  blog-assistant --topic "Biotech trends" --notes research.md --save

Output:
  - Blog post outline (section headers, key points, data)
  - Run Data Run style (1800-2000 words, narrative arc)
  - Saves to outputs/ when --save flag used
        """
    )

    parser.add_argument(
        '--topic',
        required=True,
        help='Blog post topic',
    )

    parser.add_argument(
        '--notes',
        help='Path to research notes file',
    )

    parser.add_argument(
        '--learnings-from',
        help='Agent name to pull learnings from (marcus, galen, etc.)',
    )

    parser.add_argument(
        '--save',
        action='store_true',
        help='Save outline to outputs directory',
    )

    args = parser.parse_args()

    # Check that we have notes
    if args.notes:
        notes_path = Path(args.notes).expanduser()
        if not notes_path.exists():
            print(f"❌ Notes file not found: {notes_path}")
            sys.exit(1)

        with open(notes_path) as f:
            notes = f.read()
        source = f"notes file: {notes_path}"
    elif args.learnings_from:
        print(f"🔍 Finding learnings from {args.learnings_from}...")
        notes = find_learnings(args.learnings_from)

        if not notes:
            print(f"❌ No learnings found for {args.learnings_from}")
            sys.exit(1)

        source = f"learnings from {args.learnings_from}"
        print(f"✅ Found {len(notes):,} characters of learnings")
    else:
        print("❌ Error: Please provide --notes or --learnings-from")
        parser.print_help()
        sys.exit(1)

    # Generate outline
    print(f"\n📝 Generating blog post outline for: {args.topic}")
    print(f"📊 Extracting key points and data...")

    outline = generate_outline(args.topic, notes, source)

    # Print outline
    print("\n" + outline)

    # Save to file if requested
    if args.save:
        save_outline(outline, args.topic)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Outline generation interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
