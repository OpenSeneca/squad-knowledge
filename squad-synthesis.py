#!/usr/bin/env python3
"""
Squad Research Synthesis Tool
Automatically compiles and organizes squad findings from completed tasks.
"""

import os
import re
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class TaskFinding:
    """Represents a single task finding"""
    title: str
    agent: str
    category: str
    domain: str
    date: datetime
    status: str
    findings: List[str]
    urls: List[str]
    impact: str
    file_path: str

class SquadSynthesis:
    def __init__(self, workspace_path: str = None):
        """Initialize the synthesis tool"""
        self.workspace_path = workspace_path or os.path.expanduser("~/.openclaw/workspace")
        self.completed_dirs = self._find_completed_directories()
        
    def _find_completed_directories(self) -> List[str]:
        """Find all completed task directories across squad agents"""
        completed_dirs = []
        
        try:
            # Search for completed directories in workspace
            for root, dirs, files in os.walk(self.workspace_path):
                if "completed" in dirs:
                    completed_path = os.path.join(root, "completed")
                    if os.path.exists(completed_path):
                        completed_dirs.append(completed_path)
        except Exception as e:
            print(f"Warning: Error scanning workspace: {e}")
        
        if not completed_dirs:
            print("Warning: No completed task directories found")
            
        return completed_dirs
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'https?://[^\s\)]+(?:\([^)]*\))?|[^\s]*\.[a-zA-Z]{2,}(?:/[^\s]*)?'
        urls = re.findall(url_pattern, text)
        return [url for url in urls if not url.endswith('.')]
    
    def _categorize_domain(self, content: str, title: str) -> str:
        """Categorize task by domain based on content and title"""
        content_lower = content.lower()
        title_lower = title.lower()
        
        # AI/ML keywords
        ai_ml_keywords = ['marl', 'machine learning', 'reinforcement learning', 'ai', 'model', 'algorithm', 'training', 'neural', 'deep learning']
        # Biopharma keywords  
        biopharma_keywords = ['biotech', 'pharma', 'drug', 'clinical', 'trial', 'protein', 'genomic', 'medical', 'healthcare']
        # Competitive intel keywords
        competitive_keywords = ['competitive', 'market', 'analysis', 'intel', 'competitor', 'landscape', 'benchmark']
        
        if any(keyword in content_lower or keyword in title_lower for keyword in ai_ml_keywords):
            return "AI/ML"
        elif any(keyword in content_lower or keyword in title_lower for keyword in biopharma_keywords):
            return "Biopharma"
        elif any(keyword in content_lower or keyword in title_lower for keyword in competitive_keywords):
            return "Competitive Intel"
        else:
            return "General"
    
    def _parse_task_file(self, file_path: str) -> Optional[TaskFinding]:
        """Parse a single task markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        
        # Extract metadata
        title = self._extract_title(content)
        agent = self._extract_metadata_field(content, 'Assigned To') or self._guess_agent_from_path(file_path)
        category = self._extract_metadata_field(content, 'Category') or 'Unknown'
        date_str = self._extract_metadata_field(content, 'Start Date') or self._extract_metadata_field(content, 'Date')
        status = self._extract_metadata_field(content, 'Status') or 'Unknown'
        
        # Parse date
        date = self._parse_date(date_str)
        
        # Extract findings
        findings = self._extract_findings(content)
        
        # Extract URLs
        urls = self._extract_urls(content)
        
        # Extract impact
        impact = self._extract_impact(content)
        
        # Categorize domain
        domain = self._categorize_domain(content, title)
        
        return TaskFinding(
            title=title,
            agent=agent,
            category=category,
            domain=domain,
            date=date,
            status=status,
            findings=findings,
            urls=urls,
            impact=impact,
            file_path=file_path
        )
    
    def _extract_title(self, content: str) -> str:
        """Extract title from markdown content"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return "Untitled Task"
    
    def _extract_metadata_field(self, content: str, field: str) -> Optional[str]:
        """Extract metadata field from content"""
        pattern = rf'-?\s*\*\*{field}\*\*:\s*([^\n]+)'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _guess_agent_from_path(self, file_path: str) -> str:
        """Guess agent name from file path"""
        path_parts = file_path.split('/')
        for part in path_parts:
            if part in ['archimedes', 'marcus', 'argus', 'galen', 'seneca']:
                return part.capitalize()
        return "Unknown"
    
    def _parse_date(self, date_str: Optional[str]) -> datetime:
        """Parse date string to datetime object"""
        if not date_str:
            return datetime.now()
        
        # Try common date formats
        formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M', '%Y/%m/%d', '%m/%d/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        return datetime.now()
    
    def _extract_findings(self, content: str) -> List[str]:
        """Extract key findings from content"""
        findings = []
        
        # Look for sections that might contain findings
        sections = ['## Findings', '## Results', '## Impact', '## Key Results', '## Outcomes']
        
        for section in sections:
            pattern = rf'{re.escape(section)}\s*\n(.*?)(?=## |\Z)'
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                section_content = match.group(1).strip()
                # Extract bullet points
                bullet_pattern = r'^[\s]*[-*+]\s*(.+)$'
                bullets = re.findall(bullet_pattern, section_content, re.MULTILINE)
                findings.extend([bullet.strip() for bullet in bullets if bullet.strip()])
        
        return findings
    
    def _extract_impact(self, content: str) -> str:
        """Extract impact statement from content"""
        sections = ['## Impact Assessment', '## Impact', '## Business Impact']
        
        for section in sections:
            pattern = rf'{re.escape(section)}\s*\n(.*?)(?=## |\Z)'
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()[:200] + "..." if len(match.group(1)) > 200 else match.group(1).strip()
        
        return "No impact assessment available"
    
    def collect_findings(self, target_date: datetime = None, domain_filter: str = None, days_back: int = 1) -> List[TaskFinding]:
        """Collect all findings from completed tasks"""
        all_findings = []
        
        if not self.completed_dirs:
            print("Error: No completed task directories found")
            return all_findings
        
        for completed_dir in self.completed_dirs:
            try:
                print(f"Scanning {completed_dir}...")
                
                for file_name in os.listdir(completed_dir):
                    if file_name.endswith('.md'):
                        file_path = os.path.join(completed_dir, file_name)
                        
                        try:
                            finding = self._parse_task_file(file_path)
                            
                            if finding:
                                # Apply date filter for aggregate mode
                                if days_back > 1:
                                    date_diff = (datetime.now() - finding.date).days
                                    if date_diff > days_back:
                                        continue
                                elif target_date:
                                    if finding.date.date() != target_date.date():
                                        continue
                                
                                # Apply domain filter
                                if domain_filter and finding.domain.lower() != domain_filter.lower():
                                    continue
                                
                                all_findings.append(finding)
                                
                        except Exception as e:
                            print(f"Warning: Error processing {file_name}: {e}")
                            continue
                            
            except Exception as e:
                print(f"Warning: Error scanning directory {completed_dir}: {e}")
                continue
        
        return all_findings
    
    def calculate_summary_stats(self, findings: List[TaskFinding]) -> Dict[str, Any]:
        """Calculate summary statistics"""
        stats = {
            'total_tasks': len(findings),
            'domains': defaultdict(int),
            'agents': defaultdict(int),
            'date_range': {'earliest': None, 'latest': None}
        }
        
        for finding in findings:
            stats['domains'][finding.domain] += 1
            stats['agents'][finding.agent] += 1
            
            if stats['date_range']['earliest'] is None or finding.date < stats['date_range']['earliest']:
                stats['date_range']['earliest'] = finding.date
            if stats['date_range']['latest'] is None or finding.date > stats['date_range']['latest']:
                stats['date_range']['latest'] = finding.date
        
        return stats
    
    def generate_aggregate_summary(self, findings: List[TaskFinding], days_back: int) -> str:
        """Generate aggregate summary for multiple days"""
        stats = self.calculate_summary_stats(findings)
        
        # Group findings by domain
        domain_groups = defaultdict(list)
        for finding in findings:
            domain_groups[finding.domain].append(finding)
        
        # Sort domains by number of findings (descending)
        sorted_domains = sorted(domain_groups.items(), key=lambda x: len(x[1]), reverse=True)
        
        # Generate markdown
        md = f"""# Squad Research Aggregate Summary
**Period**: Last {days_back} days  
**Total Tasks**: {stats['total_tasks']}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary Statistics

### Overview
- **Total Tasks**: {stats['total_tasks']}
- **Agents Active**: {len(stats['agents'])}
- **Domains Covered**: {len(stats['domains'])}
- **Date Range**: {stats['date_range']['earliest'].strftime('%Y-%m-%d')} to {stats['date_range']['latest'].strftime('%Y-%m-%d')}

### By Domain
"""
        
        for domain, count in sorted(stats['domains'].items(), key=lambda x: x[1], reverse=True):
            md += f"- **{domain}**: {count} tasks ({count/stats['total_tasks']*100:.1f}%)\n"
        
        md += "\n### By Agent\n"
        for agent, count in sorted(stats['agents'].items(), key=lambda x: x[1], reverse=True):
            md += f"- **{agent}**: {count} tasks\n"
        
        md += "\n---\n\n"
        
        # Domain breakdown
        md += "## Detailed Findings by Domain\n\n"
        for domain, domain_findings in sorted_domains:
            md += f"### {domain} ({len(domain_findings)} tasks)\n\n"
            
            for finding in domain_findings:
                md += f"#### {finding.title}\n"
                md += f"- **Agent**: {finding.agent}\n"
                md += f"- **Date**: {finding.date.strftime('%Y-%m-%d')}\n"
                md += f"- **Status**: {finding.status}\n"
                md += f"- **Impact**: {finding.impact}\n"
                
                if finding.findings:
                    md += "- **Key Findings**:\n"
                    for finding_text in finding.findings[:3]:  # Limit to top 3
                        md += f"  - {finding_text}\n"
                
                if finding.urls:
                    md += "- **References**:\n"
                    for url in finding.urls[:3]:  # Limit to top 3
                        md += f"  - {url}\n"
                
                md += "\n"
        
        md += f"\n---\n*Report generated by Squad Synthesis Tool*\n"
        
        return md
    
    def generate_daily_summary(self, findings: List[TaskFinding], target_date: datetime) -> str:
        """Generate daily summary report"""
        stats = self.calculate_summary_stats(findings)
        
        # Group findings by domain
        domain_groups = defaultdict(list)
        for finding in findings:
            domain_groups[finding.domain].append(finding)
        
        # Sort domains by number of findings (descending)
        sorted_domains = sorted(domain_groups.items(), key=lambda x: len(x[1]), reverse=True)
        
        # Generate markdown
        md = f"""# Squad Research Daily Summary
**Date**: {target_date.strftime('%Y-%m-%d')}  
**Total Tasks**: {stats['total_tasks']}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary Statistics

### Overview
- **Total Tasks**: {stats['total_tasks']}
- **Agents Active**: {len(stats['agents'])}
- **Domains Covered**: {len(stats['domains'])}

### By Domain
"""
        
        for domain, count in sorted(stats['domains'].items(), key=lambda x: x[1], reverse=True):
            md += f"- **{domain}**: {count} tasks ({count/stats['total_tasks']*100:.1f}%)\n"
        
        md += "\n### By Agent\n"
        for agent, count in sorted(stats['agents'].items(), key=lambda x: x[1], reverse=True):
            md += f"- **{agent}**: {count} tasks\n"
        
        md += "\n---\n\n"
        
        # Domain breakdown
        md += "## Domain Breakdown\n\n"
        for domain, domain_findings in sorted_domains:
            md += f"### {domain} ({len(domain_findings)} tasks)\n\n"
            
            for finding in domain_findings:
                md += f"#### {finding.title}\n"
                md += f"- **Agent**: {finding.agent}\n"
                md += f"- **Status**: {finding.status}\n"
                md += f"- **Impact**: {finding.impact}\n"
                
                if finding.findings:
                    md += "- **Key Findings**:\n"
                    for finding_text in finding.findings[:3]:  # Limit to top 3
                        md += f"  - {finding_text}\n"
                
                if finding.urls:
                    md += "- **References**:\n"
                    for url in finding.urls[:3]:  # Limit to top 3
                        md += f"  - {url}\n"
                
                md += "\n"
        
        # Quick stats
        md += "## Quick Stats\n\n"
        md += f"- **AI/ML Tasks**: {stats['domains'].get('AI/ML', 0)}\n"
        md += f"- **Biopharma Tasks**: {stats['domains'].get('Biopharma', 0)}\n"
        md += f"- **Competitive Intel Tasks**: {stats['domains'].get('Competitive Intel', 0)}\n"
        md += f"- **General Tasks**: {stats['domains'].get('General', 0)}\n"
        md += "\n"
        
        # Key URLs
        all_urls = []
        for finding in findings:
            all_urls.extend(finding.urls)
        
        if all_urls:
            md += "## Key References\n\n"
            for url in all_urls[:10]:  # Top 10 URLs
                md += f"- {url}\n"
        
        md += f"\n---\n*Report generated by Squad Synthesis Tool*\n"
        
        return md
    
    def save_report(self, content: str, filename: str, output_dir: str = None) -> str:
        """Save report to specified directory"""
        if output_dir:
            synthesis_dir = output_dir
        else:
            synthesis_dir = os.path.join(self.workspace_path, "daily-synthesis")
        
        os.makedirs(synthesis_dir, exist_ok=True)
        
        file_path = os.path.join(synthesis_dir, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return file_path
        except Exception as e:
            print(f"Error saving report: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Squad Research Synthesis Tool')
    parser.add_argument('--date', type=str, help='Target date (YYYY-MM-DD)', 
                       default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--aggregate', type=int, metavar='DAYS', help='Aggregate findings from last N days')
    parser.add_argument('--domain', type=str, help='Filter by specific domain (ai-ml, biopharma, competitive-intel, general)')
    parser.add_argument('--output-dir', type=str, help='Custom output directory')
    parser.add_argument('--workspace', type=str, help='Workspace path', 
                       default=os.path.expanduser("~/.openclaw/workspace"))
    parser.add_argument('--list-dirs', action='store_true', help='List completed task directories')
    parser.add_argument('--preview', action='store_true', help='Preview without saving')
    
    args = parser.parse_args()
    
    # Initialize synthesis tool
    synthesizer = SquadSynthesis(args.workspace)
    
    if args.list_dirs:
        print("Completed task directories found:")
        if synthesizer.completed_dirs:
            for i, dir_path in enumerate(synthesizer.completed_dirs, 1):
                print(f"{i}. {dir_path}")
        else:
            print("No completed task directories found")
        return 0
    
    # Parse target date (for non-aggregate mode)
    target_date = None
    if not args.aggregate:
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD")
            return 1
    
    # Setup filtering
    domain_filter = None
    if args.domain:
        domain_mapping = {
            'ai-ml': 'AI/ML',
            'biopharma': 'Biopharma', 
            'competitive-intel': 'Competitive Intel',
            'general': 'General'
        }
        domain_filter = domain_mapping.get(args.domain.lower(), args.domain)
    
    # Collect findings
    if args.aggregate:
        print(f"Collecting findings from last {args.aggregate} days...")
        findings = synthesizer.collect_findings(domain_filter=domain_filter, days_back=args.aggregate)
    else:
        print(f"Collecting findings for {target_date.strftime('%Y-%m-%d')}...")
        findings = synthesizer.collect_findings(target_date=target_date, domain_filter=domain_filter)
    
    if not findings:
        print("No completed tasks found matching the specified criteria.")
        return 0
    
    print(f"Found {len(findings)} completed tasks.")
    
    # Generate report
    if args.aggregate:
        print("Generating aggregate summary...")
        summary = synthesizer.generate_aggregate_summary(findings, args.aggregate)
        filename = f"aggregate-{args.aggregate}days-{datetime.now().strftime('%Y-%m-%d')}.md"
    else:
        print("Generating daily summary...")
        summary = synthesizer.generate_daily_summary(findings, target_date)
        filename = f"{target_date.strftime('%Y-%m-%d')}.md"
    
    # Output
    if args.preview:
        print("\n" + "="*60)
        if args.aggregate:
            print(f"PREVIEW - Aggregate Summary (Last {args.aggregate} days)")
        else:
            print("PREVIEW - Daily Summary Report")
        print("="*60)
        print(summary[:1000] + "..." if len(summary) > 1000 else summary)
        print("="*60)
    else:
        file_path = synthesizer.save_report(summary, filename, args.output_dir)
        if file_path:
            print(f"Report saved to: {file_path}")
        else:
            print("Error: Failed to save report")
            return 1
        
        # Print brief stats
        stats = synthesizer.calculate_summary_stats(findings)
        print(f"\nSummary Statistics:")
        print(f"- Total tasks: {stats['total_tasks']}")
        print(f"- Domains covered: {', '.join(stats['domains'].keys())}")
        print(f"- Agents active: {', '.join(stats['agents'].keys())}")
    
    return 0

if __name__ == "__main__":
    exit(main())