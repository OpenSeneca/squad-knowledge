#!/usr/bin/env python3
"""
hash — File Hash Calculator

Calculate file hashes (MD5, SHA1, SHA256, SHA512) for verification.
"""

import sys
import argparse
import hashlib
from pathlib import Path
from typing import List, Optional, Dict


class HashTool:
    """File hash calculator."""

    def __init__(self):
        self.algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512,
        }

    def calculate_hash(self, file_path: str, algorithm: str = 'sha256',
                     chunk_size: int = 8192) -> Optional[str]:
        """Calculate file hash."""
        if algorithm not in self.algorithms:
            print(f"Error: Unknown algorithm: {algorithm}", file=sys.stderr)
            return None

        path = Path(file_path)

        if not path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            return None

        if not path.is_file():
            print(f"Error: Not a file: {file_path}", file=sys.stderr)
            return None

        hasher = self.algorithms[algorithm]()

        try:
            with open(path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)

            return hasher.hexdigest()

        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return None

    def calculate_hashes(self, file_path: str,
                      algorithms: List[str] = None) -> Dict[str, str]:
        """Calculate multiple hashes for a file."""
        if algorithms is None:
            algorithms = ['md5', 'sha1', 'sha256', 'sha512']

        hashes = {}
        for algo in algorithms:
            if algo in self.algorithms:
                hash_value = self.calculate_hash(file_path, algo)
                if hash_value:
                    hashes[algo] = hash_value

        return hashes

    def verify_hash(self, file_path: str, expected: str,
                   algorithm: str = 'sha256') -> bool:
        """Verify file hash."""
        actual = self.calculate_hash(file_path, algorithm)

        if actual is None:
            return False

        return actual.lower() == expected.lower()

    def format_size(self, size: int) -> str:
        """Format size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"


def main():
    parser = argparse.ArgumentParser(
        description='hash — File Hash Calculator'
    )

    # Input
    parser.add_argument('file', nargs='+', help='File(s) to hash')

    # Options
    parser.add_argument('--algorithm', '-a', default='sha256',
                      choices=['md5', 'sha1', 'sha256', 'sha512'],
                      help='Hash algorithm (default: sha256)')
    parser.add_argument('--all', action='store_true',
                      help='Calculate all hashes')
    parser.add_argument('--verify', '-v', metavar='HASH',
                      help='Verify file against expected hash')
    parser.add_argument('--chunk-size', type=int, default=8192,
                      help='Read chunk size in bytes (default: 8192)')
    parser.add_argument('--quiet', '-q', action='store_true',
                      help='Only show hash (no filename)')

    args = parser.parse_args()

    tool = HashTool()

    # Verify mode
    if args.verify:
        if len(args.file) > 1:
            print("Error: Verify mode only accepts one file", file=sys.stderr)
            return 1

        is_valid = tool.verify_hash(args.file[0], args.verify, args.algorithm)

        if args.quiet:
            print("OK" if is_valid else "FAIL")
        else:
            if is_valid:
                print(f"✓ {args.file[0]}: Hash matches")
            else:
                print(f"✗ {args.file[0]}: Hash mismatch")
                actual = tool.calculate_hash(args.file[0], args.algorithm)
                if actual:
                    print(f"  Expected: {args.verify}")
                    print(f"  Actual:   {actual}")

        return 0 if is_valid else 1

    # Calculate all hashes
    if args.all:
        for file_path in args.file:
            hashes = tool.calculate_hashes(file_path)
            path = Path(file_path)

            if args.quiet:
                for algo in ['md5', 'sha1', 'sha256', 'sha512']:
                    if algo in hashes:
                        print(f"{hashes[algo]}")
            else:
                size = path.stat().st_size
                print(f"{file_path} ({tool.format_size(size)})")

                for algo in ['md5', 'sha1', 'sha256', 'sha512']:
                    if algo in hashes:
                        print(f"  {algo.upper():>8}: {hashes[algo]}")

        return 0

    # Calculate single hash
    for file_path in args.file:
        hash_value = tool.calculate_hash(file_path, args.algorithm, args.chunk_size)

        if hash_value:
            if args.quiet:
                print(hash_value)
            else:
                path = Path(file_path)
                size = path.stat().st_size
                print(f"{hash_value}  {file_path} ({tool.format_size(size)})")

    return 0


if __name__ == '__main__':
    sys.exit(main())
