#!/usr/bin/env python3
"""
Squad Briefing Generator
Formats daily briefings for email and Telegram from structured input.
"""

import json
import argparse
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import textwrap

@dataclass
class SquadBriefing:
    """Structured briefing data model"""
    date: str
    executive_summary: str
    domain_findings: List[Dict[str, Any]]
    squad_activity: List[Dict[str, Any]]
    queue_status: List[Dict[str, Any]]
    key_metrics: Dict[str, Any]
    priority_actions: List[str]

class BriefingGenerator:
    def __init__(self):
        """Initialize the briefing generator"""
        self.email_template = self._load_email_template()
        self.telegram_template = self._load_telegram_template()
    
    def _load_email_template(self) -> str:
        """Load email template"""
        return """# Squad Daily Briefing

**Date**: {date}
**Generated**: {timestamp}

## Executive Summary

{executive_summary}

## Key Findings by Domain

{domain_findings}

## Squad Activity Update

{squad_activity}

## Queue Status & Priorities

{queue_status}

## Key Metrics

{key_metrics}

## Priority Actions for Today

{priority_actions}

---
*Squad Daily Briefing System*
"""

    def _load_telegram_template(self) -> str:
        """Load Telegram template"""
        return """{executive_summary}

Key updates: {highlights}

Priority actions: {priority_count} items

Full briefing available in dashboard."""
    
    def load_from_json(self, json_file: str) -> SquadBriefing:
        """Load briefing data from JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return SquadBriefing(**data)
        except Exception as e:
            print(f"Error loading JSON file {json_file}: {e}")
            return None
    
    def load_from_dict(self, data: Dict) -> SquadBriefing:
        """Load briefing data from dictionary"""
        try:
            return SquadBriefing(**data)
        except Exception as e:
            print(f"Error loading briefing data: {e}")
            return None
    
    def generate_email_format(self, briefing: SquadBriefing) -> str:
        """Generate email format briefing"""
        # Format domain findings
        domain_text = ""
        for domain in briefing.domain_findings:
            domain_text += f"### {domain['name']}\n\n"
            
            for finding in domain.get('findings', []):
                domain_text += f"• **{finding['title']}**\n"
                domain_text += f"  {finding['description']}\n"
                if finding.get('source'):
                    domain_text += f"  *Source: {finding['source']}*\n"
                domain_text += "\n"
        
        # Format squad activity
        activity_text = ""
        for activity in briefing.squad_activity:
            status_emoji = "✅" if activity['status'] == 'completed' else "🔄" if activity['status'] == 'in_progress' else "⏳"
            activity_text += f"• {status_emoji} **{activity['agent']}**: {activity['task']} ({activity['status']})\n"
            if activity.get('details'):
                activity_text += f"  {activity['details']}\n"
            activity_text += "\n"
        
        # Format queue status
        queue_text = ""
        if briefing.queue_status:
            for queue_item in briefing.queue_status:
                priority_emoji = "🔥" if queue_item['priority'] == 'high' else "⚡" if queue_item['priority'] == 'medium' else "📋"
                queue_text += f"• {priority_emoji} **{queue_item['task']}** ({queue_item['priority']} priority)\n"
                queue_text += f"  Assigned to: {queue_item['assigned_to']} | ETA: {queue_item.get('eta', 'TBD')}\n"
                if queue_item.get('blockers'):
                    queue_text += f"  *Blockers: {queue_item['blockers']}*\n"
                queue_text += "\n"
        else:
            queue_text = "• Queue is clear for new priorities\n\n"
        
        # Format key metrics
        metrics_text = ""
        for metric, value in briefing.key_metrics.items():
            metrics_text += f"• **{metric}**: {value}\n"
        
        # Format priority actions
        actions_text = ""
        for i, action in enumerate(briefing.priority_actions, 1):
            actions_text += f"{i}. {action}\n"
        
        return self.email_template.format(
            date=briefing.date,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            executive_summary=briefing.executive_summary,
            domain_findings=domain_text,
            squad_activity=activity_text,
            queue_status=queue_text,
            key_metrics=metrics_text,
            priority_actions=actions_text
        )
    
    def generate_telegram_format(self, briefing: SquadBriefing) -> str:
        """Generate Telegram format briefing (plain text, 2-3 sentences)"""
        # Extract key highlights
        highlights = []
        
        # Get top domain findings
        for domain in briefing.domain_findings[:2]:  # Top 2 domains
            top_finding = domain.get('findings', [{}])[0] if domain.get('findings') else {}
            if top_finding.get('title'):
                highlights.append(f"{domain['name']}: {top_finding['title']}")
        
        # Get top squad activity
        completed_count = sum(1 for a in briefing.squad_activity if a['status'] == 'completed')
        in_progress_count = sum(1 for a in briefing.squad_activity if a['status'] == 'in_progress')
        
        if completed_count > 0:
            highlights.append(f"{completed_count} tasks completed")
        if in_progress_count > 0:
            highlights.append(f"{in_progress_count} in progress")
        
        # Get high priority queue items
        high_priority = len([q for q in briefing.queue_status if q['priority'] == 'high'])
        if high_priority > 0:
            highlights.append(f"{high_priority} high-priority items")
        
        highlights_text = ", ".join(highlights[:3])  # Top 3 highlights
        
        return self.telegram_template.format(
            executive_summary=briefing.executive_summary,
            highlights=highlights_text,
            priority_count=len(briefing.priority_actions)
        )
    
    def save_to_file(self, content: str, filename: str) -> str:
        """Save content to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return filename
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return None

def create_sample_data() -> Dict:
    """Create sample briefing data for testing"""
    return {
        "date": "2026-02-08",
        "executive_summary": "Squad completed MARL environment template system with 40% research velocity increase. AI/ML research showing strong results, biopharma analysis pending final review.",
        "domain_findings": [
            {
                "name": "AI/ML",
                "findings": [
                    {
                        "title": "MARL Environment Templates Deployed",
                        "description": "Template system for rapid environment generation reduced setup time from hours to minutes. Integration testing shows 98% code coverage.",
                        "source": "BUILD-001 completion report"
                    },
                    {
                        "title": "Training Pipeline Optimization",
                        "description": "New scheduling algorithm reduced training time by 25% across multiple experiments.",
                        "source": "Marcus research notes"
                    }
                ]
            },
            {
                "name": "Biopharma",
                "findings": [
                    {
                        "title": "Protein Folding Analysis Progress",
                        "description": "Initial results show 15% improvement in prediction accuracy over baseline models.",
                        "source": "Galen preliminary data"
                    }
                ]
            }
        ],
        "squad_activity": [
            {
                "agent": "Archimedes",
                "task": "MARL Environment Template System",
                "status": "completed",
                "details": "Build completed with 95% quality score, deployed to production"
            },
            {
                "agent": "Marcus", 
                "task": "Training Pipeline Analysis",
                "status": "in_progress",
                "details": "80% complete, expecting results tomorrow"
            },
            {
                "agent": "Galen",
                "task": "Biopharma Data Processing",
                "status": "in_progress", 
                "details": "Waiting on final dataset from research partner"
            }
        ],
        "queue_status": [
            {
                "task": "Competitive Intelligence Dashboard",
                "priority": "high",
                "assigned_to": "Argus",
                "eta": "2026-02-09",
                "blockers": "API access pending"
            },
            {
                "task": "Market Analysis Report",
                "priority": "medium",
                "assigned_to": "Marcus",
                "eta": "2026-02-10",
                "blockers": None
            }
        ],
        "key_metrics": {
            "Tasks Completed": 1,
            "Tasks In Progress": 2,
            "High Priority Items": 1,
            "Research Velocity": "+40%",
            "Quality Score": "95/100"
        },
        "priority_actions": [
            "Resolve API access for Competitive Intelligence Dashboard",
            "Complete Training Pipeline analysis by EOD",
            "Review and finalize Biopharma data processing workflow"
        ]
    }

def main():
    parser = argparse.ArgumentParser(description='Squad Briefing Generator')
    parser.add_argument('--input', '-i', type=str, help='Input JSON file path')
    parser.add_argument('--email', '-e', action='store_true', help='Generate email format')
    parser.add_argument('--telegram', '-t', action='store_true', help='Generate Telegram format')
    parser.add_argument('--both', '-b', action='store_true', help='Generate both formats')
    parser.add_argument('--output-email', type=str, help='Save email to file')
    parser.add_argument('--output-telegram', type=str, help='Save Telegram to file')
    parser.add_argument('--sample', action='store_true', help='Use sample data for testing')
    parser.add_argument('--stdout', action='store_true', help='Output to stdout')
    
    args = parser.parse_args()
    
    # Default to both formats if no specific format requested
    if not any([args.email, args.telegram, args.both]):
        args.both = True
    
    # Load briefing data
    if args.sample:
        print("Using sample data...")
        data = create_sample_data()
        briefing = BriefingGenerator().load_from_dict(data)
    elif args.input:
        print(f"Loading briefing data from {args.input}...")
        generator = BriefingGenerator()
        briefing = generator.load_from_json(args.input)
    else:
        print("Error: Please provide input file with --input or use --sample for testing")
        return 1
    
    if not briefing:
        print("Error: Failed to load briefing data")
        return 1
    
    generator = BriefingGenerator()
    
    # Generate formats
    results = {}
    
    if args.email or args.both:
        email_content = generator.generate_email_format(briefing)
        results['email'] = email_content
        print(f"✓ Email format generated ({len(email_content)} characters)")
    
    if args.telegram or args.both:
        telegram_content = generator.generate_telegram_format(briefing)
        results['telegram'] = telegram_content
        print(f"✓ Telegram format generated ({len(telegram_content)} characters)")
    
    # Save or output results
    if args.stdout:
        print("\n" + "="*60)
        if 'email' in results:
            print("EMAIL FORMAT:")
            print("="*60)
            print(results['email'])
            print("\n" + "="*60)
        if 'telegram' in results:
            print("TELEGRAM FORMAT:")
            print("="*60)
            print(results['telegram'])
            print("="*60)
    
    # Save to files if requested
    if args.output_email and 'email' in results:
        saved_file = generator.save_to_file(results['email'], args.output_email)
        if saved_file:
            print(f"✓ Email saved to {saved_file}")
    
    if args.output_telegram and 'telegram' in results:
        saved_file = generator.save_to_file(results['telegram'], args.output_telegram)
        if saved_file:
            print(f"✓ Telegram saved to {saved_file}")
    
    # Default file saving if no output specified and not stdout
    if not args.stdout and not args.output_email and not args.output_telegram:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if 'email' in results:
            email_file = f"briefing_email_{timestamp}.md"
            generator.save_to_file(results['email'], email_file)
            print(f"✓ Email saved to {email_file}")
        
        if 'telegram' in results:
            telegram_file = f"briefing_telegram_{timestamp}.txt"
            generator.save_to_file(results['telegram'], telegram_file)
            print(f"✓ Telegram saved to {telegram_file}")
    
    return 0

if __name__ == "__main__":
    exit(main())