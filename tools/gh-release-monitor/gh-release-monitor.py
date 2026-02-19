#!/usr/bin/env python3
"""
GitHub Release Monitor CLI

Monitor GitHub repositories for new releases and generate digests.

Usage:
    gh-release-monitor --repos openai/openai-python anthropic/anthropic-sdk
    gh-release-monitor --config ~/.config/gh-release-monitor/repos.txt
    gh-release-monitor --since 2026-02-15

Author: Archimedes
Date: 2026-02-19
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Set
import subprocess


@dataclass
class Release:
    """GitHub release data."""
    repo: str
    tag_name: str
    name: str
    published_at: datetime
    html_url: str
    body: str
    author: str
    prerelease: bool
    draft: bool


class GitHubReleaseMonitor:
    """Monitor GitHub repositories for releases."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or self._get_token()
        self.cache_dir = Path.home() / '.cache' / 'gh-release-monitor'
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _get_token() -> Optional[str]:
        """Get GitHub token from gh CLI or environment."""
        # Try gh CLI
        try:
            result = subprocess.run(
                ['gh', 'auth', 'token'],
                capture_output=True,
                text=True,
                check=True
            )
            token = result.stdout.strip()
            if token:
                return token
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Try environment
        import os
        return os.environ.get('GITHUB_TOKEN')

    def get_releases(self, repo: str, limit: int = 10) -> List[Release]:
        """Get releases for a repository."""
        cache_file = self.cache_dir / f'{repo.replace("/", "_")}.json'

        # Check cache (5 minutes)
        if cache_file.exists():
            cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
            if cache_age < timedelta(minutes=5):
                try:
                    with open(cache_file, 'r') as f:
                        cached = json.load(f)
                    return [self._parse_release(r) for r in cached]
                except:
                    pass  # Fall through to fetch

        # Fetch from GitHub
        try:
            cmd = ['gh', 'api', f'repos/{repo}/releases', '--paginate']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            releases = json.loads(result.stdout)
            if not isinstance(releases, list):
                releases = []

            # Cache
            with open(cache_file, 'w') as f:
                json.dump(releases[:limit], f)

            return [self._parse_release(r) for r in releases[:limit]]

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error fetching releases for {repo}: {e.stderr}", file=sys.stderr)
            return []

    @staticmethod
    def _parse_release(data: dict) -> Release:
        """Parse release JSON into Release object."""
        published_at = datetime.fromisoformat(data['published_at'].replace('Z', '+00:00'))
        return Release(
            repo=data.get('html_url', '').split('/')[4] + '/' + data.get('html_url', '').split('/')[5],
            tag_name=data['tag_name'],
            name=data['name'] or data['tag_name'],
            published_at=published_at,
            html_url=data['html_url'],
            body=data['body'] or '',
            author=data['author']['login'],
            prerelease=data['prerelease'],
            draft=data['draft']
        )

    def filter_by_date(self, releases: List[Release], since: datetime) -> List[Release]:
        """Filter releases published after a date."""
        return [r for r in releases if r.published_at >= since]

    def filter_by_keywords(self, releases: List[Release], keywords: List[str]) -> List[Release]:
        """Filter releases by keywords in name or body."""
        if not keywords:
            return releases

        keywords_lower = [k.lower() for k in keywords]
        filtered = []

        for r in releases:
            text = f"{r.name} {r.body}".lower()
            if any(kw in text for kw in keywords_lower):
                filtered.append(r)

        return filtered

    @staticmethod
    def truncate_body(body: str, max_lines: int = 5) -> str:
        """Truncate release body to first N lines."""
        lines = body.strip().split('\n')
        return '\n'.join(lines[:max_lines])

    @staticmethod
    def extract_urls(body: str) -> List[str]:
        """Extract URLs from release body."""
        import re
        url_pattern = re.compile(r'https?://[^\s\)]+')
        return url_pattern.findall(body)


class ReleaseFormatter:
    """Format releases for output."""

    @staticmethod
    def text_format(releases: List[Release], show_body: bool = False) -> str:
        """Format as plain text."""
        if not releases:
            return "No new releases found."

        lines = []
        lines.append("=" * 70)
        lines.append("GITHUB RELEASE MONITOR")
        lines.append(f"Found {len(releases)} release(s)")
        lines.append("=" * 70)
        lines.append("")

        # Group by repo
        by_repo: Dict[str, List[Release]] = {}
        for r in releases:
            if r.repo not in by_repo:
                by_repo[r.repo] = []
            by_repo[r.repo].append(r)

        for repo, repo_releases in sorted(by_repo.items()):
            lines.append(f"## {repo}")
            lines.append("")

            for r in repo_releases:
                # Header
                badges = []
                if r.prerelease:
                    badges.append("PRE")
                if r.draft:
                    badges.append("DRAFT")

                badge_str = f" [{', '.join(badges)}]" if badges else ""
                lines.append(f"📦 {r.tag_name}{badge_str}")
                lines.append(f"   Name: {r.name}")
                lines.append(f"   Published: {r.published_at.strftime('%Y-%m-%d %H:%M UTC')}")
                lines.append(f"   By: @{r.author}")
                lines.append(f"   URL: {r.html_url}")
                lines.append("")

                # Body (truncated)
                if show_body and r.body:
                    body = GitHubReleaseMonitor.truncate_body(r.body, max_lines=10)
                    if body:
                        lines.append("   Notes:")
                        for line in body.split('\n'):
                            lines.append(f"      {line}")
                        lines.append("")

                lines.append("-" * 70)
                lines.append("")

        return "\n".join(lines)

    @staticmethod
    def json_format(releases: List[Release]) -> str:
        """Format as JSON."""
        data = []
        for r in releases:
            data.append({
                'repo': r.repo,
                'tag_name': r.tag_name,
                'name': r.name,
                'published_at': r.published_at.isoformat(),
                'html_url': r.html_url,
                'author': r.author,
                'prerelease': r.prerelease,
                'draft': r.draft,
                'body': r.body
            })
        return json.dumps(data, indent=2)

    @staticmethod
    def markdown_format(releases: List[Release], show_body: bool = False) -> str:
        """Format as Markdown."""
        if not releases:
            return "No new releases found."

        lines = []
        lines.append("# GitHub Releases")
        lines.append("")

        # Group by repo
        by_repo: Dict[str, List[Release]] = {}
        for r in releases:
            if r.repo not in by_repo:
                by_repo[r.repo] = []
            by_repo[r.repo].append(r)

        for repo, repo_releases in sorted(by_repo.items()):
            lines.append(f"## {repo}")
            lines.append("")

            for r in repo_releases:
                badges = []
                if r.prerelease:
                    badges.append("`PRE`")
                if r.draft:
                    badges.append("`DRAFT`")

                badge_str = f" {', '.join(badges)}" if badges else ""
                lines.append(f"### {r.tag_name}{badge_str}")
                lines.append("")
                lines.append(f"**Name:** {r.name}")
                lines.append(f"**Published:** {r.published_at.strftime('%Y-%m-%d %H:%M UTC')}")
                lines.append(f"**By:** @{r.author}")
                lines.append(f"**URL:** [{r.html_url}]({r.html_url})")
                lines.append("")

                # Body (truncated)
                if show_body and r.body:
                    body = GitHubReleaseMonitor.truncate_body(r.body, max_lines=15)
                    if body:
                        lines.append("**Notes:**")
                        lines.append("")
                        for line in body.split('\n'):
                            if line.strip():
                                lines.append(f"{line}")
                        lines.append("")

                lines.append("---")
                lines.append("")

        return "\n".join(lines)


def load_repos_from_file(filepath: Path) -> List[str]:
    """Load repository list from file (one per line)."""
    if not filepath.exists():
        print(f"❌ Config file not found: {filepath}")
        return []

    repos = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                repos.append(line)

    return repos


def main():
    parser = argparse.ArgumentParser(
        description='Monitor GitHub repositories for new releases',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gh-release-monitor --repos openai/openai-python anthropic/anthropic-sdk
  gh-release-monitor --config repos.txt --since 2026-02-15
  gh-release-monitor --repos langchain-ai/langchain --keywords "agent tool" --json
  gh-release-monitor --config repos.txt --markdown --show-body
        """
    )

    parser.add_argument(
        '--repos',
        nargs='+',
        help='Repository list (format: owner/repo)'
    )

    parser.add_argument(
        '--config',
        type=Path,
        help='Config file with one repo per line'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Releases per repo (default: 10)'
    )

    parser.add_argument(
        '--since',
        type=str,
        help='Only releases published after this date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--keywords',
        nargs='+',
        help='Filter by keywords in release name or body'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    parser.add_argument(
        '--markdown',
        action='store_true',
        help='Output in Markdown format'
    )

    parser.add_argument(
        '--show-body',
        action='store_true',
        help='Include release notes (truncated)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    # Validate args
    if not args.repos and not args.config:
        print("❌ Error: Specify --repos or --config")
        return 1

    # Load repos
    repos = args.repos or []
    if args.config:
        repos.extend(load_repos_from_file(args.config))

    if not repos:
        print("❌ No repositories to monitor")
        return 1

    # Parse date filter
    since_date = None
    if args.since:
        try:
            since_date = datetime.strptime(args.since, '%Y-%m-%d')
        except ValueError:
            print(f"❌ Invalid date format: {args.since}. Use YYYY-MM-DD.")
            return 1

    # Fetch releases
    monitor = GitHubReleaseMonitor()
    all_releases = []

    print(f"📡 Monitoring {len(repos)} repository(ies)...")

    for repo in repos:
        print(f"  Fetching {repo}...")
        releases = monitor.get_releases(repo, limit=args.limit)
        all_releases.extend(releases)

    if not all_releases:
        print("❌ No releases found")
        return 0

    # Filter by date
    if since_date:
        all_releases = monitor.filter_by_date(all_releases, since_date)
        print(f"  Filtered to {len(all_releases)} release(s) since {args.since}")

    # Filter by keywords
    if args.keywords:
        all_releases = monitor.filter_by_keywords(all_releases, args.keywords)
        print(f"  Filtered to {len(all_releases)} release(s) by keywords")

    if not all_releases:
        print("✅ No new releases matching criteria")
        return 0

    # Sort by date (newest first)
    all_releases.sort(key=lambda r: r.published_at, reverse=True)

    # Format output
    if args.json:
        output = ReleaseFormatter.json_format(all_releases)
    elif args.markdown:
        output = ReleaseFormatter.markdown_format(all_releases, show_body=args.show_body)
    else:
        output = ReleaseFormatter.text_format(all_releases, show_body=args.show_body)

    # Write or print
    if args.output:
        args.output.write_text(output, encoding='utf-8')
        print(f"✅ Saved: {args.output}")
    else:
        print("")
        print(output)

    return 0


if __name__ == '__main__':
    exit(main())
