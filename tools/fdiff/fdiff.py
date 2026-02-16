#!/usr/bin/env python3
"""
diff — File Comparison Tool

Compare files and directories with clear, colorized output.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Optional
import difflib


class FileDiffer:
    """File comparison tool."""

    def __init__(self, context_lines: int = 3):
        self.context_lines = context_lines
        self.colors = {
            'add': '\033[32m',    # Green
            'remove': '\033[31m', # Red
            'header': '\033[36m', # Cyan
            'line_num': '\033[90m', # Gray
            'reset': '\033[0m',
        }

    def read_file(self, filepath: str) -> List[str]:
        """Read file into lines."""
        try:
            with open(filepath, 'r', errors='ignore') as f:
                return f.readlines()
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            return []

    def compare_files(self, file1: str, file2: str,
                     unified: bool = True, side_by_side: bool = False,
                     color: bool = True) -> str:
        """Compare two files."""
        lines1 = self.read_file(file1)
        lines2 = self.read_file(file2)

        if not lines1 or not lines2:
            return ""

        if unified:
            return self._unified_diff(file1, file2, lines1, lines2, color)
        elif side_by_side:
            return self._side_by_side_diff(file1, file2, lines1, lines2, color)
        else:
            return self._context_diff(file1, file2, lines1, lines2, color)

    def _unified_diff(self, file1: str, file2: str,
                     lines1: List[str], lines2: List[str],
                     color: bool) -> str:
        """Unified diff format."""
        diff = difflib.unified_diff(
            lines1, lines2,
            fromfile=file1, tofile=file2,
            n=self.context_lines
        )

        output = []
        for line in diff:
            if not color:
                output.append(line.rstrip('\n'))
                continue

            if line.startswith('+++') or line.startswith('---'):
                # Header
                colored = f"{self.colors['header']}{line.rstrip()}{self.colors['reset']}"
                output.append(colored)
            elif line.startswith('+'):
                # Added line
                colored = f"{self.colors['add']}{line.rstrip()}{self.colors['reset']}"
                output.append(colored)
            elif line.startswith('-'):
                # Removed line
                colored = f"{self.colors['remove']}{line.rstrip()}{self.colors['reset']}"
                output.append(colored)
            elif line.startswith('@@'):
                # Hunk header
                colored = f"{self.colors['line_num']}{line.rstrip()}{self.colors['reset']}"
                output.append(colored)
            else:
                # Context line
                output.append(line.rstrip('\n'))

        return '\n'.join(output)

    def _context_diff(self, file1: str, file2: str,
                      lines1: List[str], lines2: List[str],
                      color: bool) -> str:
        """Context diff format."""
        diff = difflib.context_diff(
            lines1, lines2,
            fromfile=file1, tofile=file2,
            n=self.context_lines
        )

        output = []
        for line in diff:
            if not color:
                output.append(line.rstrip('\n'))
                continue

            if line.startswith('***') or line.startswith('---'):
                # Header
                colored = f"{self.colors['header']}{line.rstrip()}{self.colors['reset']}"
                output.append(colored)
            elif line.startswith('+'):
                # Added line
                colored = f"{self.colors['add']}{line.rstrip()}{self.colors['reset']}"
                output.append(colored)
            elif line.startswith('-'):
                # Removed line
                colored = f"{self.colors['remove']}{line.rstrip()}{self.colors['reset']}"
                output.append(colored)
            elif line.startswith('!'):
                # Changed line
                colored = f"{self.colors['line_num']}{line.rstrip()}{self.colors['reset']}"
                output.append(colored)
            else:
                # Context line
                output.append(line.rstrip('\n'))

        return '\n'.join(output)

    def _side_by_side_diff(self, file1: str, file2: str,
                            lines1: List[str], lines2: List[str],
                            color: bool) -> str:
        """Side-by-side diff format."""
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        output = []

        # Add header
        output.append(f"{file1:<50} {file2:<50}")
        output.append("-" * 100)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                # No changes
                for i in range(max(len(lines1), len(lines2))):
                    line1 = lines1[i].rstrip() if i < len(lines1) else ""
                    line2 = lines2[i].rstrip() if i < len(lines2) else ""

                    if not color:
                        output.append(f"{line1:<50} {line2:<50}")
                    else:
                        output.append(f"{line1:<50} {line2:<50}")

            elif tag == 'replace':
                # Replaced lines
                for i in range(i1, i2):
                    line1 = lines1[i].rstrip()
                    if color:
                        line1 = f"{self.colors['remove']}{line1}{self.colors['reset']}"
                    output.append(f"{line1:<50} {'':<50}")

                for j in range(j1, j2):
                    line2 = lines2[j].rstrip()
                    if color:
                        line2 = f"{self.colors['add']}{line2}{self.colors['reset']}"
                    output.append(f"{'':<50} {line2:<50}")

            elif tag == 'delete':
                # Deleted lines
                for i in range(i1, i2):
                    line1 = lines1[i].rstrip()
                    if color:
                        line1 = f"{self.colors['remove']}{line1}{self.colors['reset']}"
                    output.append(f"{line1:<50} {'':<50}")

            elif tag == 'insert':
                # Inserted lines
                for j in range(j1, j2):
                    line2 = lines2[j].rstrip()
                    if color:
                        line2 = f"{self.colors['add']}{line2}{self.colors['reset']}"
                    output.append(f"{'':<50} {line2:<50}")

        return '\n'.join(output)

    def compare_directories(self, dir1: str, dir2: str,
                          recursive: bool = False) -> List[Tuple[str, str, str]]:
        """Compare directories."""
        if recursive:
            files1 = sorted(Path(dir1).rglob('*'))
            files2 = sorted(Path(dir2).rglob('*'))
        else:
            files1 = sorted(Path(dir1).glob('*'))
            files2 = sorted(Path(dir2).glob('*'))

        # Filter to files only
        files1 = [f for f in files1 if f.is_file()]
        files2 = [f for f in files2 if f.is_file()]

        # Get relative paths
        files1_rel = {f.relative_to(dir1): f for f in files1}
        files2_rel = {f.relative_to(dir2): f for f in files2}

        # Compare
        results = []

        # Files in both
        common = set(files1_rel.keys()) & set(files2_rel.keys())
        for rel_path in common:
            file1 = files1_rel[rel_path]
            file2 = files2_rel[rel_path]

            # Compare content
            lines1 = self.read_file(str(file1))
            lines2 = self.read_file(str(file2))

            if lines1 != lines2:
                results.append(('changed', str(file1), str(file2)))

        # Files only in dir1
        only_in_1 = set(files1_rel.keys()) - set(files2_rel.keys())
        for rel_path in only_in_1:
            results.append(('only_in_1', str(files1_rel[rel_path]), None))

        # Files only in dir2
        only_in_2 = set(files2_rel.keys()) - set(files1_rel.keys())
        for rel_path in only_in_2:
            results.append(('only_in_2', None, str(files2_rel[rel_path])))

        return results

    def compare_strings(self, text1: str, text2: str) -> str:
        """Compare two strings."""
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)

        return self._unified_diff('string1', 'string2', lines1, lines2, color=False)


def main():
    parser = argparse.ArgumentParser(
        description='diff — File Comparison Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  diff file1.txt file2.txt
  diff file1.txt file2.txt --context 5
  diff file1.txt file2.txt --side-by-side
  diff dir1/ dir2/ --compare-dirs
  diff dir1/ dir2/ --compare-dirs --recursive
  diff --string "Hello World" "Hello Universe"

Common Use Cases:
  - Compare configuration files
  - Compare code changes
  - Compare test outputs
  - Compare directories
  - Compare strings
        """
    )

    # File comparison
    parser.add_argument('file1', nargs='?', help='First file or directory')
    parser.add_argument('file2', nargs='?', help='Second file or directory')

    # String comparison
    parser.add_argument('--string', nargs=2, metavar=('STR1', 'STR2'),
                      help='Compare two strings')

    # Options
    parser.add_argument('-u', '--unified', action='store_true', default=True,
                      help='Unified diff format (default)')
    parser.add_argument('-c', '--context', action='store_true',
                      help='Context diff format')
    parser.add_argument('-s', '--side-by-side', action='store_true',
                      help='Side-by-side diff format')
    parser.add_argument('--lines', type=int, default=3,
                      help='Number of context lines (default: 3)')
    parser.add_argument('--no-color', action='store_true',
                      help='Disable color output')

    # Directory comparison
    parser.add_argument('--compare-dirs', action='store_true',
                      help='Compare directories instead of files')
    parser.add_argument('-r', '--recursive', action='store_true',
                      help='Recursive directory comparison')

    args = parser.parse_args()

    # String comparison
    if args.string:
        if len(args.string) != 2:
            print("Error: --string requires two arguments", file=sys.stderr)
            return 1
        differ = FileDiffer(context_lines=args.lines)
        print(differ.compare_strings(args.string[0], args.string[1]))
        return 0

    # Directory comparison
    if args.compare_dirs:
        if not args.file1 or not args.file2:
            print("Error: Directory comparison requires two directories", file=sys.stderr)
            return 1

        if not Path(args.file1).is_dir() or not Path(args.file2).is_dir():
            print("Error: Both paths must be directories", file=sys.stderr)
            return 1

        differ = FileDiffer(context_lines=args.lines)
        results = differ.compare_directories(args.file1, args.file2, args.recursive)

        if not results:
            print("✅ No differences found")
            return 0

        print(f"📁 Directory Comparison: {args.file1} vs {args.file2}\n")

        changed = [r for r in results if r[0] == 'changed']
        only_in_1 = [r for r in results if r[0] == 'only_in_1']
        only_in_2 = [r for r in results if r[0] == 'only_in_2']

        if changed:
            print(f"📝 Changed files ({len(changed)}):")
            for _, file1, file2 in changed:
                print(f"  {file1}")

        if only_in_1:
            print(f"\n❌ Only in {args.file1} ({len(only_in_1)}):")
            for _, file1, _ in only_in_1:
                rel_path = Path(file1).relative_to(args.file1)
                print(f"  {rel_path}")

        if only_in_2:
            print(f"\n✅ Only in {args.file2} ({len(only_in_2)}):")
            for _, _, file2 in only_in_2:
                rel_path = Path(file2).relative_to(args.file2)
                print(f"  {rel_path}")

        return 0

    # File comparison
    if not args.file1 or not args.file2:
        parser.print_help()
        return 1

    if not Path(args.file1).exists():
        print(f"Error: File not found: {args.file1}", file=sys.stderr)
        return 1

    if not Path(args.file2).exists():
        print(f"Error: File not found: {args.file2}", file=sys.stderr)
        return 1

    differ = FileDiffer(context_lines=args.lines)

    # Determine format
    if args.context:
        diff_output = differ.compare_files(
            args.file1, args.file2,
            unified=False, side_by_side=False,
            color=not args.no_color
        )
    elif args.side_by_side:
        diff_output = differ.compare_files(
            args.file1, args.file2,
            unified=False, side_by_side=True,
            color=not args.no_color
        )
    else:
        diff_output = differ.compare_files(
            args.file1, args.file2,
            unified=True, side_by_side=False,
            color=not args.no_color
        )

    if not diff_output:
        print("✅ Files are identical")
    else:
        print(diff_output)

    return 0


if __name__ == '__main__':
    sys.exit(main())
