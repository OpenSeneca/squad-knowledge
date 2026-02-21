# GitHub Issue Analyzer

A CLI tool to analyze GitHub issues across repositories. Categorizes by label, status, assignee, and identifies patterns.

## Why This Matters

The OpenSeneca org has multiple repositories and multiple contributors. Issue management across repos is important for:

- Tracking open vs closed issues
- Identifying stale or complex issues
- Understanding label usage
- Seeing assignee distribution
- Monitoring issue velocity

This tool provides quick insights without visiting each repo separately.

## Installation

```bash
cd ~/.openclaw/workspace/tools/gh-issue-analyzer
chmod +x gh-issue-analyzer
ln -sf $(pwd)/gh-issue-analyzer ~/.local/bin/gh-issue-analyzer
```

## Prerequisites

Requires `gh` CLI installed and authenticated:

```bash
gh auth login
```

## Usage

### Analyze Issues

```bash
# Analyze single repository
gh-issue-analyzer analyze --owner OpenSeneca --repo squad-overview

# Analyze all repositories for owner
gh-issue-analyzer analyze --owner OpenSeneca --all

# Show detailed issue lists in analysis
gh-issue-analyzer analyze --owner OpenSeneca --all --show-issues

# Include closed issues
gh-issue-analyzer analyze --owner OpenSeneca --all --state all
```

Output:
```
🔍 GitHub Issue Analyzer
   Analyze issues across repositories

📊 Issue Analysis

Total: 15 issues

📈 By Status:
   open: 12
   closed: 3

🏷️  By Label (top 10):
   bug: 5
   enhancement: 4
   question: 3
   documentation: 2
   unlabeled: 1

👤 By Assignee:
   archimedes: 6
   unassigned: 5
   marcus: 2
   galen: 2

💡 Insights:
   ⚠️ 3 stale issues (>30 days, no comments)
   💬 2 complex issues (10+ comments)
   🆕 4 recent issues (last 7 days)
   📊 10/15 issues assigned (66.7%)
   🏷️  14/15 issues labeled (93.3%)
```

### List Issues

```bash
# List issues from single repository
gh-issue-analyzer list --owner OpenSeneca --repo squad-overview

# List all issues for owner
gh-issue-analyzer list --owner OpenSeneca --all

# List only closed issues
gh-issue-analyzer list --owner OpenSeneca --all --state closed
```

Output:
```
📋 Issues (12):

1. #23: Add export to CSV feature
   Status: open
   Assignee: archimedes
   Labels: enhancement
   Comments: 3
   URL: https://github.com/OpenSeneca/squad-overview/issues/23

2. #22: Fix JSON parsing error
   Status: open
   Assignee: unassigned
   Labels: bug
   Comments: 1
   URL: https://github.com/OpenSeneca/squad-overview/issues/22
```

## Options

### analyze
| Option | Description |
|--------|-------------|
| `--owner OWNER` | Repository owner (required) |
| `--repo REPO` | Specific repository (use with `--all` or separately) |
| `--all` | Analyze all repositories for owner |
| `--state STATE` | Issue state: open, closed, all (default: open) |
| `--show-issues` | Show detailed issue lists in analysis |

### list
| Option | Description |
|--------|-------------|
| `--owner OWNER` | Repository owner (required) |
| `--repo REPO` | Specific repository (use with `--all` or separately) |
| `--all` | List all repositories for owner |
| `--state STATE` | Issue state: open, closed, all (default: open) |

## Analysis Metrics

The tool calculates several metrics:

### By Status
- open: Currently open issues
- closed: Resolved issues

### By Label
- Top 10 most used labels
- Count of unlabeled issues

### By Assignee
- Issues per assignee
- Count of unassigned issues
- Assignment rate percentage

### By Repository
- Issues per repository (when using `--all`)

### Insights

**Stale Issues**: Older than 30 days with no comments
- Indicates issues that may need attention or cleanup

**Complex Issues**: 10 or more comments
- Indicates discussion-heavy issues that might need breaking down

**Recent Issues**: Created in the last 7 days
- Shows issue velocity and recent activity

**Assignment Rate**: Percentage of issues with assignees
- Indicates how well issues are being triaged

**Label Coverage**: Percentage of issues with labels
- Indicates how well issues are categorized

## Examples

### Monitor OpenSeneca Org Activity

```bash
# Quick health check
gh-issue-analyzer analyze --owner OpenSeneca --all

# Detailed view with issues
gh-issue-analyzer analyze --owner OpenSeneca --all --show-issues

# Check for stale issues
gh-issue-analyzer analyze --owner OpenSeneca --all --show-issues | grep "stale"
```

### Review Specific Repository

```bash
# Analyze squad-overview repo
gh-issue-analyzer analyze --owner OpenSeneca --repo squad-overview

# List all issues
gh-issue-analyzer list --owner OpenSeneca --repo squad-overview

# Check closed issues
gh-issue-analyzer analyze --owner OpenSeneca --repo squad-overview --state closed
```

### Track Issue Velocity

```bash
# Weekly check - compare recent vs total
gh-issue-analyzer analyze --owner OpenSeneca --all --show-issues

# Look at the "recent issues" count
# Compare with total to gauge velocity
```

## Integration with GitHub

Uses the `gh` CLI for all GitHub operations. This means:

- No API keys needed (uses gh auth)
- Works with all gh features (search, filters)
- Respects gh configuration (default host, tokens, etc.)

## For the Squad

**Justin**: Use this to monitor OpenSeneca org health, identify stale issues, and understand team workload.

**Archimedes**: Use this to review tool repositories, prioritize issues, and track progress.

**Seneca**: Use this to identify blockers and high-priority issues across repos.

## Notes

- Requires gh CLI to be installed and authenticated
- Uses `gh issue list` with JSON output
- Supports both individual repositories and all repos for an owner
- State filter: open, closed, or all

## License

MIT
