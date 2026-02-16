# logfind — Log File Search and Analyzer

Search, filter, and analyze log files with powerful patterns and time filters. Essential for debugging and monitoring.

**Location:** `~/workspace/tools/logfind/`

**Install:** Symlink to `~/.local/bin/logfind`

```bash
ln -s ~/workspace/tools/logfind/logfind.py ~/.local/bin/logfind
chmod +x ~/workspace/tools/logfind/logfind.py
```

## Features

- **Pattern Search** — Regex search in log files
- **Level Filtering** — Filter by DEBUG, INFO, WARN, ERROR, etc.
- **Time Filters** — Search within time ranges (relative or absolute)
- **Multiple Files** — Search multiple log files at once
- **Tail Mode** — Show last N lines
- **Grep Mode** — Simple grep without log parsing
- **Statistics** — Analyze log statistics
- **Auto-Detection** — Detect common log formats automatically
- **Colored Output** — Color-coded log levels
- **JSON Output** — Machine-readable output
- **File Prefix** — Show which file each entry is from

## Key Commands

### Basic Search

- `logfind <file>` — Show all log entries
- `logfind <file> -p <pattern>` — Search for pattern
- `logfind <file> -l <level>` — Filter by level
- `logfind <file1> <file2>` — Search multiple files

### Pattern Search

- `logfind app.log -p "ERROR"` — Search for errors
- `logfind app.log -p "timeout|failed"` — Search for patterns
- `logfind app.log -p "user.*login"` — Regex search

### Level Filtering

- `logfind app.log -l ERROR` — Show errors only
- `logfind app.log -l WARN` — Show warnings
- `logfind app.log -l DEBUG` — Show debug messages
- `logfind app.log -l ERROR -l FATAL` — (Note: multiple levels not supported, use pattern)

### Time Filters

- `logfind app.log --after 1h` — Entries from last hour
- `logfind app.log --before 30m` — Entries older than 30 minutes
- `logfind app.log --after "2026-02-16 10:00:00"` — After specific time
- `logfind app.log --after 1h --before 30m` — Time range

### Tail and Head

- `logfind app.log --tail 50` — Last 50 lines
- `logfind app.log --head 20` — First 20 lines

### Grep Mode

- `logfind app.log --grep "ERROR"` — Simple grep
- `logfind app.log --grep "404|500"` — Grep multiple patterns

### Statistics

- `logfind app.log --stats` — Show log statistics
- `logfind app.log,access.log --stats` — Stats for multiple files

### Formatting

- `logfind app.log --show-level` — Show log level
- `logfind app.log --show-time` — Show timestamp
- `logfind app.log --show-file` — Show filename
- `logfind app.log --color` — Force colored output
- `logfind app.log --reverse` — Show newest first
- `logfind app.log --json` — Output as JSON

## Examples

### Search for Errors

```bash
# Find all errors
logfind app.log -l ERROR

# Find errors with pattern
logfind app.log -l ERROR -p "timeout"

# Find errors and fatal messages
logfind app.log -p "ERROR|FATAL"
```

### Time-Based Search

```bash
# Recent errors (last hour)
logfind app.log -l ERROR --after 1h

# Errors from last 30 minutes
logfind app.log -l ERROR --after 30m

# Errors from specific time range
logfind app.log -l ERROR --after "2026-02-16 10:00" --before "2026-02-16 11:00"

# All logs from last day
logfind app.log --after 1d
```

### Pattern Search

```bash
# Search for specific user
logfind app.log -p "user_123"

# Search for API endpoints
logfind app.log -p "/api/.*"

# Search for HTTP status codes
logfind access.log -p " (400|500) "

# Search for exceptions
logfind app.log -p "Exception|Error|Failed"
```

### Multiple Files

```bash
# Search multiple logs
logfind app.log,access.log,errors.log -p "ERROR"

# Search all logs in directory
logfind logs/*.log -l ERROR

# Search specific logs
logfind app-production.log,app-staging.log -p "deploy"
```

### Monitor Logs

```bash
# Watch recent errors
watch -n 5 'logfind app.log -l ERROR --after 5m --tail 20'

# Check for recent issues
logfind app.log -p "ERROR|WARN|timeout" --after 5m

# Quick status check
logfind app.log --tail 10
```

### Analyze Patterns

```bash
# Check statistics
logfind app.log --stats

# See error distribution
logfind app.log -l ERROR --stats

# Check recent activity
logfind app.log --stats --after 1h
```

### Debug Specific Issues

```bash
# Find database errors
logfind app.log -p "database|sql|connection" -l ERROR

# Find authentication failures
logfind app.log -p "auth|login|password" -l ERROR

# Find performance issues
logfind app.log -p "timeout|slow|latency"

# Find API errors
logfind app.log -p "/api/.* (400|500)"
```

### Context and Detail

```bash
# Show with timestamps and levels
logfind app.log -l ERROR --show-time --show-level

# Show which file each entry is from
logfind app.log,errors.log -p "ERROR" --show-file

# Show newest first
logfind app.log -l ERROR --reverse

# Show first 20 errors
logfind app.log -l ERROR --head 20
```

### JSON Output

```bash
# Get JSON output
logfind app.log -l ERROR --json

# Pipe to jq
logfind app.log -l ERROR --json | jq '.[] | .timestamp'

# Save to file
logfind app.log --json > log-analysis.json

# Extract specific data
logfind app.log --json | jq -r '.[] | select(.level == "ERROR") | .raw'
```

### Grep Mode (Fast)

```bash
# Simple grep (faster, no parsing)
logfind app.log --grep "ERROR"

# Grep for multiple patterns
logfind app.log --grep "ERROR|FATAL|CRITICAL"

# Grep in multiple files
logfind *.log --grep "404"
```

## Use Cases

### Troubleshooting Errors

```bash
# Find recent errors
logfind app.log -l ERROR --after 1h

# Find specific error type
logfind app.log -p "ConnectionError|TimeoutError" -l ERROR

# Find errors with stack traces
logfind app.log -p "ERROR.*Traceback"
```

### Monitoring Services

```bash
# Check for errors in last 10 minutes
logfind app.log -l ERROR --after 10m

# Check for warnings
logfind app.log -l WARN --after 10m

# Quick status check
logfind app.log --tail 20
```

### Analyzing Traffic

```bash
# Find 404 errors
logfind access.log -p " 404 "

# Find 500 errors
logfind access.log -p " 500 "

# Find slow requests
logfind access.log -p "latency.*[0-9]{4}"
```

### Debugging Deployments

```bash
# Find deployment-related logs
logfind app.log -p "deploy|restart|shutdown"

# Check logs after deployment
logfind app.log --after 10m

# Find startup issues
logfind app.log -p "startup|init|config" --head 50
```

### Security Auditing

```bash
# Find failed logins
logfind auth.log -p "failed|denied|unauthorized" -l ERROR

# Find suspicious activity
logfind auth.log -p "invalid|unknown|unusual"

# Find security events
logfind app.log -p "security|auth|login|logout"
```

### Performance Analysis

```bash
# Find slow operations
logfind app.log -p "slow|timeout|latency|performance"

# Find database issues
logfind app.log -p "database|sql|connection|pool"

# Find memory issues
logfind app.log -p "memory|oom|heap|gc"
```

### Compliance and Auditing

```bash
# Find user actions
logfind app.log -p "user.*action|user.*deleted|user.*created"

# Find data access
logfind app.log -p "access|read|write|delete"

# Generate audit report
logfind app.log -p "audit|compliance|PII" --after 7d --stats
```

## Integration with Other Tools

### With notes (note taking)

```bash
# Note recent errors
logfind app.log -l ERROR --after 1h | notes add "Recent errors" -c debug

# Note critical issues
logfind app.log -p "CRITICAL|FATAL" | notes add "Critical issues found"
```

### With fwatch (file watcher)

```bash
# Monitor for errors
fwatch -p "app.log" -c "logfind app.log -l ERROR --tail 20"

# Watch logs and alert on errors
fwatch -p "*.log" -c "logfind app.log -l ERROR --after 5m | notes add 'Errors found'"
```

### With run (command runner)

```bash
# Store log check command
run add check-errors "logfind app.log -l ERROR --tail 20"

# Run stored command
run check-errors
```

### With port (port checker)

```bash
# Check service is running
port check localhost 8080

# Then check logs
logfind app.log --tail 20
```

### With httpc (HTTP client)

```bash
# Check API health
httpc get http://api.example.com/health

# Check logs for errors
logfind api.log -l ERROR --after 5m
```

## Log Format Detection

**logfind automatically detects common log formats:**

- **Standard format:** `2026-02-16 12:00:00 [INFO] Message`
- **Bracketed timestamp:** `[2026-02-16 12:00:00] INFO Message`
- **Timestamp prefix:** `timestamp=2026-02-16T12:00:00 INFO Message`
- **US date format:** `02/16/2026 12:00:00 INFO Message`

**Supported log levels:**
- DEBUG
- INFO
- WARN / WARNING
- ERROR
- FATAL
- CRITICAL
- TRACE

## Best Practices

### Time-Based Filtering

**Use relative time for monitoring:**
```bash
# Recent errors
logfind app.log -l ERROR --after 5m

# Last hour
logfind app.log -l ERROR --after 1h

# Last day
logfind app.log --after 1d
```

**Use absolute time for analysis:**
```bash
# Specific incident
logfind app.log --after "2026-02-16 10:00" --before "2026-02-16 11:00"

# Deployment window
logfind app.log --after "2026-02-16 09:00" --before "2026-02-16 09:30"
```

### Pattern Matching

**Use specific patterns:**
```bash
# Good (specific)
logfind app.log -p "user_123"

# Too broad
logfind app.log -p "user"
```

**Combine with level filtering:**
```bash
# Find specific errors
logfind app.log -l ERROR -p "timeout"

# Find all critical messages
logfind app.log -p "CRITICAL|FATAL"
```

### Performance

**Use tail for quick checks:**
```bash
# Fast: just last lines
logfind app.log --tail 20

# Slower: parse all logs
logfind app.log
```

**Use grep for simple searches:**
```bash
# Fast: no parsing
logfind app.log --grep "ERROR"

# Slower: parse timestamps and levels
logfind app.log -p "ERROR"
```

## Troubleshooting

### No Results Found

**Check file exists:**
```bash
ls -la app.log
```

**Check permissions:**
```bash
cat app.log | head 10
```

**Try broader search:**
```bash
# Too specific
logfind app.log -p "user_123 ERROR timeout"

# Broader
logfind app.log -p "timeout"
```

### Timestamps Not Detected

**Check log format:**
```bash
head -10 app.log
```

**If timestamps not standard, use grep:**
```bash
logfind app.log --grep "your pattern"
```

### Performance Issues

**For large log files:**
```bash
# Use tail
logfind app.log --tail 100

# Use grep (faster)
logfind app.log --grep "ERROR"

# Use time filters
logfind app.log --after 1h
```

**For many files:**
```bash
# Search specific files
logfind app-production.log -p "ERROR"

# Instead of
logfind *.log -p "ERROR"
```

## Comparison to Alternatives

**vs `grep`:**
- `grep`: Faster, more flexible
- `logfind`: Parses timestamps, levels, colored output

**vs `awk`:**
- `awk`: More powerful for complex processing
- `logfind`: Simpler, log-specific features

**vs `journalctl`:**
- `journalctl`: Systemd logs only
- `logfind`: Any log file

## Technical Details

**Log Parsing:**
- Detects common timestamp formats
- Detects log level patterns
- Falls back to raw text if not detected

**Time Parsing:**
- Supports ISO format (2026-02-16T12:00:00)
- Supports space format (2026-02-16 12:00:00)
- Supports relative format (1h, 30m, 1d)

**Regex Support:**
- Uses Python's `re` module
- Case-insensitive by default
- Supports all regex patterns

## Requirements

- Python 3.6+
- No external dependencies
- Log files (any format)

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Search. Analyze. Understand.**

Log analysis made simple with intelligent parsing and powerful filtering.
