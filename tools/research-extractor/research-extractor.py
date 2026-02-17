#!/usr/bin/env python3
"""
research-extractor — Extract tweet drafts, blog angles, signup links from research

Scans Marcus/Galen outputs and extracts:
- ## Tweet Draft lines
- BLOG ANGLE: lines
- SIGNUP: lines

Output: Single markdown file Seneca can scan for content to post

Usage:
    research-extractor
    research-extractor --days 3
    research-extractor --output content-extract.md
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def scan_outputs(days=7):
    """Scan agent outputs for tweet drafts, blog angles, signup links."""
    workspace = Path.home() / ".openclaw/workspace"
    outputs_dir = workspace / "outputs"

    # Find recent output files
    if not outputs_dir.exists():
        print(f"❌ Outputs directory not found: {outputs_dir}")
        return [], [], []

    # Get files modified in last N days
    cutoff = datetime.now() - timedelta(days=days)
    recent_files = []

    for f in outputs_dir.glob("*.md"):
        if f.stat().st_mtime > cutoff.timestamp():
            recent_files.append(f)

    if not recent_files:
        print(f"⚠️  No output files found in last {days} days")
        return [], [], []

    print(f"🔍 Scanning {len(recent_files)} recent files...")

    tweet_drafts = []
    blog_angles = []
    signup_links = []

    # Scan each file
    for f in recent_files:
        try:
            with open(f) as file:
                content = file.read()

            # Extract tweet drafts
            tweet_matches = re.findall(
                r'##\s*Tweet\s+Draft[:\s]*(.*?)(?=\n|$|##)',
                content,
                re.IGNORECASE
            )
            for tweet in tweet_matches:
                tweet = tweet.strip()
                if len(tweet) > 10:
                    tweet_drafts.append({
                        "source": f.name,
                        "date": datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d'),
                        "content": tweet
                    })

            # Extract blog angles
            blog_matches = re.findall(
                r'BLOG\s+ANGLE[:\s]*(.*?)(?=\n|$|##)',
                content,
                re.IGNORECASE
            )
            for angle in blog_matches:
                angle = angle.strip()
                if len(angle) > 10:
                    blog_angles.append({
                        "source": f.name,
                        "date": datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d'),
                        "content": angle
                    })

            # Extract signup links
            signup_matches = re.findall(
                r'SIGNUP[:\s]*(.*?)(?=\n|$|##)',
                content,
                re.IGNORECASE
            )
            for signup in signup_matches:
                signup = signup.strip()
                if len(signup) > 5:
                    signup_links.append({
                        "source": f.name,
                        "date": datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d'),
                        "content": signup
                    })

        except Exception as e:
            print(f"⚠️  Error reading {f.name}: {e}")

    return tweet_drafts, blog_angles, signup_links


def scan_learnings(agent_names=None, days=7):
    """Scan agent learnings for content metadata."""
    learnings_dir = Path.home() / ".openclaw/learnings"

    if not learnings_dir.exists():
        return [], [], []

    # Get files modified in last N days
    cutoff = datetime.now() - timedelta(days=days)
    recent_files = []

    for f in learnings_dir.glob("*.md"):
        if f.stat().st_mtime > cutoff.timestamp():
            # Filter by agent if specified
            if agent_names:
                if not any(agent.lower() in f.name.lower() for agent in agent_names):
                    continue
            recent_files.append(f)

    if not recent_files:
        return [], [], []

    print(f"🔍 Scanning {len(recent_files)} learning files...")

    tweet_drafts = []
    blog_angles = []
    signup_links = []

    # Scan each file
    for f in recent_files:
        try:
            with open(f) as file:
                content = file.read()

            # Extract tweet drafts
            tweet_matches = re.findall(
                r'##\s*Tweet\s+Draft[:\s]*(.*?)(?=\n|$|##)',
                content,
                re.IGNORECASE
            )
            for tweet in tweet_matches:
                tweet = tweet.strip()
                if len(tweet) > 10:
                    tweet_drafts.append({
                        "source": f.name,
                        "date": datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d'),
                        "content": tweet
                    })

            # Extract blog angles
            blog_matches = re.findall(
                r'BLOG\s+ANGLE[:\s]*(.*?)(?=\n|$|##)',
                content,
                re.IGNORECASE
            )
            for angle in blog_matches:
                angle = angle.strip()
                if len(angle) > 10:
                    blog_angles.append({
                        "source": f.name,
                        "date": datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d'),
                        "content": angle
                    })

            # Extract signup links
            signup_matches = re.findall(
                r'SIGNUP[:\s]*(.*?)(?=\n|$|##)',
                content,
                re.IGNORECASE
            )
            for signup in signup_matches:
                signup = signup.strip()
                if len(signup) > 5:
                    signup_links.append({
                        "source": f.name,
                        "date": datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d'),
                        "content": signup
                    })

        except Exception as e:
            print(f"⚠️  Error reading {f.name}: {e}")

    return tweet_drafts, blog_angles, signup_links


def generate_extract(tweet_drafts, blog_angles, signup_links, days):
    """Generate content extract markdown."""
    lines = [
        "# Research Content Extract",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Scan Period:** Last {days} days",
        f"---",
        f"",
    ]

    # Tweet drafts
    lines.append(f"## Tweet Drafts ({len(tweet_drafts)})")
    lines.append(f"")

    if tweet_drafts:
        for i, tweet in enumerate(tweet_drafts, 1):
            lines.append(f"### Draft {i}")
            lines.append(f"**Source:** {tweet['source']}")
            lines.append(f"**Date:** {tweet['date']}")
            lines.append(f"")
            lines.append(f"{tweet['content']}")
            lines.append(f"")
    else:
        lines.append(f"No tweet drafts found.")
        lines.append(f"")

    # Blog angles
    lines.append(f"---")
    lines.append(f"## Blog Angles ({len(blog_angles)})")
    lines.append(f"")

    if blog_angles:
        for i, angle in enumerate(blog_angles, 1):
            lines.append(f"### Angle {i}")
            lines.append(f"**Source:** {angle['source']}")
            lines.append(f"**Date:** {angle['date']}")
            lines.append(f"")
            lines.append(f"{angle['content']}")
            lines.append(f"")
    else:
        lines.append(f"No blog angles found.")
        lines.append(f"")

    # Signup links
    lines.append(f"---")
    lines.append(f"## Signup Links ({len(signup_links)})")
    lines.append(f"")

    if signup_links:
        for i, signup in enumerate(signup_links, 1):
            lines.append(f"### Link {i}")
            lines.append(f"**Source:** {signup['source']}")
            lines.append(f"**Date:** {signup['date']}")
            lines.append(f"")
            lines.append(f"{signup['content']}")
            lines.append(f"")
    else:
        lines.append(f"No signup links found.")
        lines.append(f"")

    # Summary
    lines.append(f"---")
    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"- **Tweet Drafts:** {len(tweet_drafts)}")
    lines.append(f"- **Blog Angles:** {len(blog_angles)}")
    lines.append(f"- **Signup Links:** {len(signup_links)}")
    lines.append(f"- **Total:** {len(tweet_drafts) + len(blog_angles) + len(signup_links)} items")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"*Generated by research-extractor for Seneca*")

    return '\n'.join(lines)


def save_extract(content, output_path=None):
    """Save extract to file."""
    if output_path is None:
        # Generate default filename
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        output_path = Path.home() / ".openclaw/workspace/outputs" / f"content-extract-{timestamp}.md"

    output_path = Path(output_path).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(content)

    print(f"✅ Saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Extract tweet drafts, blog angles, signup links from research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan all outputs from last 7 days
  research-extractor

  # Scan last 3 days
  research-extractor --days 3

  # Save to specific file
  research-extractor --output content-extract.md

  # Scan learnings from specific agents
  research-extractor --agents marcus galen

  # Combine outputs and learnings
  research-extractor --scan both

Output:
  - Tweet drafts (## Tweet Draft)
  - Blog angles (BLOG ANGLE:)
  - Signup links (SIGNUP:)
  - Single markdown file for Seneca to scan

What It Scans:
- Agent outputs (~/workspace/outputs/)
- Agent learnings (~/learnings/)
- Files modified in last N days
        """
    )

    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to scan (default: 7)',
    )

    parser.add_argument(
        '--scan',
        choices=['outputs', 'learnings', 'both'],
        default='both',
        help='What to scan: outputs, learnings, or both (default: both)',
    )

    parser.add_argument(
        '--agents',
        nargs='+',
        help='Agent names to scan learnings from (e.g., marcus galen)',
    )

    parser.add_argument(
        '--output',
        help='Output file path (default: outputs/content-extract-TIMESTAMP.md)',
    )

    args = parser.parse_args()

    # Scan outputs
    tweet_drafts = []
    blog_angles = []
    signup_links = []

    if args.scan in ['outputs', 'both']:
        print("📂 Scanning outputs...")
        t, b, s = scan_outputs(days=args.days)
        tweet_drafts.extend(t)
        blog_angles.extend(b)
        signup_links.extend(s)

    # Scan learnings
    if args.scan in ['learnings', 'both']:
        print("📂 Scanning learnings...")
        t, b, s = scan_learnings(agent_names=args.agents, days=args.days)
        tweet_drafts.extend(t)
        blog_angles.extend(b)
        signup_links.extend(s)

    # Deduplicate
    tweet_drafts = list({f['source'] + f['content']: f for f in tweet_drafts}.values())
    blog_angles = list({f['source'] + f['content']: f for f in blog_angles}.values())
    signup_links = list({f['source'] + f['content']: f for f in signup_links}.values())

    # Generate extract
    print(f"\n📊 Generating content extract...")
    extract = generate_extract(tweet_drafts, blog_angles, signup_links, args.days)

    # Print summary
    print(f"\n✅ Extracted:")
    print(f"   - {len(tweet_drafts)} tweet draft(s)")
    print(f"   - {len(blog_angles)} blog angle(s)")
    print(f"   - {len(signup_links)} signup link(s)")
    print(f"   - Total: {len(tweet_drafts) + len(blog_angles) + len(signup_links)} items")

    # Save to file
    print(f"\n💾 Saving to file...")
    save_path = save_extract(extract, args.output)

    # Print preview
    print(f"\n📄 Preview (first 500 chars):")
    print("-" * 60)
    print(extract[:500])
    print("-" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Extraction interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
