# quick — Quick CLI Utilities

Fast conversions and calculations right in your terminal.

**Location:** `~/workspace/tools/quick/`

**Install:** Symlink to `~/.local/bin/quick`

```bash
ln -s ~/workspace/tools/quick/quick.py ~/.local/bin/quick
chmod +x ~/workspace/tools/quick/quick.py
```

## Features

- **Base64 Encoding/Decoding** — Encode/decode text to/from base64
- **URL Encoding/Decoding** — URL encode/decode text
- **Timestamp Conversion** — Convert Unix/ISO timestamps
- **Color Conversion** — Convert hex to RGB/HSL
- **JSON Formatting** — Pretty-print or minify JSON
- **String Analysis** — Count chars, bytes, words, lines
- **UUID Generation** — Generate random UUIDs
- **Hashing** — Hash text (MD5, SHA1, SHA256, SHA512)
- **Zero Dependencies** — Pure Python, no external packages

## Key Commands

### Encoding/Decoding

- `quick b64encode <text>` — Encode text to base64
- `quick b64decode <text>` — Decode base64 to text
- `quick urlencode <text>` — URL encode text
- `quick urldecode <text>` — URL decode text

### Timestamps

- `quick timestamp` — Show current time
- `quick timestamp <unix>` — Convert Unix timestamp
- `quick timestamp <iso>` — Convert ISO timestamp
- `quick timestamp -f all` — Show all formats

### Colors

- `quick hex2rgb <hex>` — Convert hex to RGB/HSL

### JSON

- `quick json-pretty <json>` — Format JSON
- `quick json-minify <json>` — Minify JSON

### String Analysis

- `quick strlen <text>` — Calculate string length
- `quick strlen <text> --bytes` — Count bytes instead of chars

### UUID & Hash

- `quick uuid` — Generate random UUID
- `quick hash <text>` — Hash text (default: MD5)
- `quick hash <text> -a sha256` — Hash with specific algorithm

## Examples

### Base64 Encoding/Decoding

```bash
# Encode to base64
quick b64encode "Hello World"
# SGVsbG8gV29ybGQ=

# Decode from base64
quick b64decode "SGVsbG8gV29ybGQ="
# Hello World

# URL-safe encoding
quick b64encode "user:password" --urlsafe
# dXNlcjpwYXNzd29yZA==
```

**Use Cases:**
- Encoding credentials for HTTP headers
- Encoding data for URLs
- Decoding base64-encoded strings
- Creating JWT payloads

### URL Encoding/Decoding

```bash
# URL encode
quick urlencode "hello world"
# hello%20world

# URL encode special characters
quick urlencode "user@domain.com"
# user%40domain.com

# URL decode
quick urldecode "hello%20world"
# hello world
```

**Use Cases:**
- Encoding URLs for API requests
- Encoding query parameters
- Decoding URL-encoded strings
- Creating properly formatted URLs

### Timestamp Conversion

```bash
# Show current time
quick timestamp
# 📅 2026-02-16 08:50:00
#
# ISO:     2026-02-16T08:50:00.123456
# Unix:    1644982200

# Convert Unix timestamp
quick timestamp 1644982200
# 📅 2026-02-16 08:50:00
#
# ISO:     2026-02-16T08:50:00

# Convert ISO timestamp
quick timestamp "2026-02-16T08:50:00"
# 📅 2026-02-16 08:50:00
#
# ISO:     2026-02-16T08:50:00
# Unix:    1644982200

# Show all formats
quick timestamp 1644982200 -f all
# 📅 2026-02-16 08:50:00
#
# ISO:     2026-02-16T08:50:00.123456
# Unix:    1644982200
# RFC2822: Mon, 16 Feb 2026 08:50:00 +0000
# ISO8601: 2026-02-16T08:50:00+0000
```

**Use Cases:**
- Debugging timestamp issues
- Converting between timestamp formats
- Creating log timestamps
- Comparing timestamps

### Color Conversion

```bash
# Convert hex to RGB
quick hex2rgb "#3b82f6"
# RGB: rgb(59, 130, 246)
# CSS: rgb(59, 130, 246)
# HSL: hsl(221, 91%, 60%)

# Convert hex (without #)
quick hex2rgb "3b82f6"
# RGB: rgb(59, 130, 246)
# CSS: rgb(59, 130, 246)
# HSL: hsl(221, 91%, 60%)
```

**Use Cases:**
- Converting colors between formats
- Working with CSS colors
- Design work with color codes
- Creating color palettes

### JSON Formatting

```bash
# Format JSON
quick json-pretty '{"name":"test","count":42}'
# {
#   "name": "test",
#   "count": 42
# }

# Format from file
quick json-pretty data.json

# Minify JSON
quick json-minify '{
#   "name": "test",
#   "count": 42
# }'
# {"name":"test","count":42}

# Minify from file
quick json-minify data.json
```

**Use Cases:**
- Pretty-printing JSON for reading
- Minifying JSON for size reduction
- Debugging JSON structure
- Validating JSON syntax

### String Analysis

```bash
# Count characters
quick strlen "Hello World"
# Chars:   11
# Words:    2
# Lines:    1

# Count bytes (UTF-8)
quick strlen "Hello World" --bytes
# Bytes:   11
# Words:    2
# Lines:    1

# Count bytes for multi-byte characters
quick strlen "你好" --bytes
# Bytes:   6
# Chars:   2
```

**Use Cases:**
- Checking string lengths for database limits
- Counting bytes for storage limits
- Validating input length constraints
- Debugging encoding issues

### UUID Generation

```bash
# Generate UUID
quick uuid
# 550e8400-e29b-41d4-a716-446655440000

# Generate multiple
for i in {1..5}; do quick uuid; done
```

**Use Cases:**
- Generating unique IDs
- Creating database keys
- Generating session tokens
- Creating test data

### Hashing

```bash
# Hash text (MD5 default)
quick hash "my-password"
# MD5: 5f4dcc3b5aa765d61d8327deb882cf99

# Hash with SHA256
quick hash "my-password" -a sha256
# SHA256: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

# Hash with SHA512
quick hash "my-password" -a sha512
# SHA512: 109f4b3c71f9f1d72f4bb299d2d2a52c2b326d553f2234f014a0e1f5e1c7464d0246e0f6b05838421896522...

# Generate password hash
quick hash "MySecurePassword123!" -a sha256
```

**Use Cases:**
- Generating password hashes
- Creating file integrity checksums
- Hashing API tokens
- Comparing hash values

## Use Cases

### Development

```bash
# Encode API key
API_KEY=$(quick b64encode "my-api-key")
curl -H "Authorization: Bearer $API_KEY" https://api.example.com

# URL encode query parameter
QUERY=$(quick urlencode "hello world")
curl "https://api.example.com/search?q=$QUERY"

# Convert timestamp
LOG_TIME="1644982200"
quick timestamp $LOG_TIME
# 📅 2026-02-16 08:50:00
```

### API Testing

```bash
# Create JSON payload
PAYLOAD='{"user":"test","action":"login"}'
quick json-pretty "$PAYLOAD"
# {
#   "user": "test",
#   "action": "login"
# }

# Send pretty JSON
curl -H "Content-Type: application/json" \
     -d "$(quick json-minify "$PAYLOAD")" \
     https://api.example.com/endpoint
```

### Configuration

```bash
# Generate config hash
CONFIG_HASH=$(quick hash "$(cat config.json)")
echo "Config hash: $CONFIG_HASH"

# Verify config integrity
if [ "$(quick hash "$(cat config.json)")" == "$CONFIG_HASH" ]; then
    echo "Config unchanged"
else
    echo "Config modified!"
fi
```

### Data Validation

```bash
# Check JSON syntax
quick json-pretty "$(cat data.json)"
# If valid: pretty printed
# If invalid: ❌ Invalid JSON

# Check string length
if [ $(quick strlen "$(cat message.txt)" | grep "Chars:" | awk '{print $2}') -gt 280 ]; then
    echo "Message too long!"
fi
```

### Security

```bash
# Generate password hash
quick hash "my-secret-password" -a sha256
# SHA256: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

# Encode credentials for HTTP basic auth
CREDENTIALS=$(quick b64encode "user:password")
curl -H "Authorization: Basic $CREDENTIALS" https://api.example.com

# Generate secure random token
TOKEN=$(quick uuid)
echo "Token: $TOKEN"
```

### Debugging

```bash
# Decode base64-encoded data
echo "SGVsbG8gV29ybGQ=" | quick b64decode
# Hello World

# Decode URL-encoded string
echo "hello%20world%20%21" | quick urldecode
# hello world !

# Convert timestamp from logs
LOG_TIME="1644982200"
quick timestamp $LOG_TIME -f all
# 📅 2026-02-16 08:50:00
# ISO:     2026-02-16T08:50:00
# Unix:    1644982200
```

### Design Work

```bash
# Convert design color
quick hex2rgb "#3b82f6"
# RGB: rgb(59, 130, 246)
# CSS: rgb(59, 130, 246)
# HSL: hsl(221, 91%, 60%)

# Generate multiple UUIDs for test data
for i in {1..10}; do
    echo "$(quick uuid)"
done
```

## Integration with Other Tools

**With run (command runner):**
```bash
# Quick encode command
run add b64enc "quick b64encode"

# Use in scripts
TOKEN=$(quick b64encode "$API_TOKEN")
```

**With notes (note taking):**
```bash
# Note hash for verification
notes add "Config hash: $(quick hash config.json)" -c debug -t hash -t config
```

**With snip (snippet manager):**
```bash
# Save encoding patterns
snip add b64-token "TOKEN=\$(quick b64encode \"\$TOKEN\")"
snip add url-param "QUERY=\$(quick urlencode \"\$QUERY\")"
```

**With tick (task tracker):**
```bash
# Task with quick reference
tick add "Test API - token: $(quick uuid)" -p high
```

**With git-helper (git automation):**
```bash
# Commit with generated UUID
git-helper commit "feat: Generated unique ID $(quick uuid)"
```

## Comparison to Alternatives

**vs Online Tools:**
- `quick`: Instant, no network required
- `online`: Slower, requires internet

**vs Complex Tools:**
- `quick`: Simple, focused commands
- `complex`: More features, more learning curve

**vs Language-Specific:**
- `quick`: Language-agnostic
- `python`: Python only
- `node`: Node.js only

## Future Enhancements

- **QR Code Generation** — Generate QR codes from text/URLs
- **Barcode Generation** — Generate barcodes
- **Color Palettes** — Generate complementary colors
- **Diff** — Show differences between strings
- **Base32/58 Encoding** — Additional encoding formats
- **JWT Parsing** — Decode and validate JWTs
- **Regular Expression Tester** — Test regex patterns
- **HTML Encoding** — HTML encode/decode

## Requirements

- Python 3.6+
- No external dependencies
- No storage (stateless)

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Fast. Simple. Stateless.**

Quick utilities for developers, right in your terminal.
