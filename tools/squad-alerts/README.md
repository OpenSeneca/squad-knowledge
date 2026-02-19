# Squad Alerting System

Proactive monitoring and alerting for all OpenSeneca squad agents.

## What It Does

- **Continuous monitoring** of all 5 squad agents (Seneca, Marcus, Archimedes, Argus, Galen)
- **Multi-channel notifications** - Email, Slack, console
- **Smart alerts** on:
  - Agent down/offline (no heartbeat for >2 hours)
  - Low activity scores (< 20 for > 24 hours)
  - Status changes (active ↔ inactive)
  - Dashboard server down (no heartbeat for >1 hour)
  - Missing learnings (no learnings for > 48 hours)
- **Configurable thresholds** - Customize all alert triggers
- **Daemon mode** - Run as background process
- **One-shot mode** - Check once and exit

## Why This Tool

The squad dashboard provides monitoring, but **no proactive alerts**. Justin only knows something is wrong when he manually checks. This tool:
- Alerts you immediately when agents go down
- Warns about low activity before problems escalate
- Notifies on dashboard outages
- Tracks agent status changes proactively
- Monitors for missing learnings

## Usage

```bash
# Generate config template
squad-alerts --generate-config alerts.yaml

# Check once and exit
squad-alerts --check-once

# Run as daemon (continuous monitoring)
squad-alerts --daemon --config alerts.yaml

# Specify notification channels
squad-alerts --daemon --config alerts.yaml --channels slack email

# Stop daemon (Ctrl+C in daemon process)
```

## Configuration

Default config (generate with `--generate-config`):

```yaml
check_interval: 300  # Check interval in seconds (default: 5 minutes)

dashboard_url: "http://100.100.56.102:8080"

alerts:
  agent_down:
    enabled: true
    threshold_hours: 2

  low_activity:
    enabled: true
    threshold_hours: 24
    min_activity: 20

  status_change:
    enabled: true

  dashboard_down:
    enabled: true
    threshold_hours: 1

  missing_learnings:
    enabled: true
    threshold_hours: 48

notifications:
  email:
    enabled: false
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    smtp_user: "your-email@gmail.com"
    smtp_password: "your-app-password"
    from_address: "squad-alerts@example.com"
    to_addresses:
      - "justin@example.com"

  slack:
    enabled: false
    webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    channel: "#alerts"
```

## Alert Types

### Critical Alerts
- **agent_down** - Agent has no heartbeat for >2 hours
- **dashboard_down** - Squad dashboard unreachable

### Warning Alerts
- **low_activity** - Agent activity score <20 for >24 hours
- **missing_learnings** - Agent has no learnings for >48 hours

### Info Alerts
- **status_change** - Agent status changed (active ↔ inactive)

## Dependencies

- Python 3.8+
- squad-dashboard data file (for agent status)
- Optional: SMTP server (for email alerts)
- Optional: Slack webhook (for Slack alerts)
- Optional: PyYAML (`pip install pyyaml`)

## Daemon Mode

```bash
# Start monitoring in background
squad-alerts --daemon &

# View logs
# Logs are printed to console
# Consider redirecting to file:
squad-alerts --daemon > alerts.log 2>&1 &
```

## Use Cases

1. **Production monitoring** - Run as daemon on forge or production server
2. **Development testing** - Use `--check-once` during development
3. **Email alerts** - Configure SMTP for email notifications
4. **Slack integration** - Configure webhook for team notifications
5. **Custom thresholds** - Adjust alert thresholds per squad needs

## Integration

Works with:
- **squad-dashboard** - Reads agent status from data.json
- **squad-learnings** - Checks for missing learnings
- **squad-overview** - Complements overview with alerting

## Deployment

```bash
# Install
cd ~/workspace/tools/squad-alerts
ln -sf "$(pwd)/squad-alerts.py" ~/.local/bin/squad-alerts

# Generate config
squad-alerts --generate-config ~/alerts.yaml

# Edit config
nano ~/alerts.yaml

# Start daemon
squad-alerts --daemon --config ~/alerts.yaml
```

## Files

- `squad-alerts.py` - Main script (500+ lines)
- `README.md` - This file

## License

MIT

## Author

Archimedes (Build Agent) - OpenSeneca Squad
