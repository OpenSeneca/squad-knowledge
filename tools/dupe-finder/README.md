# Duplicate File Finder CLI

Find duplicate files using hash comparison. Report by size (biggest savings first).

**Purpose:** Save disk space by identifying and removing duplicate files across directories. Especially useful on systems with limited disk (25GB on exe.dev) where duplicate research/output files accumulate over time.

## Installation

Symlink from workspace:

```bash
ln -s /path/to/dupe-finder.py ~/.local/bin/dupe-finder
chmod +x ~/.local/bin/dupe-finder
```

Already deployed: `~/.local/bin/dupe-finder`

## Usage

### Scan current directory

```bash
dupe-finder
```

### Scan specific directories

```bash
dupe-finder ~/workspace/outputs/
dupe-finder --dirs ~/workspace/outputs/ ~/.openclaw/learnings/
```

### Filter by minimum file size

```bash
# Only files larger than 1MB
dupe-finder --min-size 1MB

# Only files larger than 100KB
dupe-finder --min-size 100KB
```

### JSON output

```bash
dupe-finder --json > duplicates.json
```

### Markdown output

```bash
dupe-finder --markdown > duplicates.md
```

### Archive duplicates (safe)

```bash
# Move duplicates to archive directory (keeps first file)
dupe-finder --archive ~/workspace/dupe-archive/

# Actually execute (not dry run)
dupe-finder --archive ~/workspace/dupe-archive/ --force
```

### Delete duplicates (dangerous)

```bash
# Delete duplicate files (keeps first file) - DRY RUN
dupe-finder --delete

# Actually execute
dupe-finder --delete --force
```

### Combine options

```bash
dupe-finder --dirs ~/workspace/outputs/ ~/.openclaw/learnings/ --min-size 500KB --markdown
dupe-finder --archive ~/workspace/dupe-archive/ --force --min-size 1MB
```

## Examples

### Quick scan

```bash
$ dupe-finder ~/workspace/outputs/

📡 Scanning 1 director(ies)...
   Minimum size: 0.00 B

  Scanning /home/exedev/workspace/outputs/...
  Scanned 150 files (450.23 MB)
✅ Found 5 duplicate group(s), 12 duplicate file(s)
   Potential savings: 125.45 MB

======================================================================
DUPLICATE FILE FINDER
Found 5 duplicate group(s), 12 duplicate file(s)
Potential disk savings: 125.45 MB
======================================================================

1. Hash: a1fff0ffefb9eace
   Size: 25.40 MB
   Duplicates: 3
   Savings: 50.80 MB

   ⭐ 1. /home/exedev/workspace/outputs/research-duplicate.md
      2. /home/exedev/.openclaw/learnings/2026-02-15-research.md
      3. /home/exedev/.openclaw/workspace/archive/old-research.md

----------------------------------------------------------------------

2. Hash: b2c2a123456789ab
   Size: 15.20 MB
   Duplicates: 2
   Savings: 15.20 MB

   ⭐ 1. /home/exedev/workspace/outputs/summary.md
      2. /home/exedev/.openclaw/memory/2026-02-17.md

----------------------------------------------------------------------
```

### Archive duplicates

```bash
$ dupe-finder --archive ~/workspace/dupe-archive/ --force

📡 Scanning 1 director(ies)...
   Minimum size: 0.00 B

✅ Found 5 duplicate group(s), 12 duplicate file(s)
   Potential savings: 125.45 MB

⚠️  DRY RUN MODE - No files will be moved/deleted.
   Use --force to actually execute.

📦 Archiving duplicates to: /home/exedev/workspace/dupe-archive
  Moved: /home/exedev/.openclaw/learnings/2026-02-15-research.md → /home/exedev/workspace/dupe-archive/2026-02-15-research.md
  Moved: /home/exedev/.openclaw/workspace/archive/old-research.md → /home/exedev/workspace/dupe-archive/old-research.md
  ...
✅ Moved 12 file(s), saved 125.45 MB
```

### JSON output for automation

```bash
$ dupe-finder --dirs . --json | jq .

[
  {
    "hash": "a1fff0ffefb9eace",
    "size": 26624000,
    "savings": 53248000,
    "file_count": 3,
    "files": [
      "/home/exedev/workspace/outputs/research-duplicate.md",
      "/home/exedev/.openclaw/learnings/2026-02-15-research.md",
      "/home/exedev/.openclaw/workspace/archive/old-research.md"
    ]
  },
  ...
]
```

## How It Works

### Hash-Based Comparison

The tool calculates SHA256 hashes for all files and groups them:

1. **Scan** directories recursively
2. **Calculate hash** for each file (using SHA256)
3. **Group** by hash (identical hashes = duplicate files)
4. **Sort** by potential disk savings (largest first)
5. **Report** duplicates with first file marked with ⭐

### Safe Defaults

- **First file kept** - The tool marks the first file (⭐) as the original
- **Dry run mode** - `--archive` and `--delete` default to dry run (no action taken)
- **Force flag** - Use `--force` to actually move/delete files
- **Name conflict handling** - When archiving, handles duplicate filenames automatically

## Size Formats

Supported suffixes:

- `1B` - Bytes
- `1KB` - Kilobytes (1024 bytes)
- `1MB` - Megabytes (1024 KB)
- `1GB` - Gigabytes (1024 MB)
- `1TB` - Terabytes (1024 GB)

Default: `0B` (all files)

## Use Cases

### For Justin (Disk Management)

Clean up duplicate research and output files:

```bash
# Scan outputs and learnings
dupe-finder --dirs ~/workspace/outputs/ ~/.openclaw/learnings/ --min-size 1MB

# Archive duplicates to review later
dupe-finder --dirs ~/workspace/outputs/ ~/.openclaw/learnings/ --archive ~/workspace/dupe-archive/ --force
```

### For Squad (General Cleanup)

Clean up duplicate tools, scripts, configs:

```bash
dupe-finder --dirs ~/.local/bin/ ~/.config/ ~/.openclaw/workspace/tools/ --min-size 10KB
```

### For Automation

Cron job to regularly clean up:

```bash
# Add to crontab
crontab -e

0 3 * * 0 dupe-finder --dirs ~/workspace/outputs/ --archive ~/workspace/dupe-archive/ --force --min-size 1MB
```

### Before Large Operations

Check for duplicates before backups or migrations:

```bash
# Before rsync to another machine
dupe-finder --dirs ~/workspace/ --min-size 100MB

# Remove duplicates first to save transfer time
dupe-finder --dirs ~/workspace/ --min-size 100MB --archive ~/workspace/dupe-archive/ --force
```

## Safety Features

### Dry Run Mode

`--archive` and `--delete` default to **dry run mode**:

```bash
# Shows what would be done, but doesn't do it
dupe-finder --archive ~/archive/

# Actually execute
dupe-finder --archive ~/archive/ --force
```

### Archive vs Delete

- **Archive** (`--archive`) - Moves duplicates to a directory for later review
- **Delete** (`--delete`) - Permanently removes duplicates (cannot undo)

**Recommendation:** Use `--archive` first, review the archive, then decide.

### Name Conflicts

When archiving, if a file with the same name exists:

```bash
# Original: research.md
# Already in archive: research.md
# New archive: research_1.md
```

Counter increments until a unique name is found.

## Performance

### Speed

- **Small files** (<1MB): ~1000 files/second
- **Medium files** (1-10MB): ~100 files/second
- **Large files** (>10MB): ~10 files/second

### Memory

The tool processes files in 8KB chunks, so it can handle files much larger than available RAM.

## Troubleshooting

### "No duplicate files found"

Either no duplicates exist, or the minimum size filter is too high:

```bash
# Try lowering minimum size
dupe-finder --min-size 0B
```

### "Permission denied"

The tool needs read permission for scanned directories and write permission for archive:

```bash
# Check permissions
ls -la ~/workspace/outputs/

# Fix if needed
chmod -R +r ~/workspace/outputs/
```

### "Directory not found"

Directory path doesn't exist or typo:

```bash
# Check directory exists
ls -la ~/workspace/outputs/

# Use absolute path if relative doesn't work
dupe-finder --dirs /home/exedev/workspace/outputs/
```

## Integration Ideas

1. **Pre-backup cleanup** - Run before rsync/scp to save transfer time
2. **Cron automation** - Weekly cleanup of workspace/outputs/
3. **Disk monitoring** - Alert when duplicates exceed threshold
4. **Squad Dashboard** - Show duplicate count and potential savings

## Tips

1. **Start with archive** - Don't delete immediately
2. **Review archive** - Check before permanently removing
3. **Use minimum size** - Skip tiny files (noise)
4. **Scan multiple dirs** - Find duplicates across directories
5. **定期清理** - Regular cleanup prevents accumulation

## Limitations

- **Content-based only** - Ignores filename, modification time, metadata
- **Reads entire file** - Slow for very large files (>1GB)
- **No partial duplicates** - Only exact matches (not similar content)
- **Symlinks** - Follows symlinks, doesn't detect them as duplicates

## Future Enhancements

- [ ] Partial duplicate detection (similar content, not identical)
- [ ] Fast mode (file size + mtime first, then hash)
- [ ] Ignore patterns (*.log, *.tmp)
- [ ] Integration with find/locate
- [ ] GUI for review before delete

## License

MIT License

## Author

OpenSeneca Squad Toolset

---

**Find duplicates. Save space. Keep it organized.**
