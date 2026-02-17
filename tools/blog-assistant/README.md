# blog-assistant — Blog Post Outline Generator

Generate structured blog post outlines from research notes, matching Run Data Run style.

## What It Does

blog-assistant takes your research and creates a blog post outline with:

- **7 structured sections** (Introduction → Problem → Shift → Data → Implications → Future → Conclusion)
- **Title options** (5 catchy titles)
- **Hook ideas** (4 attention-grabbing openers)
- **Key points extraction** (from research notes)
- **Quote extraction** (pulls relevant quotes)
- **Number/statistic extraction** (identifies data points)
- **Style guide** (Run Data Run conventions)

**Run Data Run Style:**
- 1800-2000 words
- Narrative arc (hook → problem → solution → data → conclusion)
- Specific numbers and quotes
- Conversational, data-driven tone
- Real examples, no jargon

## Installation

```bash
ln -s /path/to/blog-assistant.py ~/.local/bin/blog-assistant
chmod +x blog-assistant.py
```

Already symlinked in this workspace: `~/.local/bin/blog-assistant`

## Usage

### Generate Outline from Research Notes

```bash
blog-assistant --topic "AI in drug discovery" --notes research.md
```

### Generate from Agent's Learnings

```bash
blog-assistant --topic "CRISPR" --learnings-from galen
```

### Save Outline to File

```bash
blog-assistant --topic "Edge AI" --notes research.md --save
```

## Examples

### From Notes File

```bash
$ blog-assistant --topic "Startup Accelerators" --notes tinyseed-analysis.md

📝 Generating blog post outline for: Startup Accelerators
📊 Extracting key points and data...

# Blog Post Outline: Startup Accelerators

**Generated:** 2026-02-17 19:53 UTC
**Word count target:** 1800-2000 words
**Style:** Run Data Run (narrative, data-driven, conversational)

---

## Title Options

1. How Startup Accelerators Is Changing Everything
2. The Startup Accelerators Revolution: What You Need to Know
3. Why Startup Accelerators Matters Now More Than Ever
4. Inside the Startup Accelerators Shift
5. Startup Accelerators: The Data-Driven Story

## Hook Ideas (Choose One)

1. Start with a surprising statistic about Startup Accelerators
2. Open with a real-world Startup Accelerators story
3. Hook with a common misconception about Startup Accelerators
4. Begin with the 'before' state of Startup Accelerators

---

## Section 1: Introduction (200-250 words)

**Goal:** Grab attention, set context, state the main point

### Opening hook
Start with a surprising statistic about Startup Accelerators

### Context setting
- Briefly introduce Startup Accelerators
- Why this matters right now
- What readers will learn

### Thesis statement
[Insert 1-2 sentence thesis about Startup Accelerators]

**Suggested data points:** 12%, 43%, 100%

---

## Section 2: The Problem (300-350 words)

**Goal:** Set up the tension, show why Startup Accelerators is hard/interesting

**Key points to include:**
- **Tech Alignment:** TinySeed focuses on SaaS + OpenSeneca is building agent SaaS
- **Remote Ready:** Squad already remote (5 agents on Tailscale network)
- **Revenue Potential:** Enterprise web agents is hot market with clear monetization

**Suggested quotes:**
- "Multi-agent research platform for biopharma"
- "Enterprise web agent orchestration dashboard"

...

---

## Research Notes Summary

**Source:** notes file: tinyseed-analysis.md
**Key points extracted:** 15
**Quotes extracted:** 3
**Numbers/statistics:** 10

### Top 3 Key Points
1. **Tech Alignment:** TinySeed focuses on SaaS + OpenSeneca is building agent SaaS
2. **Remote Ready:** Squad already remote (5 agents on Tailscale network)
3. **Revenue Potential:** Enterprise web agents is hot market with clear monetization

### Top 2 Quotes
- "Multi-agent research platform for biopharma"
- "Enterprise web agent orchestration dashboard"

### Available Numbers
12%, 43%, 100%, $120, $220, $250, $300, $1
```

### Save to File

```bash
$ blog-assistant --topic "Startup Accelerators" --notes tinyseed-analysis.md --save

📝 Generating blog post outline for: Startup Accelerators
📊 Extracting key points and data...

[outline output]

✅ Saved: /home/exedev/.openclaw/workspace/outputs/startup-accelerators-outline.md
```

## Output Format

The outline includes 7 sections:

```
# Blog Post Outline: [Topic]

## Title Options
5 catchy title ideas

## Hook Ideas
4 attention-grabbing openers

---

## Section 1: Introduction (200-250 words)
Grab attention, set context, thesis statement

## Section 2: The Problem (300-350 words)
Current state, specific challenge, stakes

## Section 3: The Shift / Solution (400-450 words)
What's changing, how it works, early results

## Section 4: The Data (350-400 words)
Hard numbers, case studies, comparisons

## Section 5: Practical Implications (300-350 words)
Who should care, what to do next, common mistakes

## Section 6: The Future (200-250 words)
Near-term predictions, long-term vision, open questions

## Section 7: Conclusion (150-200 words)
Recap, final thought, call to action

---

## Style Notes (Run Data Run)
Tone, structure, to include, to avoid

## Research Notes Summary
Key points, quotes, numbers, next steps
```

## Features

- ✅ **7-section outline** (Introduction → Problem → Shift → Data → Implications → Future → Conclusion)
- ✅ **Title options** (5 variations)
- ✅ **Hook ideas** (4 attention-grabbing openers)
- ✅ **Key points extraction** (up to 15)
- ✅ **Quote extraction** (up to 10)
- ✅ **Number/statistic extraction** (up to 10)
- ✅ **Run Data Run style guide** (tone, structure, conventions)
- ✅ **Word count targets** (per section)
- ✅ **Save to file** option
- ✅ **Agent learnings integration** (pull from marcus, galen, etc.)
- ✅ **Zero external dependencies** (pure Python)

## Use Cases

### For Justin (Run Data Run)

```bash
# Generate outline from research
blog-assistant --topic "AI in biopharma" --notes research.md --save

# Pull from Galen's learnings
blog-assistant --topic "CRISPR applications" --learnings-from galen --save

# Quick outline for meeting prep
blog-assistant --topic "Edge AI" --notes ~/intel/edge-ai.md
```

### For Marcus (AI Research)

```bash
# Summarize AI paper into blog outline
blog-assistant --topic "Transformers in 2026" --notes paper-summary.md

# Generate from agent research notes
blog-assistant --topic "Multi-agent systems" --learnings-from marcus
```

### For Galen (Biopharma Research)

```bash
# Biopharma topic outline
blog-assistant --topic "CRISPR Cas9" --notes crispr-research.md

# Drug discovery blog outline
blog-assistant --topic "AI in drug discovery" --learnings-from galen
```

## What Gets Extracted

### Key Points
- Numbered lists (`1. Point`)
- Bullet points (`- Point`)
- Sentences with keywords (finding, result, shows, data, found, demonstrated)

### Quotes
- Double quotes (`"text"`)
- Backticks (`` `text` ``)

### Numbers/Statistics
- Percentages (`43%`, `12.5%`)
- Dollar amounts (`$120`, `$1M`, `$5,000`)
- Large numbers (`100`, `1000`, `10000`)
- Written numbers (`1 billion`, `2 million`)

## Style Notes (Run Data Run)

### Tone
- Conversational but not casual
- Data-driven but not dry
- Opinionated but fair

### Structure
- Narrative arc (hook → problem → solution → data → future)
- Short paragraphs (2-3 sentences max)
- Mix of sentence lengths

### To Include
- Specific numbers and quotes
- Real examples (name names)
- Surprising facts
- Concrete takeaways

### To Avoid
- Generic statements
- Passive voice
- Clichés
- Too much jargon

## Tips

1. **Use rich research** — more content = better extraction
2. **Include numbers** — stats and percentages make blogs stronger
3. **Use real quotes** — adds authenticity
4. **Choose 1 title** — pick the best from 5 options
5. **Pick 1 hook** — go with your gut
6. **Fill brackets** — the outline is a skeleton, you add the meat
7. **Add examples** — real-world examples make posts engaging

## Troubleshooting

### No Key Points Extracted

```bash
# Ensure notes have structured content
# Use numbered lists or bullet points
# Include "finding", "result", "shows", "data" in text
```

### Wrong Topic in Titles

The template uses your exact topic. If it doesn't fit:

```bash
# Edit the generated outline
vim outputs/your-topic-outline.md

# Or use a better topic name
blog-assistant --topic "The Future of AI" --notes research.md
```

### No Numbers/Quotes Found

```bash
# Add explicit numbers to research notes
# Use real quotes from sources
# Include percentages and dollar amounts
```

## Workflow

### 1. Research
- Marcus/Galen produce research notes
- Justin adds context and numbers

### 2. Generate Outline
```bash
blog-assistant --topic "Your Topic" --notes research.md --save
```

### 3. Fill in Brackets
- Choose 1 title and 1 hook
- Fill bracketed sections with research
- Add 3-5 real-world examples

### 4. Write Draft
- Aim for 1800-2000 words
- Follow Run Data Run style
- Use extracted quotes and numbers

### 5. Edit and Publish
- Edit for clarity and flow
- Add links and references
- Publish to Run Data Run

## Integration with Other Tools

### Squad Output Digest

```bash
# Get today's digest
squad-output-digest

# Generate blog from digest
blog-assistant --topic "Today's Research" --notes outputs/daily-digest-2026-02-17.md
```

### Paper Summarizer

```bash
# Summarize paper
paper-summarizer https://arxiv.org/abs/2401.00001 --save

# Generate blog from summary
blog-assistant --topic "New AI Research" --notes outputs/abs-2401.00001.md
```

## Future Enhancements

- [ ] Markdown export with bracketed sections highlighted
- [ ] Word count estimation per section
- [ ] Suggest real-world examples based on topic
- [ ] Integration with Run Data Run CMS
- [ ] Draft generation (not just outline)
- [ ] SEO optimization suggestions
- [ ] Title A/B testing suggestions

## Limitations

- **Not a full writer** — generates outlines, not complete posts
- **Depends on input quality** — better research = better outline
- **Template-based** — follows structure, may need adjustments
- **No creativity** — you add the original ideas and voice

## License

MIT License

## Author

OpenSeneca Squad Toolset

---

**Blog outlines in seconds. Drafts in minutes.**

For Justin, Marcus, Galen — and anyone writing data-driven posts.
