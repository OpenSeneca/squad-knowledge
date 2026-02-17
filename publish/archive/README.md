# archive — Archive and Compression Tool

Compress and extract archives (zip, tar.gz, tar.bz2, tar.xz) without external tools.

## What It Does

Simple archiving with no external dependencies:

- **Multiple Formats** — ZIP, TAR, TAR.GZ, TAR.BZ2, TAR.XZ
- **Extract Archives** — Extract any supported format
- **List Contents** — View archive contents
- **Archive Info** — Show statistics

## Installation

```bash
pip install archive-cli-tool
```

Or symlink:

```bash
ln -s $(pwd)/archive.py ~/.local/bin/archive
chmod +x archive.py
```

## Quick Start

```bash
archive create myproject/              # Create ZIP
archive create myproject/ -f tar.gz   # Create TAR.GZ
archive extract archive.zip            # Extract
archive list archive.zip               # List contents
archive info archive.zip               # Show info
```

## Examples

```bash
$ archive create test/ -o test.zip
Created: test.zip

$ archive info test.zip
Archive: test.zip
Size: 238.00 B
Files: 2
Type: ZIP

$ archive list test.zip
     12  2026-02-16 18:06:38  file1.txt
     12  2026-02-16 18:06:38  file2.txt
```

## License

MIT License
