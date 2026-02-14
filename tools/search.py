#!/usr/bin/env python3
"""
Simple search utility for squad research.
Supports searching outputs directory and web search integration.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess


def search_outputs(query, directory=None):
    """Search output files for query string"""
    if directory is None:
        directory = os.path.expanduser("~/.openclaw/workspace/outputs")
    
    results = []
    output_dir = Path(directory)
    
    if not output_dir.exists():
        print(f"Output directory {directory} not found")
        return []
    
    # Search through markdown files
    for file_path in output_dir.glob("*.md"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if query.lower() in content.lower():
                    # Extract relevant context around matches
                    lines = content.split('\n')
                    matches = []
                    for i, line in enumerate(lines):
                        if query.lower() in line.lower():
                            # Get context lines
                            start = max(0, i - 2)
                            end = min(len(lines), i + 3)
                            context = lines[start:end]
                            matches.append({
                                'line_num': i + 1,
                                'context': '\n'.join(context)
                            })
                    
                    results.append({
                        'file': str(file_path),
                        'matches': matches
                    })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return results


def web_search_cli(query, count=10):
    """Simple web search using brave via curl (fallback)"""
    try:
        # Try to use web search tool if available
        cmd = ["curl", "-s", 
               "https://api.search.brave.com/res/v1/web/search",
               "-H", f"X-Subscription-Token: {os.getenv('BRAVE_API_KEY', '')}",
               "-H", "Accept: application/json",
               "-G", "-d", f"q={query}", "-d", f"count={count}"]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('web', {}).get('results', [])
        else:
            print(f"Web search failed: {result.stderr}")
            return []
    except Exception as e:
        print(f"Web search error: {e}")
        return []


def format_results(results, query, search_type="local"):
    """Format search results for display"""
    if not results:
        print(f"No results found for '{query}'")
        return
    
    print(f"\n=== {search_type.upper()} SEARCH RESULTS for '{query}' ===\n")
    
    if search_type == "local":
        for i, result in enumerate(results, 1):
            file_name = os.path.basename(result['file'])
            print(f"{i}. {file_name}")
            for match in result['matches']:
                print(f"   Line {match['line_num']}:")
                for line in match['context'].split('\n'):
                    print(f"     {line}")
                print()
    elif search_type == "web":
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            url = result.get('url', 'No URL')
            description = result.get('description', 'No description')
            
            print(f"{i}. {title}")
            print(f"   URL: {url}")
            print(f"   {description[:200]}..." if len(description) > 200 else f"   {description}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Search utility for squad research")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--web", action="store_true", help="Search web instead of local files")
    parser.add_argument("--count", type=int, default=10, help="Number of web results (default: 10)")
    parser.add_argument("--dir", help="Directory to search (default: outputs)")
    parser.add_argument("--version", action="version", version="search.py 1.0.0")
    
    args = parser.parse_args()
    
    if args.web:
        results = web_search_cli(args.query, args.count)
        format_results(results, args.query, "web")
    else:
        results = search_outputs(args.query, args.dir)
        format_results(results, args.query, "local")


if __name__ == "__main__":
    main()