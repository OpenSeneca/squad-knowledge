# Squad Tools - Archimedes

This directory contains utility scripts for maintaining squad operations and output quality.

## Available Tools

### output-counter.py
**Purpose:** Count outputs per agent per day
**Usage:** `python3 output-counter.py`
**Output:** Lists output counts by agent and date, plus totals

### format-checker.py
**Purpose:** Verify output format compliance
**Usage:** `python3 format-checker.py`
**Checks:** 
- Presence of "## Key Findings" section with bullet points
- Presence of "## Sources" section with markdown links
**Output:** Compliance rate and detailed issues if found

## Installation

All scripts are executable and ready to use from:
`~/.openclaw/workspace/tools/`

## Maintenance

- Scripts are designed to be simple and reliable
- They work with the standard output directory structure
- Error handling includes informative messages
- No external dependencies beyond Python 3.x

## Output Directory Structure

Expected format: `YYYY-MM-DD-<agent>-<topic>.md`
- Date format: YYYY-MM-DD
- Agent: optional, extracted from filename
- Topic: descriptive title slug