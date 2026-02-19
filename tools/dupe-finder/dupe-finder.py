#!/usr/bin/env python3
"""
Duplicate File Finder CLI

Find duplicate files using hash comparison. Report by size (biggest savings first).

Usage:
    dupe-finder ~/workspace/outputs/
    dupe-finder --dirs ~/workspace/outputs/ ~/.openclaw/learnings/ --min-size 1MB
    dupe-finder --archive ~/workspace/dupe-archive/

Author: Archimedes
Date: 2026-02-19
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


@dataclass
class DuplicateGroup:
    """A group of duplicate files."""
    hash: str
    files: List[Path]
    size: int

    @property
    def savings(self) -> int:
        """Bytes saved if duplicates removed (all but first)."""
        return (len(self.files) - 1) * self.size


class DupeFinder:
    """Find duplicate files by hash."""

    def __init__(self, min_size: int = 0):
        self.min_size = min_size
        self.cache_dir = Path.home() / '.cache' / 'dupe-finder'
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def file_hash(filepath: Path) -> str:
        """Calculate SHA256 hash of file."""
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(8192), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (OSError, IOError):
            return None

    @staticmethod
    def format_size(bytes_size: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"

    def scan_directory(self, directory: Path) -> Dict[str, List[Path]]:
        """Scan directory for files, grouped by hash."""
        hash_map = defaultdict(list)
        files_scanned = 0
        bytes_scanned = 0

        print(f"  Scanning {directory}...")

        for root, dirs, files in os.walk(directory):
            # Skip cache and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

            for filename in files:
                filepath = Path(root) / filename

                # Skip directories
                if not filepath.is_file():
                    continue

                # Check minimum size
                file_size = filepath.stat().st_size
                if file_size < self.min_size:
                    continue

                files_scanned += 1
                bytes_scanned += file_size

                # Calculate hash
                file_hash = self.file_hash(filepath)
                if file_hash:
                    hash_map[file_hash].append(filepath)

        print(f"  Scanned {files_scanned} files ({self.format_size(bytes_scanned)})")
        return dict(hash_map)

    def find_duplicates(self, directories: List[Path]) -> List[DuplicateGroup]:
        """Find all duplicate files across directories."""
        all_hashes = defaultdict(list)

        # Scan all directories
        for directory in directories:
            hash_map = self.scan_directory(directory)
            for h, files in hash_map.items():
                all_hashes[h].extend(files)

        # Filter to only duplicates (2+ files with same hash)
        duplicate_groups = []
        for h, files in all_hashes.items():
            if len(files) >= 2:
                size = files[0].stat().st_size
                duplicate_groups.append(DuplicateGroup(
                    hash=h[:16],  # Short hash for display
                    files=files,
                    size=size
                ))

        # Sort by savings (largest first)
        duplicate_groups.sort(key=lambda g: g.savings, reverse=True)

        return duplicate_groups


class DupeFormatter:
    """Format duplicate file results."""

    @staticmethod
    def text_format(groups: List[DuplicateGroup]) -> str:
        """Format as plain text."""
        if not groups:
            return "No duplicate files found."

        lines = []
        total_duplicates = sum(len(g.files) - 1 for g in groups)
        total_savings = sum(g.savings for g in groups)

        lines.append("=" * 70)
        lines.append("DUPLICATE FILE FINDER")
        lines.append(f"Found {len(groups)} duplicate group(s), {total_duplicates} duplicate file(s)")
        lines.append(f"Potential disk savings: {DupeFinder.format_size(total_savings)}")
        lines.append("=" * 70)
        lines.append("")

        for i, group in enumerate(groups, 1):
            # Header
            lines.append(f"{i}. Hash: {group.hash}")
            lines.append(f"   Size: {DupeFinder.format_size(group.size)}")
            lines.append(f"   Duplicates: {len(group.files)}")
            lines.append(f"   Savings: {DupeFinder.format_size(group.savings)}")
            lines.append("")

            # Files
            for j, filepath in enumerate(group.files, 1):
                marker = "⭐ " if j == 1 else "   "
                lines.append(f"   {marker}{j}. {filepath}")
            lines.append("")

            lines.append("-" * 70)
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def json_format(groups: List[DuplicateGroup]) -> str:
        """Format as JSON."""
        data = []
        for g in groups:
            data.append({
                'hash': g.hash,
                'size': g.size,
                'savings': g.savings,
                'file_count': len(g.files),
                'files': [str(f) for f in g.files]
            })
        return json.dumps(data, indent=2)

    @staticmethod
    def markdown_format(groups: List[DuplicateGroup]) -> str:
        """Format as Markdown."""
        if not groups:
            return "No duplicate files found."

        lines = []
        total_duplicates = sum(len(g.files) - 1 for g in groups)
        total_savings = sum(g.savings for g in groups)

        lines.append("# Duplicate Files")
        lines.append("")
        lines.append(f"**Found:** {len(groups)} duplicate group(s), {total_duplicates} duplicate file(s)")
        lines.append(f"**Potential savings:** {DupeFinder.format_size(total_savings)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for i, group in enumerate(groups, 1):
            lines.append(f"## {i}. Size: {DupeFinder.format_size(group.size)}")
            lines.append("")
            lines.append(f"- **Hash:** `{group.hash}`")
            lines.append(f"- **Duplicates:** {len(group.files)}")
            lines.append(f"- **Savings:** {DupeFinder.format_size(group.savings)}")
            lines.append("")
            lines.append("Files:")
            lines.append("")

            for j, filepath in enumerate(group.files, 1):
                star = "⭐ " if j == 1 else "   "
                lines.append(f"{star}{j}. `{filepath}`")

            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)


class DupeCleaner:
    """Handle duplicate file cleanup."""

    @staticmethod
    def archive_duplicates(groups: List[DuplicateGroup], archive_dir: Path, dry_run: bool = True):
        """Move duplicates to archive directory (keep first file)."""
        archive_dir.mkdir(parents=True, exist_ok=True)

        moved = 0
        saved = 0

        for group in groups:
            # Keep first file, archive rest
            for filepath in group.files[1:]:
                dest = archive_dir / filepath.name

                # Handle name conflicts
                counter = 1
                while dest.exists():
                    stem = filepath.stem
                    suffix = filepath.suffix
                    dest = archive_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                if dry_run:
                    print(f"  Would move: {filepath} → {dest}")
                else:
                    shutil.move(str(filepath), str(dest))
                    print(f"  Moved: {filepath}")

                moved += 1
                saved += group.size

        return moved, saved

    @staticmethod
    def delete_duplicates(groups: List[DuplicateGroup], dry_run: bool = True):
        """Delete duplicate files (keep first file)."""
        deleted = 0
        saved = 0

        for group in groups:
            # Keep first file, delete rest
            for filepath in group.files[1:]:
                if dry_run:
                    print(f"  Would delete: {filepath}")
                else:
                    filepath.unlink()
                    print(f"  Deleted: {filepath}")

                deleted += 1
                saved += group.size

        return deleted, saved


def parse_size(size_str: str) -> int:
    """Parse size string (1MB, 500KB, etc.) to bytes."""
    if not size_str:
        return 0

    size_str = size_str.upper().strip()
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 * 1024,
        'GB': 1024 * 1024 * 1024,
        'TB': 1024 * 1024 * 1024 * 1024
    }

    for suffix in sorted(multipliers.keys(), key=len, reverse=True):
        if size_str.endswith(suffix):
            num_str = size_str[:-len(suffix)].strip()
            try:
                num = float(num_str)
                return int(num * multipliers[suffix])
            except ValueError:
                continue

    # Assume bytes if no suffix
    try:
        return int(float(size_str))
    except ValueError:
        raise ValueError(f"Invalid size format: {size_str}")


def main():
    parser = argparse.ArgumentParser(
        description='Find duplicate files using hash comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dupe-finder ~/workspace/outputs/
  dupe-finder --dirs ~/workspace/outputs/ ~/.openclaw/learnings/ --min-size 1MB
  dupe-finder --archive ~/workspace/dupe-archive/ --delete
  dupe-finder --dirs . --json --min-size 100KB
        """
    )

    parser.add_argument(
        'directories',
        nargs='*',
        type=Path,
        help='Directories to scan (default: current dir)'
    )

    parser.add_argument(
        '--dirs',
        nargs='+',
        type=Path,
        help='Directory list (alternative to positional args)'
    )

    parser.add_argument(
        '--min-size',
        type=str,
        default='0B',
        help='Minimum file size to consider (default: 0B, examples: 1KB, 1MB, 100KB)'
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
        '--archive',
        type=Path,
        help='Move duplicates to archive directory instead of deleting'
    )

    parser.add_argument(
        '--delete',
        action='store_true',
        help='Delete duplicate files (dangerous! keeps first file)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Actually delete/archive (no dry run)'
    )

    args = parser.parse_args()

    # Get directories
    dirs = args.directories or args.dirs or [Path.cwd()]
    dirs = [d.expanduser() for d in dirs]

    # Validate directories
    for d in dirs:
        if not d.exists():
            print(f"❌ Directory not found: {d}")
            return 1

    # Parse minimum size
    try:
        min_size = parse_size(args.min_size)
    except ValueError:
        print(f"❌ Invalid size format: {args.min_size}. Use 1KB, 1MB, etc.")
        return 1

    # Scan for duplicates
    finder = DupeFinder(min_size=min_size)
    print(f"📡 Scanning {len(dirs)} director(ies)...")
    print(f"   Minimum size: {DupeFinder.format_size(min_size)}")
    print("")

    duplicate_groups = finder.find_duplicates(dirs)

    if not duplicate_groups:
        print("✅ No duplicate files found")
        return 0

    total_duplicates = sum(len(g.files) - 1 for g in duplicate_groups)
    total_savings = sum(g.savings for g in duplicate_groups)

    print(f"✅ Found {len(duplicate_groups)} duplicate group(s), {total_duplicates} duplicate file(s)")
    print(f"   Potential savings: {DupeFinder.format_size(total_savings)}")
    print("")

    # Format output
    if args.json:
        output = DupeFormatter.json_format(duplicate_groups)
    elif args.markdown:
        output = DupeFormatter.markdown_format(duplicate_groups)
    else:
        output = DupeFormatter.text_format(duplicate_groups)

    print("")

    # Archive or delete?
    if args.archive or args.delete:
        if not args.force:
            print("⚠️  DRY RUN MODE - No files will be moved/deleted.")
            print("   Use --force to actually execute.")
            print("")

        if args.archive:
            print(f"📦 Archiving duplicates to: {args.archive}")
            moved, saved = DupeCleaner.archive_duplicates(
                duplicate_groups, args.archive, dry_run=not args.force
            )

            if not args.force:
                print("")
                print(f"   Would move: {moved} file(s)")
                print(f"   Would save: {DupeFinder.format_size(saved)}")
            else:
                print(f"✅ Moved {moved} file(s), saved {DupeFinder.format_size(saved)}")

        elif args.delete:
            print("🗑️  Deleting duplicates...")
            deleted, saved = DupeCleaner.delete_duplicates(
                duplicate_groups, dry_run=not args.force
            )

            if not args.force:
                print("")
                print(f"   Would delete: {deleted} file(s)")
                print(f"   Would save: {DupeFinder.format_size(saved)}")
            else:
                print(f"✅ Deleted {deleted} file(s), saved {DupeFinder.format_size(saved)}")

    else:
        # Just show results
        print(output)

    return 0


if __name__ == '__main__':
    exit(main())
