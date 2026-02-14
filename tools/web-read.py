#!/usr/bin/env python3
"""
Web content reading utility for squad research.
Simplifies fetching and extracting content from URLs.
"""

import os
import sys
import json
import argparse
from pathlib import Path
import subprocess
import re
from urllib.parse import urlparse


def fetch_content(url, extract_mode="text", max_chars=5000):
    """Fetch and extract content from URL"""
    try:
        # Try to use textise dot iitty as a simple text extraction service
        # Fallback to curl for basic content
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SquadResearch/1.0)'
        }
        
        cmd = ["curl", "-s", "-L", "-m", "30", "--compressed"]
        for key, value in headers.items():
            cmd.extend(["-H", f"{key}: {value}"])
        cmd.append(url)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"Failed to fetch {url}: {result.stderr}")
            return None
        
        content = result.stdout
        
        # Basic HTML tag removal for text mode
        if extract_mode == "text":
            content = remove_html_tags(content)
            # Clean up whitespace
            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = content.strip()
        
        # Truncate if too long
        if len(content) > max_chars:
            content = content[:max_chars] + "..."
        
        return {
            'url': url,
            'content': content,
            'length': len(content),
            'extract_mode': extract_mode,
            'fetched_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def remove_html_tags(text):
    """Remove HTML tags from text"""
    # Simple tag removal - not perfect but functional
    clean = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    clean = clean.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    clean = clean.replace('&quot;', '"').replace('&#39;', "'")
    return clean


def extract_title(content):
    """Extract title from HTML content"""
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
    if title_match:
        return remove_html_tags(title_match.group(1)).strip()
    return "No title found"


def save_content(result, output_dir=None):
    """Save fetched content to file"""
    if output_dir is None:
        output_dir = Path.home() / ".openclaw" / "workspace" / "cache"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename from URL
    parsed = urlparse(result['url'])
    filename = f"{parsed.netloc}_{parsed.path.replace('/', '_')}.txt"
    # Clean filename
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    
    output_file = output_dir / filename
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {result['url']}\n")
            f.write(f"Fetched: {result['fetched_at']}\n")
            f.write(f"Length: {result['length']} chars\n")
            f.write(f"Mode: {result['extract_mode']}\n")
            f.write("=" * 50 + "\n\n")
            f.write(result['content'])
        
        return output_file
    except Exception as e:
        print(f"Error saving content: {e}")
        return None


def display_content(result):
    """Display fetched content"""
    print(f"\n=== CONTENT from {result['url']} ===")
    print(f"Length: {result['length']} characters")
    print(f"Fetched: {result['fetched_at']}")
    print(f"Mode: {result['extract_mode']}")
    print("=" * 50)
    print(result['content'])
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Web content reading utility")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--mode", choices=["text", "html"], default="text",
                       help="Extraction mode (default: text)")
    parser.add_argument("--max-chars", type=int, default=5000,
                       help="Maximum characters to return (default: 5000)")
    parser.add_argument("--save", action="store_true", help="Save to cache directory")
    parser.add_argument("--output-dir", help="Output directory for saved content")
    parser.add_argument("--version", action="version", version="web-read.py 1.0.0")
    
    args = parser.parse_args()
    
    # Validate URL
    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print("Error: Invalid URL")
        sys.exit(1)
    
    result = fetch_content(args.url, args.mode, args.max_chars)
    
    if result:
        display_content(result)
        
        if args.save:
            output_file = save_content(result, args.output_dir)
            if output_file:
                print(f"\nContent saved to: {output_file}")
    else:
        print("Failed to fetch content")
        sys.exit(1)


if __name__ == "__main__":
    # Add datetime import at top if not already imported
    from datetime import datetime
    main()