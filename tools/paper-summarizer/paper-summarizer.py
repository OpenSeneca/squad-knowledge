#!/usr/bin/env python3
"""
paper-summarizer — Structured summaries for papers and articles

Input: URL or arXiv ID
Output: Structured summary (title, authors, abstract, findings, methodology, implications)

Usage:
    paper-summarizer https://arxiv.org/abs/2401.00001
    paper-summarizer 2401.00001  # arXiv ID only
    paper-summarizer --url https://example.com/paper --save
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


def fetch_url(url):
    """Fetch content from URL using urllib."""
    try:
        # Set user agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; OpenSeneca-PaperSummarizer/1.0)'
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return content, None
    except Exception as e:
        return None, str(e)


def parse_arxiv_id(input_text):
    """Extract arXiv ID from input."""
    # Remove common prefixes
    cleaned = input_text.strip()
    cleaned = re.sub(r'^(https?://)?(arxiv\.org/(abs|pdf)/)?', '', cleaned)
    cleaned = cleaned.replace('.pdf', '')

    # Validate format (rough check)
    if re.match(r'^\d{4}\.\d{4,5}$', cleaned):
        return cleaned
    elif re.match(r'^\d{4}\.\d{4,5}v\d+$', cleaned):
        return cleaned.split('v')[0]
    else:
        return None


def parse_title(content):
    """Extract title from article content."""
    # Try common patterns
    patterns = [
        r'<title>(.*?)</title>',
        r'# (.*?)(?:\n|$)',
        r'Title:\s*(.*?)(?:\n|$)',
        r'title\s*=\s*{([^}]+)}',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            title = match.group(1).strip()
            # Remove HTML entities
            title = re.sub(r'&[^;]+;', '', title)
            # Remove extra whitespace
            title = re.sub(r'\s+', ' ', title)
            return title[:200]  # Limit length

    return "Unknown Title"


def parse_authors(content):
    """Extract authors from article content."""
    patterns = [
        r'Authors?:\s*([^\n]+)',
        r'author\s*=\s*{([^}]+)}',
        r'by\s+(.*?)(?:\n|Abstract)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            authors = match.group(1).strip()
            # Clean up
            authors = re.sub(r'[{}"\']', '', authors)
            authors = re.sub(r'\s+', ' ', authors)
            return authors[:300]

    return "Unknown Authors"


def parse_abstract(content):
    """Extract abstract from article content."""
    # Try to find abstract section
    abstract_match = re.search(
        r'Abstract[:\s]*(.*?)(?:\n\s*\n|\n\s*(?:Keywords|Introduction|1\.|I\.))',
        content,
        re.IGNORECASE | re.DOTALL
    )

    if abstract_match:
        abstract = abstract_match.group(1).strip()
        # Clean up
        abstract = re.sub(r'\s+', ' ', abstract)
        # Remove HTML tags
        abstract = re.sub(r'<[^>]+>', '', abstract)
        return abstract[:1500]  # Limit length

    return "No abstract found"


def extract_findings(content):
    """Extract key findings from content."""
    findings = []

    # Look for sections like "Results", "Findings", "Conclusion"
    sections = re.findall(
        r'(?:Results|Findings|Conclusion|Key\s+Takeaways)[:]?\s*(.*?)(?=\n\s*\n|\n\s*(?:\d+\.|[A-Z][a-z]+:|$))',
        content,
        re.IGNORECASE | re.DOTALL
    )

    for section in sections[:3]:  # Take up to 3 sections
        # Extract bullet points or numbered lists
        bullets = re.findall(r'[•\-\*]\s*(.*?)(?=\n|$)', section, re.IGNORECASE)
        if bullets:
            findings.extend(bullets[:5])  # Take up to 5 per section

    # If no bullets found, try to extract sentences
    if not findings:
        for section in sections[:2]:
            sentences = re.findall(r'[^.!?]+[.!?]', section)
            findings.extend(sentences[:3])

    # Clean and deduplicate
    findings = [f.strip() for f in findings if f.strip() and len(f.strip()) > 50]
    findings = list(dict.fromkeys(findings))  # Remove duplicates while preserving order

    return findings[:10]  # Return up to 10 findings


def extract_methodology(content):
    """Extract methodology from content."""
    patterns = [
        r'Methodology[:\s]*(.*?)(?=\n\s*\n|\n\s*(?:Results|Findings|Conclusion))',
        r'Methods?[:\s]*(.*?)(?=\n\s*\n|\n\s*(?:Results|Findings|Conclusion))',
        r'(?:Approach|Procedure)[:\s]*(.*?)(?=\n\s*\n|\n\s*(?:Results|Findings|Conclusion))',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            methodology = match.group(1).strip()
            # Clean up
            methodology = re.sub(r'\s+', ' ', methodology)
            methodology = re.sub(r'<[^>]+>', '', methodology)
            return methodology[:800]

    return "Methodology not found"


def extract_implications(content):
    """Extract implications from content."""
    # Look for "Implications", "Significance", "Impact" sections
    patterns = [
        r'(?:Implications?|Significance|Impact|Future\s+Work)[:\s]*(.*?)(?=\n\s*\n|\n\s*(?:\d+\.|[A-Z][a-z]+:|$))',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            implications = match.group(1).strip()
            # Clean up
            implications = re.sub(r'\s+', ' ', implications)
            implications = re.sub(r'<[^>]+>', '', implications)
            return implications[:800]

    return "Implications not specified"


def generate_summary(url, content):
    """Generate structured summary from article content."""
    title = parse_title(content)
    authors = parse_authors(content)
    abstract = parse_abstract(content)
    findings = extract_findings(content)
    methodology = extract_methodology(content)
    implications = extract_implications(content)

    summary_lines = [
        "# Paper Summary\n",
        f"**Source:** {url}\n",
        f"**Generated:** {datetime.now().strftime('%H:%M UTC on %Y-%m-%d')}\n",
        f"---\n",
        f"## {title}\n",
        f"**Authors:** {authors}\n",
        f"---\n",
        f"## Abstract\n",
        f"{abstract}\n",
        f"---\n",
    ]

    if findings:
        summary_lines.append(f"## Key Findings\n")
        for i, finding in enumerate(findings, 1):
            summary_lines.append(f"{i}. {finding}\n")
        summary_lines.append("\n")

    summary_lines.append(f"## Methodology\n")
    summary_lines.append(f"{methodology}\n")
    summary_lines.append(f"\n---\n")

    if implications and "not found" not in implications.lower():
        summary_lines.append(f"## Implications\n")
        summary_lines.append(f"{implications}\n")
        summary_lines.append(f"\n---\n")

    summary_lines.append(f"## Reference\n")
    summary_lines.append(f"- **URL:** {url}\n")
    summary_lines.append(f"- **Fetched:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    return '\n'.join(summary_lines), {
        "title": title,
        "authors": authors,
        "url": url,
        "findings_count": len(findings),
        "generated_at": datetime.now().isoformat(),
    }


def save_summary(content, url):
    """Save summary to file."""
    # Generate filename from URL
    parsed = urlparse(url)
    filename = parsed.path.replace('/', '-').strip('-')

    if not filename:
        filename = f"summary-{datetime.now().strftime('%Y%m%d-%H%M')}"

    # Ensure .md extension
    if not filename.endswith('.md'):
        filename += '.md'

    # Save to outputs/
    output_dir = Path.home() / ".openclaw/workspace/outputs"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / filename
    output_path.write_text(content)

    print(f"✅ Saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate structured summary from paper/article URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Summarize arXiv paper
  paper-summarizer https://arxiv.org/abs/2401.00001

  # Use arXiv ID only
  paper-summarizer 2401.00001

  # Summarize any URL
  paper-summarizer https://example.com/paper

  # Save to file
  paper-summarizer https://arxiv.org/abs/2401.00001 --save

Output:
  - Structured markdown with title, authors, abstract, findings, methodology, implications
  - Saves to outputs/ when --save flag used
  - Prints to stdout by default
        """
    )

    parser.add_argument(
        'url',
        help='URL or arXiv ID to summarize',
    )

    parser.add_argument(
        '--save',
        action='store_true',
        help='Save summary to outputs directory',
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output metadata as JSON',
    )

    args = parser.parse_args()

    # Check if input is arXiv ID
    arxiv_id = parse_arxiv_id(args.url)
    if arxiv_id:
        url = f"https://arxiv.org/abs/{arxiv_id}"
        print(f"🔍 ArXiv ID detected: {arxiv_id}")
    else:
        url = args.url
        print(f"🔍 URL: {url}")

    # Fetch content
    print("⏳ Fetching content...")
    content, error = fetch_url(url)

    if error:
        print(f"❌ Error fetching URL: {error}")
        sys.exit(1)

    if not content or len(content) < 100:
        print(f"❌ No content found or content too short")
        sys.exit(1)

    print(f"✅ Fetched {len(content):,} characters\n")

    # Generate summary
    print("⏳ Generating summary...")
    summary, metadata = generate_summary(url, content)

    # Print summary
    print(summary)

    # Save to file if requested
    if args.save:
        save_summary(summary, url)

    # Output JSON if requested
    if args.json:
        print(f"\n---\n")
        print(f"## Metadata (JSON)\n")
        print(f"```json\n{json.dumps(metadata, indent=2)}\n```")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Summarization interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
