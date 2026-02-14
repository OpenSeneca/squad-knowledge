#!/usr/bin/env python3
"""
Script to check output format compliance.
Verifies that outputs have Sources and Key Findings sections.
Usage: python3 format-checker.py
"""

import os
import re
from datetime import datetime

def check_file_compliance(filepath):
    """Check if a single file complies with format requirements."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    # Check for Key Findings section
    key_findings_match = re.search(r'^## Key Findings\s*$', content, re.MULTILINE)
    if not key_findings_match:
        return False, "Missing '## Key Findings' section"
    
    # Check for Sources section
    sources_match = re.search(r'^## Sources\s*$', content, re.MULTILINE)
    if not sources_match:
        return False, "Missing '## Sources' section"
    
    # Check if Key Findings has actual content (at least one bullet point)
    key_findings_section = re.search(r'## Key Findings\s*\n(.*?)(?=\n##|\n\Z)', content, re.DOTALL | re.IGNORECASE)
    if key_findings_section:
        findings_text = key_findings_section.group(1)
        if not re.search(r'^\s*-\s', findings_text, re.MULTILINE):
            return False, "Key Findings section has no bullet points"
    
    # Check if Sources has actual content
    sources_section = re.search(r'## Sources\s*\n(.*?)(?=\n##|\n\Z)', content, re.DOTALL | re.IGNORECASE)
    if sources_section:
        sources_text = sources_section.group(1)
        if not re.search(r'\[.*?\]\(.*?\)', sources_text):
            return False, "Sources section has no markdown links"
    
    return True, "Format compliant"

def check_all_outputs(outputs_dir):
    """Check all output files for format compliance."""
    if not os.path.exists(outputs_dir):
        print(f"Outputs directory {outputs_dir} does not exist")
        return
    
    files_checked = 0
    files_compliant = 0
    issues_found = []
    
    for filename in os.listdir(outputs_dir):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(outputs_dir, filename)
        files_checked += 1
        
        is_compliant, message = check_file_compliance(filepath)
        
        if is_compliant:
            files_compliant += 1
        else:
            issues_found.append((filename, message))
    
    # Print results
    print(f"Format Compliance Check Results:")
    print("=" * 40)
    print(f"Files checked: {files_checked}")
    print(f"Files compliant: {files_compliant}")
    print(f"Compliance rate: {(files_compliant/files_checked*100):.1f}%" if files_checked > 0 else "N/A")
    
    if issues_found:
        print(f"\nIssues found:")
        for filename, issue in issues_found:
            print(f"  {filename}: {issue}")
    else:
        print("\nAll files are compliant!")

if __name__ == "__main__":
    outputs_dir = os.path.expanduser("~/.openclaw/workspace/outputs")
    check_all_outputs(outputs_dir)