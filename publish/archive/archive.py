#!/usr/bin/env python3
"""
archive — Archive and Compression Tool

Compress and extract archives (zip, tar.gz, tar.bz2, tar.xz).
"""

import sys
import argparse
import tarfile
import zipfile
from pathlib import Path
from typing import List, Optional
import shutil
import os


class ArchiveTool:
    """Archive and compression tool."""

    def create_zip(self, source: str, output: str, compression: int = zipfile.ZIP_DEFLATED):
        """Create ZIP archive."""
        source_path = Path(source)
        output_path = Path(output)

        if output_path.suffix != '.zip':
            output_path = output_path.with_suffix('.zip')

        with zipfile.ZipFile(output_path, 'w', compression) as zipf:
            if source_path.is_file():
                # Single file
                zipf.write(source_path, source_path.name)
            elif source_path.is_dir():
                # Directory
                for item in source_path.rglob('*'):
                    if item.is_file():
                        arcname = item.relative_to(source_path)
                        zipf.write(item, arcname)

        return str(output_path)

    def extract_zip(self, archive: str, output: Optional[str] = None):
        """Extract ZIP archive."""
        archive_path = Path(archive)
        output_path = Path(output) if output else archive_path.parent

        with zipfile.ZipFile(archive_path, 'r') as zipf:
            zipf.extractall(output_path)

        return str(output_path)

    def create_tar(self, source: str, output: str, mode: str = 'w:gz'):
        """Create TAR archive."""
        source_path = Path(source)
        output_path = Path(output)

        # Determine extension
        if mode == 'w:gz':
            ext = '.tar.gz'
        elif mode == 'w:bz2':
            ext = '.tar.bz2'
        elif mode == 'w:xz':
            ext = '.tar.xz'
        else:
            ext = '.tar'

        if not any(output_path.suffix == e for e in ['.tar.gz', '.tar.bz2', '.tar.xz', '.tar']):
            output_path = output_path.with_suffix(ext)

        with tarfile.open(output_path, mode) as tarf:
            if source_path.is_file():
                # Single file
                tarf.add(source_path, arcname=source_path.name)
            elif source_path.is_dir():
                # Directory
                tarf.add(source_path, arcname=source_path.name)

        return str(output_path)

    def extract_tar(self, archive: str, output: Optional[str] = None):
        """Extract TAR archive."""
        archive_path = Path(archive)
        output_path = Path(output) if output else archive_path.parent

        with tarfile.open(archive_path, 'r:*') as tarf:
            tarf.extractall(output_path)

        return str(output_path)

    def list_archive(self, archive: str):
        """List contents of archive."""
        archive_path = Path(archive)

        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                for info in zipf.infolist():
                    size = info.file_size if info.file_size else 0
                    mtime = info.date_time
                    print(f"{size:>10}  {mtime[0]:04d}-{mtime[1]:02d}-{mtime[2]:02d} {mtime[3]:02d}:{mtime[4]:02d}:{mtime[5]:02d}  {info.filename}")

        elif archive_path.suffix in ['.tar', '.tar.gz', '.tar.bz2', '.tar.xz']:
            with tarfile.open(archive_path, 'r:*') as tarf:
                for member in tarf.getmembers():
                    size = member.size if member.isfile() else 0
                    mtime = member.mtime
                    from datetime import datetime
                    dt = datetime.fromtimestamp(mtime)
                    print(f"{size:>10}  {dt.strftime('%Y-%m-%d %H:%M:%S')}  {member.name}")

    def info_archive(self, archive: str):
        """Show archive info."""
        archive_path = Path(archive)
        size = archive_path.stat().st_size
        count = 0

        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                count = len(zipf.namelist())
                compressed = sum(info.file_size for info in zipf.filelist)
                uncompressed = sum(info.compress_size for info in zipf.filelist)

        elif archive_path.suffix in ['.tar', '.tar.gz', '.tar.bz2', '.tar.xz']:
            with tarfile.open(archive_path, 'r:*') as tarf:
                members = tarf.getmembers()
                count = len(members)
                compressed = sum(m.size for m in members if m.isfile())
                uncompressed = size  # Approximate

        print(f"Archive: {archive_path.name}")
        print(f"Size: {self.format_size(size)}")
        print(f"Files: {count}")
        print(f"Type: {archive_path.suffix[1:].upper()}")

    def format_size(self, size: int) -> str:
        """Format size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"


def main():
    parser = argparse.ArgumentParser(
        description='archive — Archive and Compression Tool'
    )

    # Actions
    parser.add_argument('action', choices=['create', 'extract', 'list', 'info'],
                      help='Action to perform')

    # Input
    parser.add_argument('source', help='Source file/directory or archive')

    # Options
    parser.add_argument('-o', '--output', metavar='PATH',
                      help='Output path')
    parser.add_argument('-f', '--format', choices=['zip', 'tar', 'tar.gz', 'tar.bz2', 'tar.xz'],
                      help='Archive format (default: zip)')

    args = parser.parse_args()

    tool = ArchiveTool()

    # Create archive
    if args.action == 'create':
        output = args.output or f"{Path(args.source).name}.archive"

        if args.format:
            if args.format == 'zip':
                result = tool.create_zip(args.source, output)
            elif args.format in ['tar', 'tar.gz', 'tar.bz2', 'tar.xz']:
                mode = f"w:{args.format.split('.')[-1]}" if '.' in args.format else 'w'
                result = tool.create_tar(args.source, output, mode)
        else:
            # Default to ZIP
            result = tool.create_zip(args.source, output)

        print(f"Created: {result}")

    # Extract archive
    elif args.action == 'extract':
        source_path = Path(args.source)

        if source_path.suffix == '.zip':
            result = tool.extract_zip(args.source, args.output)
        elif source_path.suffix in ['.tar', '.tar.gz', '.tar.bz2', '.tar.xz']:
            result = tool.extract_tar(args.source, args.output)
        else:
            print(f"Error: Unknown archive format: {source_path.suffix}", file=sys.stderr)
            return 1

        print(f"Extracted to: {result}")

    # List archive
    elif args.action == 'list':
        tool.list_archive(args.source)

    # Info archive
    elif args.action == 'info':
        tool.info_archive(args.source)

    return 0


if __name__ == '__main__':
    sys.exit(main())
