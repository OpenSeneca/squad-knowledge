#!/usr/bin/env python3
"""
AZ Competitor AI Announcement Database

Maintains a JSON database of competitor AI announcements relevant to AstraZeneca.
Provides add, query, and reporting functionality for tracking competitive intelligence.

Commands:
    competitor-tracker add --company "Roche" --action "Launched AI drug discovery platform" --source "URL" --implication "Competes with AZ's internal platform"
    competitor-tracker query --company "Roche" --days 30
    competitor-tracker report --days 7

Data stored in: ~/.openclaw/workspace/data/competitors.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_data_path():
    """Get the path to the competitors JSON database."""
    data_dir = os.path.expanduser('~/.openclaw/workspace/data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'competitors.json')


def load_database():
    """Load the competitor database from JSON file."""
    data_path = get_data_path()
    
    if os.path.exists(data_path):
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load database: {e}", file=sys.stderr)
    
    # Return empty database structure
    return {
        'metadata': {
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'version': '1.0',
            'total_announcements': 0
        },
        'announcements': []
    }


def save_database(database):
    """Save the competitor database to JSON file."""
    data_path = get_data_path()
    
    # Update metadata
    database['metadata']['last_updated'] = datetime.now().isoformat()
    database['metadata']['total_announcements'] = len(database['announcements'])
    
    try:
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error: Could not save database: {e}", file=sys.stderr)
        return False


def add_announcement(company, action, source, implication, category=None, priority='medium'):
    """Add a new competitor announcement to the database."""
    database = load_database()
    
    announcement = {
        'id': len(database['announcements']) + 1,
        'date_added': datetime.now().isoformat(),
        'company': company.strip(),
        'action': action.strip(),
        'source': source.strip(),
        'implication': implication.strip(),
        'category': category or 'general',
        'priority': priority.lower(),
        'status': 'active'
    }
    
    database['announcements'].append(announcement)
    
    if save_database(database):
        print(f"✓ Added announcement for {company}: {action}")
        return True
    else:
        print("✗ Failed to add announcement", file=sys.stderr)
        return False


def query_announcements(company=None, days=None, category=None, priority=None):
    """Query announcements with optional filters."""
    database = load_database()
    announcements = database['announcements']
    
    # Apply filters
    if company:
        announcements = [a for a in announcements if company.lower() in a['company'].lower()]
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        announcements = [a for a in announcements 
                        if datetime.fromisoformat(a['date_added']) >= cutoff_date]
    
    if category:
        announcements = [a for a in announcements if category.lower() == a['category'].lower()]
    
    if priority:
        announcements = [a for a in announcements if priority.lower() == a['priority'].lower()]
    
    # Sort by date (most recent first)
    announcements.sort(key=lambda x: x['date_added'], reverse=True)
    
    return announcements


def format_announcement(announcement):
    """Format a single announcement for display."""
    lines = []
    lines.append(f"📢 {announcement['company']}")
    lines.append(f"📅 {announcement['date_added'][:10]}")
    lines.append(f"🔸 {announcement['action']}")
    lines.append(f"💡 AZ Implication: {announcement['implication']}")
    lines.append(f"📎 Source: {announcement['source']}")
    lines.append(f"🏷️  Category: {announcement['category']} | Priority: {announcement['priority']}")
    return '\n'.join(lines)


def generate_report(days=7):
    """Generate a summary report of recent competitor activity."""
    database = load_database()
    all_announcements = database['announcements']
    
    # Filter for recent announcements
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_announcements = [a for a in all_announcements 
                           if datetime.fromisoformat(a['date_added']) >= cutoff_date]
    
    report = []
    report.append(f"# Competitive Intelligence Report")
    report.append(f"**Period:** Past {days} days")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    # Summary statistics
    report.append("## Summary")
    report.append(f"- Total announcements: {len(recent_announcements)}")
    
    if recent_announcements:
        # Company breakdown
        companies = {}
        for a in recent_announcements:
            companies[a['company']] = companies.get(a['company'], 0) + 1
        
        report.append("- Companies tracked:")
        for company, count in sorted(companies.items()):
            report.append(f"  - {company}: {count} announcements")
        
        # Priority breakdown
        priorities = {}
        for a in recent_announcements:
            priorities[a['priority']] = priorities.get(a['priority'], 0) + 1
        
        report.append("- Priority distribution:")
        for priority, count in sorted(priorities.items()):
            report.append(f"  - {priority}: {count}")
    
    report.append("")
    
    # Key insights
    report.append("## Key Insights")
    if recent_announcements:
        # High priority items
        high_priority = [a for a in recent_announcements if a['priority'] == 'high']
        if high_priority:
            report.append(f"⚠️  **{len(high_priority)} high-priority announcements** require immediate attention:")
            for a in high_priority[:3]:  # Top 3 high priority
                report.append(f"  - {a['company']}: {a['action']}")
            report.append("")
        
        # Most active companies
        if len(companies) > 1:
            most_active = max(companies.items(), key=lambda x: x[1])
            report.append(f"📈 **Most active competitor:** {most_active[0]} ({most_active[1]} announcements)")
            report.append("")
        
        # Common themes
        categories = {}
        for a in recent_announcements:
            categories[a['category']] = categories.get(a['category'], 0) + 1
        
        if categories:
            common_theme = max(categories.items(), key=lambda x: x[1])
            report.append(f"🎯 **Common theme:** {common_theme[0]} ({common_theme[1]} announcements)")
    else:
        report.append("- No competitive activity tracked in this period")
        report.append("- Consider reviewing recent industry news for updates")
    
    report.append("")
    
    # Detailed announcements
    report.append("## Detailed Announcements")
    if recent_announcements:
        # Sort by priority and date
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recent_announcements.sort(key=lambda x: (priority_order.get(x['priority'], 3), x['date_added']), reverse=True)
        
        for i, announcement in enumerate(recent_announcements, 1):
            report.append(f"### {i}. {announcement['company']}")
            report.append(f"**Date:** {announcement['date_added'][:10]}")
            report.append(f"**Action:** {announcement['action']}")
            report.append(f"**AZ Implication:** {announcement['implication']}")
            report.append(f"**Source:** {announcement['source']}")
            report.append(f"**Category:** {announcement['category']} | **Priority:** {announcement['priority']}")
            report.append("")
    else:
        report.append("No announcements to display")
    
    return '\n'.join(report)


def list_companies():
    """List all companies in the database."""
    database = load_database()
    companies = set()
    
    for announcement in database['announcements']:
        companies.add(announcement['company'])
    
    return sorted(list(companies))


def main():
    parser = argparse.ArgumentParser(
        description='AZ Competitor AI Announcement Database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    competitor-tracker add --company "Roche" --action "Launched AI drug discovery platform" --source "URL" --implication "Competes with AZ's internal platform"
    competitor-tracker query --company "Roche" --days 30
    competitor-tracker report --days 7
    competitor-tracker list
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new announcement')
    add_parser.add_argument('--company', required=True, help='Competitor company name')
    add_parser.add_argument('--action', required=True, help='Action or announcement details')
    add_parser.add_argument('--source', required=True, help='Source URL or reference')
    add_parser.add_argument('--implication', required=True, help='AZ business implication')
    add_parser.add_argument('--category', help='Category (default: general)')
    add_parser.add_argument('--priority', choices=['high', 'medium', 'low'], default='medium',
                          help='Priority level (default: medium)')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query announcements')
    query_parser.add_argument('--company', help='Filter by company name')
    query_parser.add_argument('--days', type=int, help='Filter by recent days')
    query_parser.add_argument('--category', help='Filter by category')
    query_parser.add_argument('--priority', choices=['high', 'medium', 'low'], help='Filter by priority')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate summary report')
    report_parser.add_argument('--days', type=int, default=7, help='Days to include (default: 7)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all companies')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'add':
        success = add_announcement(
            args.company, args.action, args.source, 
            args.implication, args.category, args.priority
        )
        sys.exit(0 if success else 1)
    
    elif args.command == 'query':
        announcements = query_announcements(
            args.company, args.days, args.category, args.priority
        )
        
        if announcements:
            print(f"Found {len(announcements)} announcements:")
            print()
            for i, announcement in enumerate(announcements, 1):
                print(f"{i}. {format_announcement(announcement)}")
                print()
        else:
            print("No announcements found matching the criteria")
    
    elif args.command == 'report':
        report = generate_report(args.days)
        print(report)
    
    elif args.command == 'list':
        companies = list_companies()
        if companies:
            print("Companies tracked:")
            for company in companies:
                print(f"  - {company}")
        else:
            print("No companies in database")


if __name__ == '__main__':
    main()