# fhash — File Hash Calculator

Calculate file hashes (MD5, SHA1, SHA256, SHA512) for verification.

## What It Does

Fast file hash calculator for integrity verification:

- **Multiple Algorithms** — MD5, SHA1, SHA256, SHA512
- **Hash Verification** — Verify files against expected hashes
- **All Hashes** — Calculate all hash types at once
- **Multiple Files** — Process multiple files
- **Quiet Mode** — Output only hash (for scripting)

## Installation

```bash
pip install fhash-cli-tool
```

Or symlink:

```bash
ln -s $(pwd)/fhash.py ~/.local/bin/fhash
chmod +x fhash.py
```

## Quick Start

```bash
fhash file.txt                      # Calculate SHA256
fhash file.txt -a md5             # Calculate MD5
fhash file.txt --all               # All hashes
fhash file.txt -v <hash>           # Verify hash
fhash file.txt -q                  # Quiet mode
```

## Examples

```bash
$ fhash file.txt
a1fff0ffefb9eace7230c24e50731f0a91c62f9cefdfe77121c2f607125dffae  file.txt (13.00 B)

$ fhash file.txt -a md5
d6eb32081c822ed572b70567826d9d9d  file.txt (13.00 B)

$ fhash file.txt --all

file.txt (13.00 B)
       MD5: d6eb32081c822ed572b70567826d9d9d
      SHA1: 4fe2b8dd12cd9cd6a413ea960cd8c09c25f19527
    SHA256: a1fff0ffefb9eace7230c24e50731f0a91c62f9cefdfe77121c2f607125dffae
    SHA512: b22137a0e8969282b85e3f9375448307d14c5aabf41be66c4f6a0323bd03a3935972021e4c34aa30914e37b03c22594fe180eea9790e9ff147016c9dfae39d5a
```

## License

MIT License
