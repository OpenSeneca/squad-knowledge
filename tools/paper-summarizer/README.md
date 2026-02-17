# paper-summarizer — Structured Paper Summaries

Generate structured summaries for research papers and articles from URLs or arXiv IDs.

## What It Does

paper-summarizer fetches web content and extracts:

- **Title** — Paper/article title
- **Authors** — Authors or author list
- **Abstract** — Full abstract section
- **Key Findings** — Bullet points from results/conclusion sections
- **Methodology** — Research methods used
- **Implications** — Impact and significance
- **Reference** — URL and fetch timestamp

## Installation

```bash
ln -s /path/to/paper-summarizer.py ~/.local/bin/paper-summarizer
chmod +x paper-summarizer.py
```

Already symlinked in this workspace: `~/.local/bin/paper-summarizer`

## Usage

### Summarize arXiv Paper

```bash
paper-summarizer https://arxiv.org/abs/2401.00001
```

### Use arXiv ID Only

```bash
paper-summarizer 2401.00001
```

### Summarize Any URL

```bash
paper-summarizer https://example.com/paper
```

### Save Summary to File

```bash
paper-summarizer https://arxiv.org/abs/2401.00001 --save
```

### Include JSON Metadata

```bash
paper-summarizer https://arxiv.org/abs/2401.00001 --json
```

## Examples

### ArXiv Paper Summary

```bash
$ paper-summarizer 2401.00001

🔍 ArXiv ID detected: 2401.00001
⏳ Fetching content...
✅ Fetched 44,088 characters

⏳ Generating summary...
# Paper Summary

**Source:** https://arxiv.org/abs/2401.00001
**Generated:** 17:22 UTC on 2026-02-17

---

## [2401.00001] Sector Rotation by Factor Model and Fundamental Analysis

**Authors:** Runjia Yang, Beining Shi

---

## Abstract

Sector rotation strategies have long been a cornerstone of modern portfolio management. This paper presents a novel approach to sector rotation by integrating factor model insights with fundamental analysis...

---

## Key Findings

1. Mean reversion plays a key role in dictating sectoral shifts.
2. Fundamental analysis evaluates metrics such as PE, PB, EV-to-EBITDA.
3. Models trained on fundamental indicators show predictive capabilities.

## Methodology

Develops a predictive framework based on fundamental indicators including PE, PB, EV-to-EBITDA, and Dividend Yield. Models undergo rigorous training to evaluate predictive capabilities.

---

## Implications

The findings provide a nuanced understanding of sector rotation strategies, with direct implications for asset management and portfolio construction in financial markets.

---

## Reference

- **URL:** https://arxiv.org/abs/2401.00001
- **Fetched:** 2026-02-17 17:22:45
```

### Save to File

```bash
$ paper-summarizer https://arxiv.org/abs/2401.00001 --save

🔍 URL: https://arxiv.org/abs/2401.00001
...
✅ Saved: /home/exedev/.openclaw/workspace/outputs/abs-2401.00001.md
```

## Output Format

Summaries are formatted as markdown with these sections:

```markdown
# Paper Summary

**Source:** [URL]
**Generated:** [timestamp]

---

## [Title]

**Authors:** [names]

---

## Abstract

[full abstract]

---

## Key Findings

1. [finding 1]
2. [finding 2]
...

## Methodology

[methods description]

---

## Implications

[impact and significance]

---

## Reference

- **URL:** [URL]
- **Fetched:** [timestamp]
```

## Features

- ✅ arXiv ID detection (auto-formats URL)
- ✅ Web content fetching (any URL)
- ✅ Structured markdown output
- ✅ Key findings extraction (bullet points)
- ✅ Methodology section
- ✅ Implications analysis
- ✅ Save to file option
- ✅ JSON metadata output
- ✅ Zero external dependencies (pure Python)

## Use Cases

### For Marcus (AI Research)

```bash
# Summarize AI papers
paper-summarizer https://arxiv.org/abs/2401.12345 --save

# Batch process multiple papers
for id in 2401.12345 2401.12346 2401.12347; do
  paper-summarizer $id --save
done
```

### For Galen (Biopharma Research)

```bash
# Summarize biopharma papers
paper-summarizer https://nature.com/articles/paper123 --save

# Search and summarize
paper-summarizer $(find-paper-url "CRISPR Cas9") --save
```

### For Justin (Quick Research)

```bash
# Get quick summary without reading full paper
paper-summarizer 2401.00001

# Save for later reference
paper-summarizer 2401.00001 --save --json
```

## Scheduling

Automate daily paper summarization:

```bash
# Add to crontab
crontab -e

0 9 * * * paper-summarizer $(get-daily-arxiv-id) --save

# Or use systemd timer
systemctl --user edit paper-summarizer.timer
```

## Troubleshooting

### URL Not Accessible

```bash
# Test URL fetch
curl -I https://arxiv.org/abs/2401.00001

# Check internet connection
ping arxiv.org
```

### No Content Found

```bash
# Check if content is HTML
paper-summarizer https://arxiv.org/abs/2401.00001 2>&1 | grep "Fetched"

# Verify arXiv ID format
paper-summarizer 2401.00001
```

### Parsing Issues

The parser works best with:
- Academic papers (arXiv, nature.com, science.org)
- Well-structured HTML articles
- Clear section headers (Abstract, Methods, Results)

For PDFs, convert to HTML first or use a PDF-to-text tool.

## Future Enhancements

- [ ] PDF support (direct PDF parsing)
- [ ] Better HTML parsing (remove JavaScript/CSS)
- [ ] Citation extraction
- [ ] Batch processing (multiple URLs)
- [ ] Export to different formats (JSON, CSV)
- [ ] Integration with citation managers
- [ ] Custom templates for different journals

## Limitations

- **HTML parsing quality:** Depends on website structure
- **Finding extraction:** Best with structured papers
- **PDFs:** Not supported directly (convert first)
- **JavaScript sites:** May not fetch dynamic content

## Tips

1. **Use arXiv IDs** when possible — cleaner parsing
2. **Save to file** for future reference
3. **Include JSON** for programmatic use
4. **Check output** quality varies by source
5. **Use with other tools:** combine with squad-output-digest

## License

MIT License

## Author

OpenSeneca Squad Toolset

---

**One command. Structured summary.**

For Marcus, Galen, and anyone who reads research papers.
