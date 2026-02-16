# http — HTTP Client for API Testing

Simple HTTP client for making requests, testing APIs, debugging web services. Lightweight alternative to curl with better JSON handling.

**Location:** `~/workspace/tools/http/`

**Install:** Symlink to `~/.local/bin/http`

```bash
ln -s ~/workspace/tools/http/http.py ~/.local/bin/http
chmod +x ~/workspace/tools/http/http.py
```

## Features

- **All HTTP Methods** — GET, POST, PUT, DELETE
- **JSON Support** — Automatic JSON handling and formatting
- **Headers** — Set custom headers easily
- **Query Parameters** — Add query parameters to URLs
- **Authentication** — Basic auth support
- **Timeout Control** — Adjustable request timeout
- **Verbose Mode** — Show request details
- **Response Inspection** — View status, headers, body, timing
- **JSON Output** — Machine-readable output
- **Request History** — Track all requests

## Key Commands

### GET Requests

- `http get <url>` — Simple GET request
- `http get <url> --params <params>` — GET with query parameters
- `http get <url> --headers <headers>` — GET with headers
- `http get <url> --show-headers` — Show response headers
- `http get <url> --verbose` — Show request and response details

### POST Requests

- `http post <url> --data <data>` — POST with data
- `http post <url> --json <json>` — POST with JSON
- `http post <url> --json <json> --headers <headers>` — POST with JSON and headers
- `http post <url> --json '{"name":"John"}'` — Quick JSON POST

### PUT Requests

- `http put <url> --data <data>` — PUT with data
- `http put <url> --json <json>` — PUT with JSON
- `http put <url> --json '{"name":"Jane"}'` — Quick JSON PUT

### DELETE Requests

- `http delete <url>` — DELETE request
- `http delete <url> --headers <headers>` — DELETE with headers

### Common Options

- `--timeout <seconds>` — Set timeout (default: 10s)
- `--verbose, -v` — Show request details
- `--show-headers` — Show response headers
- `--hide-body` — Hide response body
- `--no-pretty` — Don't pretty-print JSON
- `--json-output` — Output as JSON

## Examples

### Simple GET Request

```bash
# Get a webpage
http get http://example.com

# Get API data
http get http://api.example.com/users

# Get specific resource
http get http://api.example.com/users/123
```

### GET with Query Parameters

```bash
# JSON format
http get http://api.example.com/users --params '{"page":1,"limit":10}'

# Key-value format
http get http://api.example.com/users --params "page=1,limit=10"

# Search query
http get http://api.example.com/products --params "query=phone,category=electronics"
```

### GET with Headers

```bash
# JSON format
http get http://api.example.com/users --headers '{"Authorization":"Bearer token"}'

# Key-value format
http get http://api.example.com/users --headers "Authorization:Bearer token"

# Multiple headers
http get http://api.example.com/users --headers "Authorization:Bearer token,Accept:application/json"
```

### POST with JSON

```bash
# Simple JSON POST
http post http://api.example.com/users --json '{"name":"John","email":"john@example.com"}'

# POST with headers
http post http://api.example.com/users \
  --json '{"name":"John","email":"john@example.com"}' \
  --headers "Authorization:Bearer token,Content-Type:application/json"

# Create nested data
http post http://api.example.com/products --json '{
  "name": "Product",
  "price": 29.99,
  "category": {"id": 1, "name": "Electronics"}
}'
```

### POST with Data

```bash
# POST with raw data
http post http://api.example.com/data --data "raw string data"

# POST with form data
http post http://api.example.com/form \
  --data "name=John&email=john@example.com"
```

### PUT with JSON

```bash
# Update resource
http put http://api.example.com/users/123 --json '{"name":"Jane"}'

# PUT with headers
http put http://api.example.com/users/123 \
  --json '{"name":"Jane","email":"jane@example.com"}' \
  --headers "Authorization:Bearer token"
```

### DELETE Request

```bash
# Delete resource
http delete http://api.example.com/users/123

# Delete with headers
http delete http://api.example.com/users/123 \
  --headers "Authorization:Bearer token"
```

### Show Response Details

```bash
# Show headers
http get http://api.example.com/users --show-headers

# Verbose mode (show request and response)
http post http://api.example.com/users --json '{"name":"John"}' --verbose

# Hide body (just status and time)
http get http://api.example.com/users --hide-body
```

### Adjust Timeout

```bash
# Quick timeout (5s)
http get http://slow-api.com --timeout 5

# Long timeout (30s)
http get http://slow-api.com --timeout 30
```

### JSON Output

```bash
# Get full response as JSON
http get http://api.example.com/users --json-output

# Pipe to jq
http get http://api.example.com/users --json-output | jq '.[] | .name'

# Save to file
http get http://api.example.com/users --json-output > response.json
```

### No Pretty Print

```bash
# Raw JSON output (compact)
http get http://api.example.com/users --no-pretty

# Useful for piping
http get http://api.example.com/users --no-pretty | wc -l
```

## Use Cases

### API Testing

```bash
# Test GET endpoint
http get http://api.example.com/users

# Test POST endpoint
http post http://api.example.com/users --json '{"name":"John"}'

# Test PUT endpoint
http put http://api.example.com/users/123 --json '{"name":"Jane"}'

# Test DELETE endpoint
http delete http://api.example.com/users/123
```

### Authentication

```bash
# Bearer token
http get http://api.example.com/users \
  --headers "Authorization:Bearer YOUR_TOKEN"

# Basic auth (manual header)
http get http://api.example.com/users \
  --headers "Authorization:Basic BASE64_ENCODED_CREDENTIALS"

# Custom auth header
http get http://api.example.com/users \
  --headers "X-API-Key:YOUR_API_KEY"
```

### Debugging APIs

```bash
# Check status code
http get http://api.example.com/users

# See response headers
http get http://api.example.com/users --show-headers

# See full request/response
http post http://api.example.com/users --json '{"name":"John"}' --verbose

# Check timing
http get http://api.example.com/users --hide-body
```

### Pagination

```bash
# Page 1
http get http://api.example.com/users --params "page=1,limit=10"

# Page 2
http get http://api.example.com/users --params "page=2,limit=10"

# With search
http get http://api.example.com/users --params "page=1,limit=10,search=John"
```

### Filtering and Sorting

```bash
# Filter results
http get http://api.example.com/products --params "category=electronics"

# Sort results
http get http://api.example.com/products --params "sort=price,order=asc"

# Multiple filters
http get http://api.example.com/users --params "status=active,role=admin"
```

### Webhooks

```bash
# Test webhook
http post http://webhook.site/YOUR_ID \
  --json '{"event":"user_created","data":{"user_id":123}}'

# Test webhook with headers
http post http://webhook.site/YOUR_ID \
  --json '{"event":"user_created"}' \
  --headers "X-Webhook-Secret:secret123"
```

### JSON API Testing

```bash
# Create resource
http post http://api.example.com/users --json '{
  "name": "John Doe",
  "email": "john@example.com"
}'

# Update resource
http put http://api.example.com/users/1 --json '{
  "email": "newemail@example.com"
}'

# Delete resource
http delete http://api.example.com/users/1
```

### REST API Workflows

```bash
# Complete CRUD workflow
# Create
USER_ID=$(http post http://api.example.com/users \
  --json '{"name":"John"}' --json-output | jq -r '.id')

# Read
http get http://api.example.com/users/$USER_ID

# Update
http put http://api.example.com/users/$USER_ID \
  --json '{"name":"Jane"}'

# Delete
http delete http://api.example.com/users/$USER_ID
```

### Health Checks

```bash
# Check API health
http get http://api.example.com/health

# Check with timeout
http get http://api.example.com/health --timeout 5

# Check in a loop
while true; do
  http get http://api.example.com/health --hide-body
  sleep 10
done
```

### Data Export

```bash
# Export users to JSON
http get http://api.example.com/users --json-output > users.json

# Export products to JSON
http get http://api.example.com/products --params "limit=100" --json-output > products.json

# Pretty print and save
http get http://api.example.com/users --json-output | jq '.' > users.json
```

## Integration with Other Tools

### With jq (JSON processor)

```bash
# Extract specific field
http get http://api.example.com/users --json-output | jq '.[0].name'

# Filter results
http get http://api.example.com/users --json-output | jq '.[] | select(.active == true)'

# Count items
http get http://api.example.com/users --json-output | jq 'length'

# Format output
http get http://api.example.com/users --json-output | jq -r '.[] | "\(.name) - \(.email)"'
```

### With grep (text search)

```bash
# Search response
http get http://api.example.com/users | grep "John"

# Find status code
http get http://api.example.com/users | grep "Status:"

# Find error messages
http get http://api.example.com/users | grep -i error
```

### With notes (note taking)

```bash
# Note API response
http get http://api.example.com/users | notes add "User API response"

# Note API errors
http get http://api.example.com/users --json-output | \
  jq 'select(.error)' | notes add "API errors" -c debug
```

### With run (command runner)

```bash
# Store API command
run add get-users "http get http://api.example.com/users"

# Run stored command
run get-users
```

### With fwatch (file watcher)

```bash
# Watch config file, reload API
fwatch -p "config.json" -c "http post http://api.example.com/reload --json @config.json"
```

### With port (port checker)

```bash
# Check if API port is open
port check api.example.com 80

# Then test API
http get http://api.example.com/health
```

## Comparison to Alternatives

**vs `curl`:**
- `curl`: More features, more complex syntax
- `http`: Simpler, better JSON handling, auto-formatting

**vs `httpie`:**
- `httpie`: More features, colored output
- `http`: Simpler, no external dependencies

**vs `wget`:**
- `wget`: Download-focused
- `http`: API testing-focused

## Best Practices

### Error Handling

```bash
# Check status code
if http get http://api.example.com/users | grep "200"; then
  echo "Success"
else
  echo "Failed"
fi

# Check with json-output
STATUS=$(http get http://api.example.com/users --json-output | jq -r '.status')
if [ "$STATUS" = "200" ]; then
  echo "Success"
fi
```

### Large Responses

```bash
# Hide body for large responses
http get http://api.example.com/large-data --hide-body

# Save to file
http get http://api.example.com/large-data > data.json

# Stream to jq
http get http://api.example.com/large-data --json-output | jq '.data[]'
```

### Repeated Requests

```bash
# Loop with delay
for i in {1..10}; do
  http get http://api.example.com/health --hide-body
  sleep 1
done

# Test load
for i in {1..100}; do
  http get http://api.example.com/users &
done
wait
```

### Complex Headers

```bash
# JSON format for complex headers
http get http://api.example.com/users \
  --headers '{
    "Authorization": "Bearer token",
    "Accept": "application/json",
    "X-Request-ID": "12345",
    "X-Custom-Header": "value"
  }'

# Key-value format for simple headers
http get http://api.example.com/users \
  --headers "Authorization:Bearer token,Accept:application/json"
```

## Troubleshooting

### Connection Timeout

```bash
# Increase timeout
http get http://slow-api.com --timeout 30

# Check if host is reachable
ping api.example.com

# Check if port is open
port check api.example.com 80
```

### SSL/HTTPS Issues

```bash
# Note: Python's urllib may need additional config for SSL
# For simple testing, try HTTP first
http get http://api.example.com/users
```

### Authentication Issues

```bash
# Check auth header
http get http://api.example.com/users --verbose

# Verify token format
echo "Bearer YOUR_TOKEN" | wc -c

# Test with curl to compare
curl -H "Authorization: Bearer YOUR_TOKEN" http://api.example.com/users
```

### JSON Parsing Errors

```bash
# Check JSON validity
echo '{"name":"John"}' | jq .

# Validate API response
http get http://api.example.com/users --json-output | jq .

# Use raw output
http get http://api.example.com/users --no-pretty
```

## Technical Details

**HTTP Methods:**
- GET — Retrieve data
- POST — Create data
- PUT — Update data
- DELETE — Delete data

**Request Format:**
- URL (required)
- Headers (optional)
- Body (POST/PUT only)
- Query parameters (GET only)

**Response Format:**
- Status code
- Headers
- Body
- Request time
- Success flag

**Timeout:**
- Default: 10 seconds
- Applies to entire request
- Returns error on timeout

## Requirements

- Python 3.6+
- No external dependencies (uses urllib)
- Network connectivity

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Simple. Fast. HTTP.**

API testing made easy with automatic JSON handling.
