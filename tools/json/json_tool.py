#!/usr/bin/env python3
"""
json — JSON Manipulation Tool

Parse, validate, query, format, and manipulate JSON data.
"""

import sys
import argparse
import json as json_lib
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import re


class JSONTool:
    """JSON manipulation tool."""

    def __init__(self):
        self.indent = 2
        self.sort_keys = False
        self.ensure_ascii = False

    def parse_file(self, file_path: str) -> Optional[Dict]:
        """Parse JSON from file."""
        try:
            path = Path(file_path)
            with open(path, 'r') as f:
                return json_lib.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            return None
        except json_lib.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return None

    def parse_string(self, json_str: str) -> Optional[Dict]:
        """Parse JSON from string."""
        try:
            return json_lib.loads(json_str)
        except json_lib.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            return None

    def validate(self, json_str: str) -> bool:
        """Validate JSON string."""
        try:
            json_lib.loads(json_str)
            return True
        except json_lib.JSONDecodeError:
            return False

    def query(self, data: Any, path: str) -> Any:
        """Query JSON data using dot notation."""
        if not path:
            return data

        # Remove leading dot if present
        if path.startswith('.'):
            path = path[1:]

        keys = path.split('.')
        result = data

        for key in keys:
            # Handle array indexing
            if '[' in key:
                match = re.match(r'(\w+)\[(\d+)\]', key)
                if match:
                    array_key = match.group(1)
                    index = int(match.group(2))

                    if isinstance(result, dict) and array_key in result:
                        result = result[array_key]
                        if isinstance(result, list) and index < len(result):
                            result = result[index]
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            else:
                # Simple key access
                if isinstance(result, dict) and key in result:
                    result = result[key]
                elif isinstance(result, list) and key.isdigit():
                    index = int(key)
                    if index < len(result):
                        result = result[index]
                    else:
                        return None
                else:
                    return None

        return result

    def format_json(self, data: Any, indent: int = None,
                    sort_keys: bool = None, compact: bool = False) -> str:
        """Format JSON data."""
        if indent is None:
            indent = 0 if compact else self.indent

        if sort_keys is None:
            sort_keys = self.sort_keys

        if compact:
            return json_lib.dumps(data, separators=(',', ':'),
                            ensure_ascii=self.ensure_ascii)
        else:
            return json_lib.dumps(data, indent=indent, sort_keys=sort_keys,
                            ensure_ascii=self.ensure_ascii)

    def merge(self, *data_list: Dict, deep: bool = False) -> Dict:
        """Merge multiple JSON objects."""
        result = {}

        for data in data_list:
            if deep:
                result = self._deep_merge(result, data)
            else:
                result.update(data)

        return result

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Deep merge two dicts."""
        result = base.copy()

        for key, value in update.items():
            if (key in result and
                isinstance(result[key], dict) and
                isinstance(value, dict)):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def diff(self, data1: Dict, data2: Dict) -> Dict:
        """Find differences between two JSON objects."""
        diff = {
            'added': [],
            'removed': [],
            'changed': [],
        }

        # Find added keys
        for key in data2:
            if key not in data1:
                diff['added'].append(key)

        # Find removed keys
        for key in data1:
            if key not in data2:
                diff['removed'].append(key)

        # Find changed keys
        for key in data1:
            if key in data2 and data1[key] != data2[key]:
                diff['changed'].append({
                    'key': key,
                    'old': data1[key],
                    'new': data2[key],
                })

        return diff

    def flatten(self, data: Any, prefix: str = '') -> Dict:
        """Flatten nested JSON object."""
        result = {}

        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, (dict, list)):
                    result.update(self.flatten(value, new_key))
                else:
                    result[new_key] = value

        elif isinstance(data, list):
            for i, value in enumerate(data):
                new_key = f"{prefix}[{i}]" if prefix else f"[{i}]"
                if isinstance(value, (dict, list)):
                    result.update(self.flatten(value, new_key))
                else:
                    result[new_key] = value

        else:
            result[prefix] = data

        return result

    def unflatten(self, data: Dict) -> Dict:
        """Unflatten JSON object."""
        result = {}

        for key, value in data.items():
            # Handle array indexing
            if '[' in key:
                match = re.match(r'(.+)\[(\d+)\]$', key)
                if match:
                    base_key = match.group(1)
                    index = int(match.group(2))

                    if base_key not in result:
                        result[base_key] = []

                    # Ensure array is large enough
                    while len(result[base_key]) <= index:
                        result[base_key].append(None)

                    result[base_key][index] = value
                    continue

            # Handle nested keys
            keys = key.split('.')
            current = result

            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]

            current[keys[-1]] = value

        return result

    def keys(self, data: Any) -> List[str]:
        """Get all keys from JSON object."""
        if not isinstance(data, dict):
            return []

        return list(data.keys())

    def values(self, data: Any) -> List[Any]:
        """Get all values from JSON object."""
        if not isinstance(data, dict):
            return []

        return list(data.values())

    def size(self, data: Any) -> int:
        """Get size of JSON object."""
        if isinstance(data, dict):
            return len(data)
        elif isinstance(data, list):
            return len(data)
        elif isinstance(data, str):
            return len(data)
        elif isinstance(data, (int, float)):
            return 1
        else:
            return 0

    def type(self, data: Any) -> str:
        """Get type of JSON value."""
        if isinstance(data, dict):
            return 'object'
        elif isinstance(data, list):
            return 'array'
        elif isinstance(data, str):
            return 'string'
        elif isinstance(data, int):
            return 'integer'
        elif isinstance(data, float):
            return 'number'
        elif isinstance(data, bool):
            return 'boolean'
        elif data is None:
            return 'null'
        else:
            return 'unknown'

    def get_paths(self, data: Any, prefix: str = '') -> List[str]:
        """Get all paths in JSON object."""
        paths = []

        if isinstance(data, dict):
            for key, value in data.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                paths.append(new_prefix)
                if isinstance(value, (dict, list)):
                    paths.extend(self.get_paths(value, new_prefix))

        elif isinstance(data, list):
            for i, value in enumerate(data):
                new_prefix = f"{prefix}[{i}]" if prefix else f"[{i}]"
                paths.append(new_prefix)
                if isinstance(value, (dict, list)):
                    paths.extend(self.get_paths(value, new_prefix))

        return paths


def main():
    parser = argparse.ArgumentParser(
        description='json — JSON Manipulation Tool'
    )

    # Input options
    parser.add_argument('file', nargs='?', help='JSON file or string')
    parser.add_argument('--string', '-s', action='store_true',
                      help='Treat input as JSON string')

    # Query options
    parser.add_argument('--query', '-q', metavar='PATH',
                      help='Query JSON using dot notation')
    parser.add_argument('--keys', action='store_true',
                      help='Get all keys')
    parser.add_argument('--values', action='store_true',
                      help='Get all values')
    parser.add_argument('--type', '-t', action='store_true',
                      help='Get type of value')

    # Format options
    parser.add_argument('--format', '-f', action='store_true',
                      help='Format JSON (pretty print)')
    parser.add_argument('--compact', '-c', action='store_true',
                      help='Compact JSON output')
    parser.add_argument('--indent', type=int, default=2,
                      help='Indentation spaces (default: 2)')
    parser.add_argument('--sort', action='store_true',
                      help='Sort keys')

    # Manipulation options
    parser.add_argument('--flatten', action='store_true',
                      help='Flatten nested JSON')
    parser.add_argument('--unflatten', action='store_true',
                      help='Unflatten JSON')
    parser.add_argument('--merge', metavar='FILE', nargs='+',
                      help='Merge multiple JSON files')
    parser.add_argument('--deep', action='store_true',
                      help='Deep merge')
    parser.add_argument('--diff', metavar='FILE',
                      help='Diff with another JSON file')

    # Info options
    parser.add_argument('--size', action='store_true',
                      help='Get size of JSON')
    parser.add_argument('--validate', action='store_true',
                      help='Validate JSON')
    parser.add_argument('--paths', action='store_true',
                      help='Get all paths')

    args = parser.parse_args()

    tool = JSONTool()
    tool.indent = args.indent
    tool.sort_keys = args.sort

    # Validate
    if args.validate:
        if args.string:
            data = args.file
        else:
            with open(args.file, 'r') as f:
                data = f.read()

        is_valid = tool.validate(data)
        print("Valid" if is_valid else "Invalid")
        return 0 if is_valid else 1

    # Parse input
    if args.string:
        data = tool.parse_string(args.file)
    else:
        data = tool.parse_file(args.file)

    if data is None:
        return 1

    # Query
    if args.query:
        result = tool.query(data, args.query)
        print(tool.format_json(result, compact=args.compact))
        return 0

    # Keys
    if args.keys:
        keys = tool.keys(data)
        print(tool.format_json(keys))
        return 0

    # Values
    if args.values:
        values = tool.values(data)
        print(tool.format_json(values))
        return 0

    # Type
    if args.type:
        print(tool.type(data))
        return 0

    # Format
    if args.format:
        print(tool.format_json(data, compact=args.compact))
        return 0

    # Flatten
    if args.flatten:
        flat = tool.flatten(data)
        print(tool.format_json(flat))
        return 0

    # Unflatten
    if args.unflatten:
        flat = tool.flatten(data)  # First flatten
        unflat = tool.unflatten(flat)
        print(tool.format_json(unflat))
        return 0

    # Merge
    if args.merge:
        data_list = [data]
        for file in args.merge:
            merge_data = tool.parse_file(file)
            if merge_data:
                data_list.append(merge_data)

        result = tool.merge(*data_list, deep=args.deep)
        print(tool.format_json(result))
        return 0

    # Diff
    if args.diff:
        data2 = tool.parse_file(args.diff)
        if data2:
            diff = tool.diff(data, data2)
            print(tool.format_json(diff))
        return 0

    # Size
    if args.size:
        print(tool.size(data))
        return 0

    # Paths
    if args.paths:
        paths = tool.get_paths(data)
        print(tool.format_json(paths))
        return 0

    # Default: format JSON
    print(tool.format_json(data))
    return 0


if __name__ == '__main__':
    sys.exit(main())
