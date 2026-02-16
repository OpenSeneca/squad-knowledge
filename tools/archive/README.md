# archive — Archive and Compression Tool

Compress and extract archives (zip, tar.gz, tar.bz2, tar.xz). Simple archiving without external tools.

**Location:** `~/workspace/tools/archive/`

**Install:** Symlink to `~/.local/bin/archive`

```bash
ln -s ~/workspace/tools/archive/archive.py ~/.local/bin/archive
chmod +x ~/workspace/tools/archive/archive.py
```

## Features

- **Create Archives** — ZIP, TAR, TAR.GZ, TAR.BZ2, TAR.XZ
- **Extract Archives** — Extract any supported format
- **List Contents** — View archive contents
- **Archive Info** — Show archive statistics
- **No Dependencies** — Pure Python, no tar/zip required

## Key Commands

### Create Archives

- `archive create <source>` — Create archive (ZIP by default)
- `archive create <source> -o <output>` — Specify output path
- `archive create <source> -f <format>` — Specify format

### Extract Archives

- `archive extract <archive>` — Extract archive
- `archive extract <archive> -o <output>` — Extract to specific path

### List and Info

- `archive list <archive>` — List archive contents
- `archive info <archive>` — Show archive information

### Formats

- `zip` — ZIP archive (default)
- `tar` — TAR archive (uncompressed)
- `tar.gz` — TAR.GZ archive (gzip compressed)
- `tar.bz2` — TAR.BZ2 archive (bzip2 compressed)
- `tar.xz` — TAR.XZ archive (xz compressed)

## Examples

### Create ZIP Archive

```bash
# Archive single file
archive create file.txt

# Archive directory
archive create myproject/

# Specify output name
archive create myproject/ -o project-backup.zip
```

### Create TAR Archive

```bash
# Create TAR.GZ
archive create myproject/ -f tar.gz

# Create TAR.BZ2
archive create myproject/ -f tar.bz2

# Create TAR.XZ
archive create myproject/ -f tar.xz

# Create uncompressed TAR
archive create myproject/ -f tar
```

### Extract Archives

```bash
# Extract ZIP
archive extract archive.zip

# Extract TAR.GZ
archive extract archive.tar.gz

# Extract to specific directory
archive extract archive.zip -o /tmp/output/
```

### List Archive Contents

```bash
# List ZIP contents
archive list archive.zip

# List TAR.GZ contents
archive list archive.tar.gz
```

### Get Archive Info

```bash
# Show ZIP info
archive info archive.zip

# Show TAR.GZ info
archive info archive.tar.gz
```

## Use Cases

### Backup Projects

```bash
# Backup project
archive create myproject/ -o myproject-backup.zip

# Backup with date
archive create myproject/ -o myproject-$(date +%Y%m%d).zip
```

### Share Files

```bash
# Archive for sharing
archive create files-to-share/ -o share.zip
```

### Deploy Archives

```bash
# Create deployment archive
archive create dist/ -f tar.gz

# Extract on server
archive extract dist.tar.gz
```

### Clean Up Directories

```bash
# Archive old projects
archive create old-project/ -f tar.gz
rm -rf old-project/
```

### Distribution

```bash
# Create release archive
archive create release/ -f tar.gz
```

### Integration with Other Tools

### With notes (note taking)

```bash
# Note backup location
archive create myproject/ -o backup.zip | notes add "Backup created"

# Note extraction
archive extract backup.zip | notes add "Backup extracted"
```

### With fsearch (file search)

```bash
# Find files before archiving
fsearch --pattern "*.py" myproject/

# Archive found files
archive create myproject/
```

### With run (command runner)

```bash
# Store backup command
run add backup "archive create myproject/ -o myproject-backup.zip"

# Run backup
run backup
```

### With quick (CLI utilities)

```bash
# Check archive size
archive info archive.zip

# Quick backup
quick backup myproject/
```

### With logfind (log file search)

```bash
# Archive old logs
archive create logs/old/ -o old-logs.tar.gz
```

### With envman (environment manager)

```bash
# Archive environment config
archive create .env -o env-backup.zip
```

### With port (port checker)

```bash
# Archive service logs after checking port
port check localhost 8080
archive create logs/ -f tar.gz
```

## Format Comparison

| Format | Compression | Speed | Compatibility | Use Case |
|--------|-------------|--------|----------------|----------|
| ZIP | Good | Fast | Universal | Cross-platform sharing |
| TAR | None | Very Fast | Universal | Backup, no compression needed |
| TAR.GZ | Good | Fast | Linux/Unix | Linux distribution |
| TAR.BZ2 | Best | Slow | Linux/Unix | Maximum compression |
| TAR.XZ | Excellent | Slow | Linux/Unix | Long-term storage |

## Output Formats

### Create Output

```
Created: archive.zip
```

### Extract Output

```
Extracted to: /home/user/output/
```

### List Output

```
      1024  2026-02-16 18:00:00  file1.txt
     10240  2026-02-16 18:00:00  file2.txt
```

### Info Output

```
Archive: archive.zip
Size: 11.26 KB
Files: 2
Type: ZIP
```

## Best Practices

### Creating Archives

**Use ZIP for cross-platform:**
```bash
archive create myproject/ -f zip
```

**Use TAR.GZ for Linux:**
```bash
archive create myproject/ -f tar.gz
```

**Use TAR.XZ for long-term storage:**
```bash
archive create myproject/ -f tar.xz
```

### Backup Strategy

**Include date in backup names:**
```bash
archive create myproject/ -o myproject-$(date +%Y%m%d).zip
```

**Verify backup contents:**
```bash
archive list backup.zip
```

### Extraction

**Extract to temporary directory first:**
```bash
mkdir -p /tmp/extract
archive extract archive.zip -o /tmp/extract
```

### Compression

**Choose compression level:**
- Quick backup: ZIP or TAR.GZ
- Long-term storage: TAR.XZ
- Maximum compression: TAR.BZ2

## Troubleshooting

### Archive Creation Fails

**Check source exists:**
```bash
ls -la myproject/
```

**Check write permissions:**
```bash
ls -la output/
```

### Extraction Fails

**Verify archive is valid:**
```bash
archive info archive.zip
archive list archive.zip
```

### Wrong Format

**Auto-detection:**
- Tool auto-detects format from file extension
- No need to specify format for extraction

## Technical Details

**Supported Formats:**
- ZIP (.zip)
- TAR (.tar)
- TAR.GZ (.tar.gz)
- TAR.BZ2 (.tar.bz2)
- TAR.XZ (.tar.xz)

**Compression:**
- ZIP: DEFLATE compression
- TAR.GZ: GZIP compression
- TAR.BZ2: BZIP2 compression
- TAR.XZ: XZ compression

**Dependencies:**
- Python 3.6+
- No external tools (tar, zip, etc.)
- Built-in modules only

## Requirements

- Python 3.6+
- No external dependencies
- Works on Linux, macOS, Windows

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Compress. Extract. Archive.**

Simple archiving without external tools.
