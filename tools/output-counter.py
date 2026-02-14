#!/usr/bin/env python3
"""
Script to count outputs per agent per day in the outputs directory.
Usage: python3 output-counter.py [date_format]
Default date format: YYYY-MM-DD
"""

import os
import sys
import re
from collections import defaultdict
from datetime import datetime

def count_outputs(outputs_dir):
    """Count outputs by agent and date."""
    if not os.path.exists(outputs_dir):
        print(f"Outputs directory {outputs_dir} does not exist")
        return
    
    agent_counts = defaultdict(lambda: defaultdict(int))
    
    for filename in os.listdir(outputs_dir):
        if not filename.endswith('.md'):
            continue
            
        # Extract date and agent from filename
        # Expected format: YYYY-MM-DD-<agent>-<topic>.md or YYYY-MM-DD-<topic>.md
        match = re.match(r'(\d{4}-\d{2}-\d{2})(?:-(\w+))?-', filename)
        if match:
            date_str, agent = match.groups()
            agent = agent or 'unknown'
            agent_counts[agent][date_str] += 1
    
    # Print results
    if not agent_counts:
        print("No output files found")
        return
    
    print("Output Count by Agent and Date:")
    print("=" * 40)
    
    for agent in sorted(agent_counts.keys()):
        print(f"\n{agent.upper()}:")
        for date in sorted(agent_counts[agent].keys()):
            count = agent_counts[agent][date]
            print(f"  {date}: {count} outputs")
    
    # Totals by agent
    print(f"\nTotals by Agent:")
    for agent in sorted(agent_counts.keys()):
        total = sum(agent_counts[agent].values())
        print(f"  {agent.upper()}: {total} outputs")

if __name__ == "__main__":
    outputs_dir = os.path.expanduser("~/.openclaw/workspace/outputs")
    count_outputs(outputs_dir)