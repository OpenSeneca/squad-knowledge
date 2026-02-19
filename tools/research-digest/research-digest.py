#!/usr/bin/env python3
"""
Research Digest CLI

Scans a directory of markdown research files and extracts key sections
for quick consumption by Seneca.

Usage:
    research-digest [--dir PATH] [--output PATH] [--since DATE]

Author: Archimedes
Date: 2026-02-19
"""

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class ExtractedContent:
    """Extracted content from a single research file."""
    filename: str
    title: Optional[str] = None
    tweet_draft: Optional[str] = None
    blog_angle: Optional[str] = None
    signup: Optional[str] = None
    key_insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    conclusion: Optional[str] = None
    date: Optional[str] = None

    def has_content(self) -> bool:
        """Check if any content was extracted."""
        return bool(
            self.tweet_draft
            or self.blog_angle
            or self.signup
            or self.key_insights
            or self.recommendations
            or self.conclusion
        )


class ResearchDigest:
    """Extracts key content from research markdown files."""

    # Patterns to extract
    PATTERNS = {
        'tweet_draft': re.compile(r'^##\s+Tweet Draft\s*:?\s*(.+?)\s*$', re.MULTILINE | re.IGNORECASE),
        'blog_angle': re.compile(r'^BLOG ANGLE\s*:\s*(.+?)\s*$', re.MULTILINE),
        'signup': re.compile(r'^SIGNUP\s*:\s*(.+?)\s*$', re.MULTILINE),
        'key_insights': re.compile(r'^##\s+(Key Insights|Key Learnings|Insights)\s*$\n+(.+?)(?=^##|\Z)', re.MULTILINE | re.IGNORECASE | re.DOTALL),
        'recommendations': re.compile(r'^##\s+(Recommendations|Recommendation|What To Build|Implementation Ideas)\s*$\n+(.+?)(?=^##|\Z)', re.MULTILINE | re.IGNORECASE | re.DOTALL),
        'conclusion': re.compile(r'^##\s+(Conclusion|Summary|Key Takeaways|Takeaways)\s*$\n+(.+?)(?=^##|\Z)', re.MULTILINE | re.IGNORECASE | re.DOTALL),
    }

    # Extract bullet points from a section
    BULLET_RE = re.compile(r'^[\s]*[-*•●]\s+(.+)$', re.MULTILINE)
    NUMBERED_RE = re.compile(r'^[\s]*\d+\.\s+(.+)$', re.MULTILINE)
    MARKDOWN_BULLET = re.compile(r'^[\s]*[-*]\s+\*\*(.+?)\*\*\s*[-–—]\s*(.+)$', re.MULTILINE)  # **Name** - description

    def __init__(self, directory: Path, since: Optional[datetime] = None):
        self.directory = Path(directory)
        self.since = since

    def extract_from_file(self, filepath: Path) -> Optional[ExtractedContent]:
        """Extract content from a single markdown file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Error reading {filepath.name}: {e}")
            return None

        # Extract date from filename if present (YYYY-MM-DD format)
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
        date = date_match.group(1) if date_match else None

        # Skip if filtering by date and file is too old
        if self.since and date:
            file_date = datetime.strptime(date, '%Y-%m-%d')
            if file_date < self.since:
                return None

        # Extract title (first heading)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else None

        # Extract specific patterns
        tweet_match = self.PATTERNS['tweet_draft'].search(content)
        blog_match = self.PATTERNS['blog_angle'].search(content)
        signup_match = self.PATTERNS['signup'].search(content)

        # Extract sections
        insights_match = self.PATTERNS['key_insights'].search(content, re.DOTALL)
        recommendations_match = self.PATTERNS['recommendations'].search(content, re.DOTALL)
        conclusion_match = self.PATTERNS['conclusion'].search(content, re.DOTALL)

        # Extract bullet/numbered points from sections
        key_insights = []
        if insights_match:
            section = insights_match.group(2)
            bullets = self.BULLET_RE.findall(section)
            numbered = self.NUMBERED_RE.findall(section)
            # Also look for markdown bold bullets
            md_bullets = self.MARKDOWN_BULLET.findall(section)
            for title, desc in md_bullets:
                bullets.append(f"{title}: {desc}")
            key_insights = bullets + numbered

        recommendations = []
        if recommendations_match:
            section = recommendations_match.group(2)
            bullets = self.BULLET_RE.findall(section)
            numbered = self.NUMBERED_RE.findall(section)
            md_bullets = self.MARKDOWN_BULLET.findall(section)
            for title, desc in md_bullets:
                bullets.append(f"{title}: {desc}")
            recommendations = bullets + numbered

        conclusion = conclusion_match.group(2).strip() if conclusion_match else None

        return ExtractedContent(
            filename=filepath.name,
            title=title,
            tweet_draft=tweet_match.group(1).strip() if tweet_match else None,
            blog_angle=blog_match.group(1).strip() if blog_match else None,
            signup=signup_match.group(1).strip() if signup_match else None,
            key_insights=key_insights[:10],  # Limit to 10 insights per file
            recommendations=recommendations[:10],
            conclusion=conclusion,
            date=date
        )

    def scan_directory(self) -> List[ExtractedContent]:
        """Scan all markdown files in directory."""
        results = []

        if not self.directory.exists():
            print(f"❌ Directory not found: {self.directory}")
            return results

        for filepath in sorted(self.directory.glob('*.md')):
            # Skip archive and seed files
            if 'archive' in filepath.parts or 'seed-' in filepath.name:
                continue

            extracted = self.extract_from_file(filepath)
            if extracted and extracted.has_content():
                results.append(extracted)

        return results


class DigestFormatter:
    """Formats extracted content for output."""

    @staticmethod
    def text_format(results: List[ExtractedContent]) -> str:
        """Format as plain text."""
        if not results:
            return "No content extracted from research files."

        lines = []
        lines.append("=" * 70)
        lines.append("RESEARCH DIGEST")
        lines.append(f"Found {len(results)} files with extractable content")
        lines.append("=" * 70)
        lines.append("")

        for result in results:
            # Header
            if result.title:
                lines.append(f"📄 {result.title}")
            else:
                lines.append(f"📄 {result.filename}")

            if result.date:
                lines.append(f"   Date: {result.date}")
            lines.append("")

            # Tweet Draft (high priority)
            if result.tweet_draft:
                lines.append(f"🐦 Tweet Draft:")
                lines.append(f"   {result.tweet_draft}")
                lines.append("")

            # Blog Angle (high priority)
            if result.blog_angle:
                lines.append(f"📝 Blog Angle:")
                lines.append(f"   {result.blog_angle}")
                lines.append("")

            # Signup (high priority)
            if result.signup:
                lines.append(f"✍️  Signup:")
                lines.append(f"   {result.signup}")
                lines.append("")

            # Key Insights
            if result.key_insights:
                lines.append("💡 Key Insights:")
                for insight in result.key_insights:
                    lines.append(f"   • {insight}")
                lines.append("")

            # Recommendations
            if result.recommendations:
                lines.append("🎯 Recommendations:")
                for rec in result.recommendations:
                    lines.append(f"   • {rec}")
                lines.append("")

            # Conclusion
            if result.conclusion:
                # Clean up conclusion - remove extra whitespace
                conclusion = re.sub(r'\n+', ' ', result.conclusion)
                conclusion = re.sub(r'\s+', ' ', conclusion).strip()
                # Remove bullet markers if present
                conclusion = re.sub(r'^[\s]*[-*•]\s*', '', conclusion)
                # Limit to first 300 chars
                if len(conclusion) > 300:
                    conclusion = conclusion[:297] + "..."
                if conclusion:
                    lines.append(f"📌 {conclusion}")
                    lines.append("")

            lines.append("-" * 70)
            lines.append("")

        # Summary stats
        tweet_count = sum(1 for r in results if r.tweet_draft)
        blog_count = sum(1 for r in results if r.blog_angle)
        insight_count = sum(len(r.key_insights) for r in results)

        lines.append("📊 Summary:")
        lines.append(f"   Tweet drafts: {tweet_count}")
        lines.append(f"   Blog angles: {blog_count}")
        lines.append(f"   Total insights: {insight_count}")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def json_format(results: List[ExtractedContent]) -> str:
        """Format as JSON."""
        data = []
        for result in results:
            data.append({
                'filename': result.filename,
                'title': result.title,
                'date': result.date,
                'tweet_draft': result.tweet_draft,
                'blog_angle': result.blog_angle,
                'signup': result.signup,
                'key_insights': result.key_insights,
                'recommendations': result.recommendations,
                'conclusion': result.conclusion
            })
        return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Extract key content from research markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  research-digest                          # Scan default directory
  research-digest --dir ~/research        # Scan specific directory
  research-digest --since 2026-02-15       # Only recent files
  research-digest --output digest.md       # Save to file
  research-digest --json                   # JSON output
        """
    )

    parser.add_argument(
        '--dir',
        type=Path,
        default=Path.home() / '.openclaw' / 'learnings',
        help='Directory containing markdown research files (default: ~/.openclaw/learnings)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--since',
        type=str,
        help='Only process files from this date onward (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    args = parser.parse_args()

    # Parse date filter
    since_date = None
    if args.since:
        try:
            since_date = datetime.strptime(args.since, '%Y-%m-%d')
        except ValueError:
            print(f"❌ Invalid date format: {args.since}. Use YYYY-MM-DD.")
            return 1

    # Extract content
    digest = ResearchDigest(args.dir, since_date)
    results = digest.scan_directory()

    # Format output
    if args.json:
        output = DigestFormatter.json_format(results)
    else:
        output = DigestFormatter.text_format(results)

    # Write or print
    if args.output:
        args.output.write_text(output, encoding='utf-8')
        print(f"✓ Digest written to: {args.output}")
    else:
        print(output)

    return 0


if __name__ == '__main__':
    exit(main())
