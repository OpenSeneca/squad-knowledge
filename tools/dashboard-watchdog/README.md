# Dashboard Watchdog

Auto-restart squad-dashboard when it goes down.

## Problem

The squad-dashboard has a persistent stability issue where it stops every ~27 minutes, requiring manual intervention to restart. This tool automatically monitors the dashboard and restarts it when it becomes unresponsive.

## Features

- **Automatic monitoring** - Continuously checks dashboard status
- **Auto-restart** - Restarts dashboard when it goes down
- **Configurable intervals** - Check every N seconds (default: 60)
- **Max restarts** - Give up after N restarts (default: 10)
- **Dry run mode** - Test without taking action
- **Logging** - Detailed logs for troubleshooting
- **Uptime tracking** - Know how long dashboard stays up

## Installation

```bash
# Clone or copy to workspace
cd /home/exedev/.openclaw/workspace/tools/dashboard-watchdog

# Make executable
chmod +x dashboard_watchdog.py

# (Optional) Install system-wide
sudo ln -s $(pwd)/dashboard_watchdog.py /usr/local/bin/dashboard-watchdog
```

## Usage

### Basic Usage
```bash
# Monitor with defaults (localhost:8080, check every 60s, max 10 restarts)
dashboard-watchdog
```

### Custom Configuration
```bash
# Check every 30 seconds, max 5 restarts
dashboard-watchdog --interval 30 --max-restarts 5

# Monitor custom URL
dashboard-watchdog --url http://localhost:3000

# Custom log file
dashboard-watchdog --log-file /var/log/dashboard-watchdog.log
```

### Dry Run (Test Mode)
```bash
# Test without taking action
dashboard-watchdog --dry-run
```

## Options

| Option | Default | Description |
|---------|-----------|-------------|
| `--url` | `http://localhost:8080` | Dashboard URL to monitor |
| `--interval` | `60` | Check interval in seconds |
| `--max-restarts` | `10` | Maximum auto-restarts before giving up |
| `--log-file` | `/tmp/dashboard-watchdog.log` | Log file path |
| `--dry-run` | `false` | Show what would happen without taking action |

## How It Works

1. **Monitoring Loop**: Checks dashboard API status every N seconds
2. **Failure Detection**: Detects when dashboard is down (HTTP errors, timeouts)
3. **Auto-Restart**: Kills existing node process and starts new one with nohup
4. **Stabilization Wait**: Waits 10 seconds after restart to let dashboard stabilize
5. **Max Restarts**: Gives up after N restarts to prevent infinite loops

## Logs

All activity logged to:
- **Console output** (real-time monitoring)
- **Log file** (`/tmp/dashboard-watchdog.log` by default)

Log format:
```
2026-02-23 08:45:00 - INFO - Dashboard UP - Agents: 5
2026-02-23 08:52:00 - WARNING - Dashboard DOWN - Request failed
2026-02-23 08:52:00 - INFO - Restart attempt #1
2026-02-23 08:52:05 - INFO - Dashboard restarted successfully
```

## Use Cases

### Production Deployment
```bash
# Run as background service with systemd
nohup dashboard-watchdog --interval 60 --max-restarts 10 > /tmp/watchdog.log 2>&1 &
```

### Testing
```bash
# Dry run to see what would happen
dashboard-watchdog --dry-run --interval 30
```

### Development
```bash
# Quick testing with verbose output
dashboard-watchdog --interval 10
```

## Troubleshooting

### Dashboard Not Restarting
- Check if `pkill` command is available
- Verify dashboard path: `/home/exedev/.openclaw/workspace/tools/squad-dashboard`
- Check log file: `/tmp/dashboard-watchdog.log`

### Max Restarts Reached
- Indicates persistent issue with dashboard stability
- Increase `--max-restarts` limit if needed
- Investigate root cause of dashboard crashes

### Permission Errors
- Ensure `pkill` can kill node processes: check permissions
- Verify directory access for dashboard startup

## Requirements

- Python 3.7+
- requests library (`pip install requests`)

## License

MIT

## Author

Archimedes - Engineering arm of the OpenSeneca squad

---

**Use this tool to solve the CRITICAL dashboard stability issue!**
