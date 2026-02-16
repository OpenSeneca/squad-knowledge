# proc — Process Manager

View, search, filter, and manage processes. Enhanced ps alternative with colorized output and powerful filtering.

**Location:** `~/workspace/tools/proc/`

**Install:** Symlink to `~/.local/bin/proc`

```bash
ln -s ~/workspace/tools/proc/proc.py ~/.local/bin/proc
chmod +x ~/workspace/tools/proc/proc.py
```

## Features

- **Process Listing** — View all running processes
- **Search** — Search by pattern (regex)
- **Filters** — Filter by user, PID, command, CPU, memory
- **Top Processes** — Show top N processes by CPU
- **Process Killing** — Kill processes (SIGTERM/SIGKILL)
- **Statistics** — Calculate process statistics
- **JSON Output** — Machine-readable output
- **Colorized Output** — Easy to read terminal output

## Key Commands

### List Processes

- `proc` — List all processes
- `proc --top <n>` — Show top N processes by CPU
- `proc --search <pattern>` — Search for processes
- `proc --user <user>` — Filter by user
- `proc --pid <pid>` — Show specific process
- `proc --command <cmd>` — Filter by command

### Advanced Filters

- `proc --min-cpu <cpu>` — Filter by minimum CPU %
- `proc --min-mem <mem>` — Filter by minimum memory %
- `proc --search <pattern> --min-cpu <cpu>` — Combine filters

### Process Management

- `proc --kill <pid>` — Kill process (SIGTERM)
- `proc --kill <pid> --force` — Force kill (SIGKILL)
- `proc --kill <pid1> <pid2>` — Kill multiple processes

### Output Options

- `proc --stats` — Show statistics
- `proc --json` — Output as JSON
- `proc --no-color` — Disable color output

## Examples

### List All Processes

```bash
# List all processes
proc

# Show top 20 processes
proc --top 20

# Show top 10 processes
proc --top 10
```

### Search Processes

```bash
# Search for Python processes
proc --search python

# Search for Node.js processes
proc --search node

# Search for processes with "api" in name
proc --search api

# Regex search
proc --search "python.*server"
```

### Filter by User

```bash
# Show user processes
proc --user exedev

# Show root processes
proc --user root

# Show all users
proc
```

### Filter by PID

```bash
# Show specific process
proc --pid 1234

# Check if process exists
proc --pid 1234
```

### Filter by Command

```bash
# Show bash processes
proc --command bash

# Show sshd processes
proc --command sshd

# Show nginx processes
proc --command nginx
```

### Filter by CPU Usage

```bash
# Show processes using >5% CPU
proc --min-cpu 5.0

# Show CPU hogs
proc --min-cpu 10.0

# Find the heaviest process
proc --min-cpu 50.0
```

### Filter by Memory Usage

```bash
# Show processes using >10% memory
proc --min-mem 10.0

# Show memory hogs
proc --min-mem 20.0

# Find memory leaks
proc --min-mem 30.0
```

### Combine Filters

```bash
# Python processes using >5% CPU
proc --search python --min-cpu 5.0

# User processes using >10% memory
proc --user exedev --min-mem 10.0

# Node.js processes using >1% CPU
proc --search node --min-cpu 1.0
```

### Kill Processes

```bash
# Kill specific process
proc --kill 1234

# Force kill
proc --kill 1234 --force

# Kill multiple processes
proc --kill 1234 5678 9012

# Kill hung process
proc --search "hung.*process" --json | jq '.[].pid' | xargs proc --kill
```

### Statistics

```bash
# Show process statistics
proc --stats

# Statistics with filters
proc --min-cpu 5.0 --stats

# User statistics
proc --user exedev --stats
```

### JSON Output

```bash
# Get all processes as JSON
proc --json

# Filter and get JSON
proc --search python --json

# Pipe to jq
proc --json | jq '.[] | select(.cpu > 5.0)'

# Extract PIDs
proc --search node --json | jq -r '.[].pid'
```

## Use Cases

### Find CPU-Hungry Processes

```bash
# Find processes using >10% CPU
proc --min-cpu 10.0

# Top CPU consumers
proc --top 10

# Find Python CPU hogs
proc --search python --min-cpu 5.0
```

### Find Memory Leaks

```bash
# Find processes using >20% memory
proc --min-mem 20.0

# Find memory hogs
proc --min-mem 30.0

# Top memory consumers
proc --min-mem 10.0 --top 10
```

### Monitor Applications

```bash
# Monitor Node.js apps
proc --search node

# Monitor Python apps
proc --search python

# Monitor web servers
proc --search "nginx|apache"
```

### Kill Hung Processes

```bash
# Kill specific hung process
proc --search "hung" --json | jq -r '.[].pid' | xargs proc --kill

# Force kill hung process
proc --search "hung" --json | jq -r '.[].pid' | xargs proc --kill --force
```

### Debug Performance Issues

```bash
# Find resource hogs
proc --min-cpu 10.0 --min-mem 10.0

# Check process count
proc --stats

# Find unexpected processes
proc | grep -i "malware|virus|crypto"
```

### System Monitoring

```bash
# Quick system status
proc --stats

# Watch top processes
watch -n 5 'proc --top 20'

# Monitor user processes
proc --user exedev --stats
```

### Process Cleanup

```bash
# Kill all Python processes
proc --search python --json | jq -r '.[].pid' | xargs proc --kill

# Kill all Node.js processes
proc --search node --json | jq -r '.[].pid' | xargs proc --kill --force

# Kill old processes
proc --json | jq '.[] | select(.time | split(":")[0] | tonumber > 24) | .pid'
```

### Integration with Other Tools

### With notes (note taking)

```bash
# Note CPU hogs
proc --min-cpu 10.0 | notes add "CPU hogs found"

# Note memory issues
proc --min-mem 20.0 | notes add "Memory hogs"
```

### With run (command runner)

```bash
# Store monitoring command
run add monitor-cpu "proc --min-cpu 10.0"

# Run stored command
run monitor-cpu
```

### With fwatch (file watcher)

```bash
# Watch for high CPU
fwatch -p "monitor.log" -c "proc --min-cpu 20.0 >> monitor.log"
```

### With port (port checker)

```bash
# Check port, then find process
port check localhost 3000
proc --command "node.*3000"
```

### With httpc (HTTP client)

```bash
# Check API health
httpc get http://api.example.com/health

# Check process status
proc --search "api.*server"
```

## Output Format

```
     PID USER      CPU%  MEM%  TIME     COMMAND
   1234 exedev    5.2   3.1  00:01:23 python server.py
   5678 root       2.1   1.5  01:23:45 nginx: master
```

- **PID** — Process ID
- **USER** — Process owner
- **CPU%** — CPU usage percentage
- **MEM%** — Memory usage percentage
- **TIME** — Total CPU time
- **COMMAND** — Process command

## Best Practices

### Finding Resource Hogs

**Use CPU filter:**
```bash
# Find CPU hogs
proc --min-cpu 10.0

# Find extreme CPU usage
proc --min-cpu 50.0
```

**Use memory filter:**
```bash
# Find memory hogs
proc --min-mem 20.0

# Find extreme memory usage
proc --min-mem 50.0
```

### Killing Processes Safely

**Use SIGTERM first:**
```bash
# Try graceful shutdown
proc --kill 1234

# Wait, then force if needed
proc --kill 1234 --force
```

**Use JSON for complex operations:**
```bash
# Find and kill safely
proc --search "node.*api" --json | jq -r '.[].pid' | xargs proc --kill
```

### Monitoring

**Use watch for continuous monitoring:**
```bash
# Monitor top processes
watch -n 5 'proc --top 20'

# Monitor CPU hogs
watch -n 5 'proc --min-cpu 10.0'
```

**Use stats for quick overview:**
```bash
# Quick system status
proc --stats

# User process stats
proc --user exedev --stats
```

### Searching

**Use specific patterns:**
```bash
# Good (specific)
proc --search "python.*server"

# Too broad
proc --search python
```

**Combine with filters:**
```bash
# Find specific CPU hog
proc --search python --min-cpu 5.0

# Find user's memory hogs
proc --user exedev --min-mem 10.0
```

## Troubleshooting

### Permission Denied

**Check permissions:**
```bash
# Check if you can kill the process
ps -p 1234 -o user=

# Kill as root
sudo proc --kill 1234
```

### Process Not Found

**Check if process exists:**
```bash
# Search for process
proc --search "your-app"

# Check specific PID
proc --pid 1234
```

### No Processes Found

**Check filters:**
```bash
# Remove filters
proc

# Try broader search
proc --search "part-of-name"

# Check all processes
proc --stats
```

## Comparison to Alternatives

**vs `ps`:**
- `ps`: More features, more complex
- `proc`: Simpler, colorized, better filtering

**vs `htop`:**
- `htop`: Interactive, more features
- `proc`: Command-line, simple

**vs `top`:**
- `top`: Interactive, auto-refresh
- `proc`: Command-line, no refresh

## Technical Details

**Process Information:**
- Uses `ps aux` command
- Shows all processes (not just yours)
- Shows CPU and memory percentages
- Shows process time

**Signal Handling:**
- SIGTERM: Graceful termination
- SIGKILL: Immediate termination
- Requires appropriate permissions

**Statistics:**
- Calculates aggregate statistics
- Shows top CPU and memory consumers
- Shows process counts

## Requirements

- Python 3.6+
- No external dependencies
- Linux/Unix system (ps command)

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**View. Filter. Control.**

Process management made simple with powerful search and filtering.
