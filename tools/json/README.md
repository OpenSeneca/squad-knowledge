# json — JSON Manipulation Tool

Parse, validate, query, format, and manipulate JSON data. jq-lite for the command line.

**Location:** `~/workspace/tools/json/`

**Install:** Symlink to `~/.local/bin/json`

```bash
ln -s ~/workspace/tools/json/json.py ~/.local/bin/json
chmod +x ~/workspace/tools/json/json.py
```

## Features

- **Parse & Validate** — Parse JSON from files or strings
- **Query** — Query JSON using dot notation
- **Format** — Pretty print or compact JSON
- **Extract** — Extract keys, values, paths
- **Manipulate** — Flatten, unflatten, merge JSON
- **Diff** — Find differences between JSON objects
- **Type Info** — Get type and size of JSON values
- **No Dependencies** — Pure Python, no jq required

## Key Commands

### Parsing & Validation

- `json <file>` — Parse and format JSON file
- `json --string '<json>'` — Parse JSON string
- `json --validate <file>` — Validate JSON file
- `json --validate --string '<json>'` — Validate JSON string

### Querying

- `json --query <path> <file>` — Query using dot notation
- `json --query 'user.name' <file>` — Extract nested value
- `json --query 'items[0].price' <file>` — Extract array element

### Formatting

- `json --format <file>` — Pretty print JSON
- `json --compact <file>` — Compact JSON (no whitespace)
- `json --format --indent 4 <file>` — Custom indentation
- `json --format --sort <file>` — Sort keys alphabetically

### Extraction

- `json --keys <file>` — Get all keys
- `json --values <file>` — Get all values
- `json --paths <file>` — Get all paths
- `json --type <file>` — Get type of value

### Manipulation

- `json --flatten <file>` — Flatten nested JSON
- `json --unflatten <file>` — Unflatten JSON
- `json --merge file1.json file2.json` — Merge JSON files
- `json --merge --deep file1.json file2.json` — Deep merge
- `json --diff file1.json file2.json` — Diff JSON files

### Info

- `json --size <file>` — Get size of JSON
- `json --type <file>` — Get type of value

## Examples

### Parsing JSON Files

```bash
# Parse and format JSON file
json data.json

# Parse with custom formatting
json --format --indent 4 data.json

# Parse with sorted keys
json --format --sort data.json

# Compact output (minified)
json --compact data.json
```

### Parsing JSON Strings

```bash
# Parse JSON string
json --string '{"name": "John", "age": 30}'

# Format JSON string
json --format --string '{"name": "John", "age": 30}'

# Compact JSON string
json --compact --string '{"name": "John", "age": 30}'
```

### Validating JSON

```bash
# Validate JSON file
json --validate data.json
# Output: Valid

# Validate JSON string
json --validate --string '{"name": "John"}'
# Output: Valid

# Validate invalid JSON
json --validate --string '{invalid}'
# Output: Invalid
```

### Querying JSON

```bash
# Extract nested value
json --query 'user.name' data.json
# Output: "John"

# Extract array element
json --query 'items[0]' data.json
# Output: {"name": "Item 1", "price": 10}

# Extract deep value
json --query 'items[0].price' data.json
# Output: 10

# Query root
json --query '' data.json
# Output: Entire JSON
```

### Extracting Keys and Values

```bash
# Get all keys
json --keys data.json
# Output: ["name", "age", "items"]

# Get all values
json --values data.json
# Output: ["John", 30, [...]]

# Get all paths
json --paths data.json
# Output: ["name", "age", "items", "items[0]", "items[0].name", ...]

# Get type
json --type data.json
# Output: object
```

### Flattening JSON

```bash
# Flatten nested JSON
json --flatten data.json
# Output: {"name": "John", "items[0].name": "Item 1", ...}

# Unflatten
json --unflatten data.json
# Output: {"name": "John", "items": [{"name": "Item 1", ...}]}
```

### Merging JSON

```bash
# Merge JSON files
json --merge file1.json file2.json

# Deep merge
json --merge --deep file1.json file2.json

# Merge multiple files
json --merge base.json override.json extras.json
```

### Diffing JSON

```bash
# Find differences
json --diff file1.json file2.json
# Output: {"added": ["new_field"], "removed": [], "changed": [...]}

# Compare files
json --diff old.json new.json
```

### Getting Size

```bash
# Get size of object
json --size data.json
# Output: 3

# Get size of array
json --size array.json
# Output: 5
```

## Use Cases

### API Testing

```bash
# Format API response
curl -s https://api.example.com/data | json --format

# Query specific value
curl -s https://api.example.com/user | json --query 'user.name'

# Validate API response
curl -s https://api.example.com/data | json --validate --string "$(cat)"
```

### Configuration Management

```bash
# Validate config
json --validate config.json

# Extract configuration value
json --query 'database.host' config.json

# Merge config files
json --merge base.json override.json > config.json
```

### Data Processing

```bash
# Flatten nested data
json --flatten data.json > flat.json

# Query array of items
json --query 'items[*].price' data.json

# Filter values
json --query 'items[?price>10]' data.json
```

### Debugging

```bash
# Pretty print minified JSON
json --format minified.json

# Validate JSON before use
json --validate data.json

# Compare JSON outputs
json --diff output1.json output2.json
```

### Log Analysis

```bash
# Parse JSON logs
json --format log.jsonl

# Extract specific fields
json --query 'message' log.json

# Count entries
json --size logs.json
```

### Data Migration

```bash
# Validate migration data
json --validate old.json
json --validate new.json

# Compare schemas
json --diff old.json new.json

# Merge data sources
json --merge source1.json source2.json > merged.json
```

### Integration with Other Tools

### With httpc (HTTP client)

```bash
# Format API response
httpc get https://api.example.com/data --json | json --format

# Extract value from API
httpc get https://api.example.com/user | json --query 'user.id'
```

### With fwatch (file watcher)

```bash
# Watch JSON file and format on change
fwatch -p data.json -c "json --format data.json"
```

### With logfind (log file search)

```bash
# Extract JSON from logs
logfind --pattern "json:" --format json | json --format --string "$(grep -o '{.*}')"
```

### With notes (note taking)

```bash
# Note JSON query results
json --query 'stats' data.json | notes add "API stats"

# Note validation errors
json --validate data.json || notes add "Invalid JSON found"
```

### With run (command runner)

```bash
# Store query command
run add get-user-name "json --query 'user.name' user.json"

# Run stored command
run get-user-name
```

## Output Formats

### Pretty Print

```json
{
  "name": "John",
  "age": 30,
  "items": [
    {"name": "Item 1", "price": 10}
  ]
}
```

### Compact

```json
{"name":"John","age":30,"items":[{"name":"Item 1","price":10}]}
```

### Query Output

```bash
# Single value
"John"

# Array
[{"name": "Item 1", "price": 10}]

# Number
10
```

### Keys Output

```json
["name", "age", "items"]
```

### Diff Output

```json
{
  "added": ["new_field"],
  "removed": ["old_field"],
  "changed": [
    {"key": "age", "old": 30, "new": 31}
  ]
}
```

## Query Syntax

**Dot Notation:**

- `user.name` — Access nested object
- `items[0]` — Access array element
- `items[0].price` — Access nested array element
- `items[*]` — Access all array elements (wildcard)

**Examples:**

```bash
# Root object
json --query '' data.json

# Nested object
json --query 'user.address.city' data.json

# Array element
json --query 'items[2]' data.json

# Nested array element
json --query 'items[0].tags[1]' data.json
```

## Best Practices

### Validation

**Always validate before use:**
```bash
# Validate first
json --validate data.json || exit 1

# Then process
json --format data.json
```

### Querying

**Use specific paths:**
```bash
# Good (specific)
json --query 'user.name' data.json

# Too broad
json --query 'user' data.json
```

**Check type before processing:**
```bash
# Check type first
json --query 'items' data.json | json --type

# Then process if array
if json --query 'items' data.json | json --type | grep -q array; then
  json --query 'items[*].name' data.json
fi
```

### Formatting

**Use pretty print for human reading:**
```bash
json --format data.json
```

**Use compact for storage/transmission:**
```bash
json --compact data.json
```

**Use sort for consistency:**
```bash
json --format --sort data.json
```

### Merging

**Deep merge for nested objects:**
```bash
json --merge --deep base.json override.json
```

**Shallow merge for simple overrides:**
```bash
json --merge base.json override.json
```

### Diffing

**Use diff for validation:**
```bash
# Compare before/after
json --diff before.json after.json
```

## Troubleshooting

### Invalid JSON

**Check syntax:**
```bash
# Validate file
json --validate data.json

# Get error details
json data.json
```

### Query Returns Nothing

**Check path:**
```bash
# Show all paths
json --paths data.json

# Verify path exists
json --query 'user.name' data.json
```

### Merge Overwrites Values

**Use deep merge:**
```bash
# Deep merge preserves nested values
json --merge --deep base.json override.json
```

### Flatten Loses Structure

**Save original before flattening:**
```bash
# Backup original
cp data.json data.bak.json

# Then flatten
json --flatten data.json
```

## Comparison to jq

**vs `jq`:**
- `jq`: More powerful, complex syntax, external dependency
- `json`: Simpler, pure Python, built-in syntax

**When to use `json`:**
- Simple queries and formatting
- No external dependencies allowed
- Python code integration
- Simple data manipulation

**When to use `jq`:**
- Complex filtering and transformations
- Advanced data manipulation
- Performance-critical operations

## Technical Details

**Supported JSON Types:**
- Object (`{}`)
- Array (`[]`)
- String (`""`)
- Number (`123`, `12.3`)
- Boolean (`true`, `false`)
- Null (`null`)

**Query Features:**
- Dot notation for nested access
- Array indexing
- Wildcard support (`[*]`)
- Type-aware access

**Manipulation Features:**
- Flatten/unflatten with dot notation
- Deep/shallow merge
- Diff with added/removed/changed
- Keys/values/paths extraction

## Requirements

- Python 3.6+
- No external dependencies
- JSON support built-in

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Parse. Query. Format.**

JSON manipulation made simple without jq.
