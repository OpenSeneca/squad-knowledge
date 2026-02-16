# hash — File Hash Calculator

Calculate file hashes (MD5, SHA1, SHA256, SHA512) for verification.

**Location:** `~/workspace/tools/hash/`

**Install:** Symlink to `~/.local/bin/hash`

```bash
ln -s ~/workspace/tools/hash/hash.py ~/.local/bin/hash
chmod +x ~/workspace/tools/hash/hash.py
```

## Features

- **Calculate Hashes** — MD5, SHA1, SHA256, SHA512
- **Verify Hashes** — Verify file integrity
- **Multiple Files** — Process multiple files at once
- **All Hashes** — Calculate all hash types
- **Quiet Mode** — Only show hash (for scripting)
- **No Dependencies** — Pure Python

## Key Commands

### Calculate Hash

- `hash <file>` — Calculate SHA256 hash (default)
- `hash <file> -a md5` — Calculate MD5 hash
- `hash <file> -a sha1` — Calculate SHA1 hash
- `hash <file> -a sha256` — Calculate SHA256 hash
- `hash <file> -a sha512` — Calculate SHA512 hash

### Multiple Files

- `hash file1.txt file2.txt` — Hash multiple files
- `hash *.txt` — Hash all text files

### Verify Hash

- `hash <file> -v <hash>` — Verify file against hash
- `hash <file> -v <hash> -a sha256` — Verify with specific algorithm

### All Hashes

- `hash <file> --all` — Calculate all hashes
- `hash <file> --all --quiet` — All hashes, output only

### Quiet Mode

- `hash <file> -q` — Only show hash (no filename)
- `hash <file> --verify <hash> -q` — Only show OK/FAIL

## Algorithms

| Algorithm | Hash Length | Use Case |
|-----------|-------------|-----------|
| MD5 | 32 chars | Legacy verification, checksums |
| SHA1 | 40 chars | Git, legacy verification |
| SHA256 | 64 chars | Default, modern applications |
| SHA512 | 128 chars | Maximum security |

## Examples

### Calculate SHA256

```bash
# Calculate SHA256 hash
hash file.txt

# Output:
# a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e  file.txt (12.00 B)
```

### Calculate Different Algorithms

```bash
# MD5
hash file.txt -a md5

# SHA1
hash file.txt -a sha1

# SHA256 (default)
hash file.txt

# SHA512
hash file.txt -a sha512
```

### Hash Multiple Files

```bash
# Multiple files
hash file1.txt file2.txt file3.txt

# All text files
hash *.txt

# All Python files
hash *.py

# Output:
# a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e  file1.txt (12.00 B)
# c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960744ef5a0c43  file2.txt (12.00 B)
# a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e  file3.txt (12.00 B)
```

### Calculate All Hashes

```bash
# All hashes for one file
hash file.txt --all

# Output:
# file.txt (12.00 B)
#       MD5: 098f6bcd4621d373cade4e832627b4f6
#      SHA1: 356a192b7913b04c54574d18c28d46e6395428ab
#    SHA256: a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
#    SHA512: 9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043
```

### Verify Hash

```bash
# Verify file
hash file.txt -v a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e

# Output (valid):
# ✓ file.txt: Hash matches

# Output (invalid):
# ✗ file.txt: Hash mismatch
#   Expected: invalidhashhere...
#   Actual:   a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
```

### Quiet Mode

```bash
# Only hash (no filename)
hash file.txt -q
# Output: a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e

# Verify (quiet)
hash file.txt -v a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e -q
# Output: OK (or FAIL)
```

## Use Cases

### Verify Downloads

```bash
# Download file
wget https://example.com/file.zip

# Verify against provided hash
hash file.zip -v expected-sha256-hash
```

### Check File Integrity

```bash
# Calculate hash before modification
hash file.txt > hash.txt

# Later, verify file
hash file.txt -v $(cat hash.txt)
```

### Create Checksums

```bash
# Create checksums for all files
hash *.txt > checksums.txt

# Verify all files
# (Script to check each hash)
```

### Compare Files

```bash
# Check if files are identical
hash file1.txt
hash file2.txt

# If hashes match, files are identical
```

### Security Verification

```bash
# Verify downloaded binary
hash binary.exe -v expected-sha512-hash -a sha512

# Verify critical files
hash /etc/passwd -v expected-hash
```

### Backup Verification

```bash
# Hash backup files
hash backup.tar.gz > backup.hash

# Later, verify backup
hash backup.tar.gz -v $(cat backup.hash)
```

### Integration with Other Tools

### With archive (archive tool)

```bash
# Hash archive before distribution
archive create project/ -f tar.gz
hash project.tar.gz > project.tar.gz.sha256

# Verify after download
hash project.tar.gz -v $(cat project.tar.gz.sha256)
```

### With notes (note taking)

```bash
# Note hash for verification
hash important.dat | notes add "Important file hash"

# Verify later
hash important.dat -v $(notes list | grep "Important file hash" | extract hash)
```

### With run (command runner)

```bash
# Store verification command
run add verify-file "hash file.txt -v expected-hash"

# Run verification
run verify-file
```

### With fsearch (file search)

```bash
# Find files and hash them
fsearch --pattern "*.py" src/
hash $(fsearch --pattern "*.py" src/)
```

### With fdiff (file comparison)

```bash
# Compare hashes first
hash file1.txt
hash file2.txt

# If hashes differ, use fdiff
fdiff file1.txt file2.txt
```

### With logfind (log file search)

```bash
# Hash log files
hash logs/*.log

# Check for changes over time
```

## Best Practices

### Hash Selection

**Use SHA256 for most cases:**
```bash
hash file.txt -a sha256
```

**Use SHA512 for maximum security:**
```bash
hash file.txt -a sha512
```

**Use MD5/SHA1 only for legacy:**
```bash
hash file.txt -a md5
```

### Verification

**Always verify downloads:**
```bash
# Download
wget https://example.com/file.zip

# Verify
hash file.zip -v expected-hash

# Only use file if verification succeeds
```

**Store hashes securely:**
```bash
# Create hash file
hash important.dat > important.dat.sha256

# Move to secure location
mv important.dat.sha256 /secure/
```

### Scripting

**Use quiet mode for scripts:**
```bash
# Check file integrity
if hash file.txt -q != expected-hash; then
  echo "File corrupted!"
  exit 1
fi
```

## Hash Output Format

### Single Hash

```
<hash>  <filename> (<size>)
```

### Multiple Hashes

```
<filename> (<size>)
  <ALGORITHM>: <hash>
  <ALGORITHM>: <hash>
  ...
```

### Verification

```
✓ <filename>: Hash matches
# or
✗ <filename>: Hash mismatch
  Expected: <expected-hash>
  Actual:   <actual-hash>
```

### Quiet Mode

```
<hash>
# or
OK / FAIL
```

## Troubleshooting

### Hash Mismatch

**Check file corruption:**
```bash
# Re-download file
wget https://example.com/file.zip

# Re-verify
hash file.zip -v expected-hash
```

### File Not Found

**Check path:**
```bash
ls -la file.txt
hash file.txt
```

### Algorithm Not Supported

**Use supported algorithm:**
```bash
# Supported: md5, sha1, sha256, sha512
hash file.txt -a sha256
```

## Technical Details

**Hash Algorithms:**
- MD5: 128-bit hash (32 hex chars)
- SHA1: 160-bit hash (40 hex chars)
- SHA256: 256-bit hash (64 hex chars)
- SHA512: 512-bit hash (128 hex chars)

**Chunk Size:**
- Default: 8192 bytes (8 KB)
- Configurable with --chunk-size
- Larger chunks = faster for large files

**Case Insensitivity:**
- Hash verification is case-insensitive
- Output is lowercase

## Security Notes

**Algorithm Security:**
- MD5: Broken, not secure for cryptographic purposes
- SHA1: Broken, not secure for cryptographic purposes
- SHA256: Secure for all current applications
- SHA512: Secure for all current applications

**Use Cases:**
- File integrity: SHA256 recommended
- Cryptographic verification: SHA512 recommended
- Legacy compatibility: MD5/SHA1 only if required

## Requirements

- Python 3.6+
- No external dependencies
- Works on Linux, macOS, Windows

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Verify. Confirm. Trust.**

File hash calculation for integrity verification.
