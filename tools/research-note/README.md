# Research Note Taker

A CLI tool for quickly logging research findings. Takes a topic or URL, extracts content, and saves a structured note.

## Why This Matters

Marcus and Galen do a lot of research (AI papers, biopharma studies, competitor analysis). This tool makes it easy to:

- Quickly log research findings in a structured format
- Fetch and save content from URLs (arXiv, blogs, papers)
- Tag notes for easy retrieval
- Maintain a research log over time

## Installation

```bash
cd ~/.openclaw/workspace/tools/research-note
chmod +x research-note
ln -sf $(pwd)/research-note ~/.local/bin/research-note
```

## Usage

### Interactive Mode

Best for detailed research logging:

```bash
research-note --interactive
```

Prompts for:
- Research topic or URL
- Your notes
- Key points (comma-separated)
- Tags (comma-separated)

### Quick Mode

Fast logging from CLI:

```bash
# Log a topic
research-note "GPT-5 benchmark results" \
  --note "New model shows 40% improvement on reasoning tasks" \
  --tags "ai,models,benchmarking" \
  --keypoints "reasoning improved, math unchanged"

# Fetch and log from URL
research-note "https://arxiv.org/abs/2401.12345" \
  --note "Paper discusses new attention mechanism" \
  --tags "arxiv,attention,transformers"
```

### Output

Saves notes to `~/clawd/research/` (or custom directory with `--output`):

```
~/clawd/research/
├── 2026-02-21-gpt-5-benchmark-results.md
├── 2026-02-21-new-attention-mechanism.md
└── 2026-02-21-competitive-landscape.md
```

### Note Format

```markdown
# GPT-5 Benchmark Results

## Source
GPT-5 benchmark results

## Date
2026-02-21

## Notes
New model shows 40% improvement on reasoning tasks

## Key Points
- Reasoning improved
- Math unchanged

## Tags
ai, models, benchmarking

---
Agent: archimedes
Session: cli
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--interactive` | `-i` | Interactive mode (prompts for input) |
| `--note TEXT` | `-n` | Research notes |
| `--tags TAGS` | `-t` | Comma-separated tags |
| `--keypoints POINTS` | `-k` | Comma-separated key points |
| `--output DIR` | `-o` | Output directory (default: ~/clawd/research) |

## For the Squad

**Marcus**: Use this when discovering new AI tools, frameworks, or papers. Log findings before they fade.

**Galen**: Use for biopharma research papers, clinical trial results, or competitive analysis.

**Archimedes**: Use for technical research, tool exploration, or prototype documentation.

## Examples

### Researching AI Tools

```bash
research-note "Tambo AI - Generative UI SDK" \
  --note "React SDK for building AI-powered apps. Register components with Zod schemas, agent renders them dynamically. Could be useful for squad dashboard." \
  --tags "ai,react,ui,tambo" \
  --keypoints "component registration, streaming props, agent-driven UI"
```

### Logging arXiv Papers

```bash
research-note "https://arxiv.org/abs/2401.12345" \
  --note "Proposes new attention mechanism for transformers. Early results show 15% speedup." \
  --tags "arxiv,attention,transformers"
```

### Competitive Intelligence

```bash
research-note "Anthropic Claude 4 release" \
  --note "New model launched with improved coding capabilities. Pricing increased 20%." \
  --tags "anthropic,claude,competition" \
  --key-points "coding improved, pricing up, new features"
```

## Integration

Works well with other research tools:

```bash
# After reading a paper with paper-summarizer
paper-summarizer https://arxiv.org/abs/2401.12345 | \
  xargs -I {} research-note "https://arxiv.org/abs/2401.12345" --note "{}"

# Export notes for research-digest
research-digest ~/clawd/research/
```

## Customization

Change output directory:

```bash
# Use custom research directory
export RESEARCH_DIR=~/notes/research
research-note "topic" --note "notes"

# Or use --output flag
research-note "topic" --note "notes" --output ~/custom/path
```

## Notes

- URLs are fetched via HTTP/HTTPS (no API key needed)
- Large URLs may time out; use `--note` for the content
- Filenames are auto-generated from title + date
- Notes are saved in Markdown for easy editing

## License

MIT
