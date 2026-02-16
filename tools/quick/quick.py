#!/usr/bin/env python3
"""
quick — Quick CLI Utilities

Fast conversions and calculations right in your terminal.
"""

import sys
import argparse
import base64
import urllib.parse
import json
from datetime import datetime
from typing import Tuple


class QuickUtils:
    """Quick CLI utilities."""

    def base64_encode(self, text: str, url_safe: bool = False):
        """Encode text to base64."""
        if url_safe:
            encoded = base64.urlsafe_b64encode(text.encode()).decode()
        else:
            encoded = base64.b64encode(text.encode()).decode()
        print(f"{encoded}")
        return True

    def base64_decode(self, text: str, url_safe: bool = False):
        """Decode base64 to text."""
        try:
            if url_safe:
                decoded = base64.urlsafe_b64decode(text).decode()
            else:
                decoded = base64.b64decode(text).decode()
            print(f"{decoded}")
            return True
        except Exception as e:
            print(f"❌ Decoding failed: {e}")
            return False

    def url_encode(self, text: str):
        """URL encode text."""
        encoded = urllib.parse.quote(text, safe='')
        print(f"{encoded}")
        return True

    def url_decode(self, text: str):
        """URL decode text."""
        decoded = urllib.parse.unquote(text)
        print(f"{decoded}")
        return True

    def timestamp(self, ts: str = None, format: str = 'iso'):
        """Convert or show timestamps."""
        if ts:
            # Parse timestamp and format
            try:
                # Try Unix timestamp
                if ts.isdigit():
                    dt = datetime.fromtimestamp(int(ts))
                else:
                    # Try ISO format
                    dt = datetime.fromisoformat(ts)

                self._print_timestamp(dt, format)
                return True
            except Exception as e:
                print(f"❌ Invalid timestamp: {e}")
                return False
        else:
            # Show current time
            dt = datetime.now()
            self._print_timestamp(dt, format)
            return True

    def _print_timestamp(self, dt: datetime, format: str):
        """Print timestamp in different formats."""
        print(f"📅 {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        if format == 'iso':
            print(f"ISO:     {dt.isoformat()}")
        elif format == 'unix':
            print(f"Unix:    {int(dt.timestamp())}")
        elif format == 'all':
            print(f"ISO:     {dt.isoformat()}")
            print(f"Unix:    {int(dt.timestamp())}")
            print(f"RFC2822: {dt.strftime('%a, %d %b %Y %H:%M:%S %z')}")
            print(f"ISO8601: {dt.strftime('%Y-%m-%dT%H:%M:%S%z')}")
        else:
            # Show all by default
            print(f"ISO:     {dt.isoformat()}")
            print(f"Unix:    {int(dt.timestamp())}")
            print(f"RFC2822: {dt.strftime('%a, %d %b %Y %H:%M:%S %z')}")

    def hex_to_rgb(self, hex_color: str):
        """Convert hex color to RGB."""
        # Remove # if present
        hex_color = hex_color.lstrip('#')

        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

            print(f"RGB: rgb({r}, {g}, {b})")
            print(f"CSS: rgb({r}, {g}, {b})")
            print(f"HSL: {self._rgb_to_hsl(r, g, b)}")
            return True
        else:
            print(f"❌ Invalid hex color: {hex_color}")
            print(f"   Expected: RRGGBB (6 hex digits)")
            return False

    def _rgb_to_hsl(self, r: int, g: int, b: int) -> str:
        """Convert RGB to HSL."""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        max_c = max(r_norm, g_norm, b_norm)
        min_c = min(r_norm, g_norm, b_norm)
        l = (max_c + min_c) / 2

        if max_c == min_c:
            h = s = 0
        else:
            d = max_c - min_c
            s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)

            if max_c == r_norm:
                h = (g_norm - b_norm) / d % 6
            elif max_c == g_norm:
                h = (b_norm - r_norm) / d + 2
            else:
                h = (r_norm - g_norm) / d + 4

            h = h * 60

        return f"hsl({int(h)}, {int(s * 100)}%, {int(l * 100)}%)"

    def json_format(self, text: str):
        """Format JSON text."""
        try:
            data = json.loads(text)
            print(json.dumps(data, indent=2))
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return False

    def json_minify(self, text: str):
        """Minify JSON text."""
        try:
            data = json.loads(text)
            print(json.dumps(data, separators=(',', ':')))
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return False

    def string_length(self, text: str, bytes: bool = False):
        """Calculate string length."""
        if bytes:
            length = len(text.encode('utf-8'))
            print(f"Bytes:   {length}")
        else:
            length = len(text)
            print(f"Chars:   {length}")
        print(f"Words:    {len(text.split())}")
        print(f"Lines:    {len(text.split(chr(10)))}")
        return True

    def generate_uuid(self):
        """Generate a random UUID."""
        import uuid
        print(f"{str(uuid.uuid4())}")
        return True

    def hash_text(self, text: str, algorithm: str = 'md5'):
        """Hash text."""
        import hashlib

        algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }

        if algorithm not in algorithms:
            print(f"❌ Unsupported algorithm: {algorithm}")
            print(f"   Available: {', '.join(algorithms.keys())}")
            return False

        hash_obj = algorithms[algorithm](text.encode())
        hash_hex = hash_obj.hexdigest()
        print(f"{algorithm.upper()}: {hash_hex}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='quick — Quick CLI Utilities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  quick b64encode "Hello World"
  quick b64decode "SGVsbG8gV29ybGQ="
  quick url_encode "hello world"
  quick timestamp 1640000000
  quick hex2rgb "#3b82f6"
  quick json-pretty '{"name":"test"}'
  quick hash "my-password"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Base64 encode
    b64enc_parser = subparsers.add_parser('b64encode', help='Encode to base64')
    b64enc_parser.add_argument('text', help='Text to encode')
    b64enc_parser.add_argument('--urlsafe', action='store_true', help='URL-safe encoding')

    # Base64 decode
    b64dec_parser = subparsers.add_parser('b64decode', help='Decode from base64')
    b64dec_parser.add_argument('text', help='Text to decode')
    b64dec_parser.add_argument('--urlsafe', action='store_true', help='URL-safe decoding')

    # URL encode
    urlenc_parser = subparsers.add_parser('urlencode', help='URL encode text')
    urlenc_parser.add_argument('text', help='Text to encode')

    # URL decode
    urldec_parser = subparsers.add_parser('urldecode', help='URL decode text')
    urldec_parser.add_argument('text', help='Text to decode')

    # Timestamp
    ts_parser = subparsers.add_parser('timestamp', help='Convert or show timestamps')
    ts_parser.add_argument('ts', nargs='?', help='Timestamp (Unix or ISO)')
    ts_parser.add_argument('-f', '--format', default='iso',
                          choices=['iso', 'unix', 'all'], help='Output format')

    # Hex to RGB
    hex_parser = subparsers.add_parser('hex2rgb', help='Convert hex color to RGB/HSL')
    hex_parser.add_argument('hex', help='Hex color (with or without #)')

    # JSON format
    jsonfmt_parser = subparsers.add_parser('json-pretty', help='Format JSON')
    jsonfmt_parser.add_argument('text', help='JSON text or file path')

    # JSON minify
    jsonmin_parser = subparsers.add_parser('json-minify', help='Minify JSON')
    jsonmin_parser.add_argument('text', help='JSON text or file path')

    # String length
    len_parser = subparsers.add_parser('strlen', help='Calculate string length')
    len_parser.add_argument('text', help='Text to measure')
    len_parser.add_argument('--bytes', action='store_true', help='Count bytes instead of characters')

    # Generate UUID
    subparsers.add_parser('uuid', help='Generate a random UUID')

    # Hash
    hash_parser = subparsers.add_parser('hash', help='Hash text')
    hash_parser.add_argument('text', help='Text to hash')
    hash_parser.add_argument('-a', '--algorithm', default='md5',
                           choices=['md5', 'sha1', 'sha256', 'sha512'],
                           help='Hash algorithm')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    utils = QuickUtils()

    if args.command == 'b64encode':
        utils.base64_encode(args.text, args.urlsafe)
    elif args.command == 'b64decode':
        utils.base64_decode(args.text, args.urlsafe)
    elif args.command == 'urlencode':
        utils.url_encode(args.text)
    elif args.command == 'urldecode':
        utils.url_decode(args.text)
    elif args.command == 'timestamp':
        utils.timestamp(args.ts, args.format)
    elif args.command == 'hex2rgb':
        utils.hex_to_rgb(args.hex)
    elif args.command == 'json-pretty':
        utils.json_format(args.text)
    elif args.command == 'json-minify':
        utils.json_minify(args.text)
    elif args.command == 'strlen':
        utils.string_length(args.text, args.bytes)
    elif args.command == 'uuid':
        utils.generate_uuid()
    elif args.command == 'hash':
        utils.hash_text(args.text, args.algorithm)

    return 0


if __name__ == '__main__':
    sys.exit(main())
