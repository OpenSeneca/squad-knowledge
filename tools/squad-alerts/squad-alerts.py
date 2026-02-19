#!/usr/bin/env python3
"""
Squad Alerting System

Proactive monitoring and alerting for all squad agents.
Integrates with squad-dashboard data.json and provides multi-channel notifications.

Usage:
    squad-alerts                    # Monitor continuously
    squad-alerts --check-once         # Check status once and exit
    squad-alerts --daemon            # Run as daemon (background)
    squad-alerts --channels slack email  # Notification channels
    squad-alerts --config alerts.yaml  # Custom config

Alerts on:
- Agent status changes (active → inactive, inactive → active)
- Low activity scores (< 20 for >24h)
- Agent down/offline (no heartbeat for >2h)
- Dashboard server down
- Missing learnings for >48h
"""

import json
import time
import signal
import smtplib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import sys


# Terminal colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# Squad agent configuration
AGENTS = {
    "seneca": {"name": "Seneca", "role": "Coordinator"},
    "marcus": {"name": "Marcus", "role": "Research (AI)"},
    "archimedes": {"name": "Archimedes", "role": "Build"},
    "argus": {"name": "Argus", "role": "Ops"},
    "galen": {"name": "Galen", "role": "Research (Biotech)"},
}


class SquadAlerts:
    """Main alerting system for OpenSeneca squad"""

    def __init__(self, config_path: Optional[Path] = None):
        self.data_file = Path.home() / ".openclaw" / "workspace" / "tools" / "squad-dashboard" / "data.json"
        self.config = self._load_config(config_path) if config_path else self._default_config()
        self.alerts_history: List[Dict] = []
        self.last_agent_states: Dict[str, Dict] = {}
        self.running = True

    def _default_config(self) -> Dict:
        """Default configuration for alerting"""
        return {
            "check_interval": 300,  # 5 minutes
            "dashboard_url": "http://100.100.56.102:8080",
            "alerts": {
                "agent_down": {
                    "enabled": True,
                    "threshold_hours": 2,  # No heartbeat for 2 hours
                },
                "low_activity": {
                    "enabled": True,
                    "threshold_hours": 24,  # >24 hours
                    "min_activity": 20,  # Activity score < 20
                },
                "status_change": {
                    "enabled": True,
                    "notify": True,
                },
                "dashboard_down": {
                    "enabled": True,
                    "threshold_hours": 1,  # No heartbeat for 1 hour
                },
                "missing_learnings": {
                    "enabled": True,
                    "threshold_hours": 48,  # No learnings for 48 hours
                },
            },
            "notifications": {
                "email": {
                    "enabled": False,
                    "smtp_server": "",
                    "smtp_port": 587,
                    "smtp_user": "",
                    "smtp_password": "",
                    "from_address": "",
                    "to_addresses": [],
                },
                "slack": {
                    "enabled": False,
                    "webhook_url": "",
                    "channel": "#alerts",
                },
            },
        }

    def _load_config(self, config_path: Path) -> Dict:
        """Load configuration from file"""
        import yaml
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        return self._default_config()

    def load_agent_status(self) -> Optional[List[Dict]]:
        """Load agent status from squad-dashboard data.json"""
        if not self.data_file.exists():
            return None

        try:
            with open(self.data_file) as f:
                data = json.load(f)
                return data.get("agents", [])
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Could not load agent status: {e}{Colors.RESET}")
            return None

    def check_agent_status(self, agent_id: str, current_status: Dict) -> Dict:
        """Check if agent status has changed and triggers alerts"""
        name = AGENTS[agent_id]["name"]

        # Get previous state
        prev_state = self.last_agent_states.get(agent_id, {
            "status": "unknown",
            "activity": 0,
            "last_output": "",
            "last_updated": datetime.now(timezone.utc).isoformat(),
        })

        # Check for status changes
        alerts = []

        # Agent down (no heartbeat for > threshold hours)
        current_time = datetime.now(timezone.utc)
        last_updated = datetime.fromisoformat(current_status.get("last_updated", current_time.isoformat()))
        hours_since_update = (current_time - last_updated).total_seconds() / 3600

        if hours_since_update > self.config["alerts"]["agent_down"]["threshold_hours"]:
            alerts.append({
                "type": "agent_down",
                "agent": name,
                "severity": "critical",
                "message": f"{name} has been down for {hours_since_update:.1f} hours (last update: {last_updated.strftime('%Y-%m-%d %H:%M')})",
            })

        # Low activity
        if current_status.get("activity", 0) < self.config["alerts"]["low_activity"]["min_activity"]:
            if hours_since_update > self.config["alerts"]["low_activity"]["threshold_hours"]:
                alerts.append({
                    "type": "low_activity",
                    "agent": name,
                    "severity": "warning",
                    "message": f"{name} has low activity score ({current_status.get('activity', 0)}) for {hours_since_update:.1f} hours",
                })

        # Status change
        if self.config["alerts"]["status_change"]["enabled"]:
            if prev_state["status"] != current_status.get("status"):
                alerts.append({
                    "type": "status_change",
                    "agent": name,
                    "severity": "info",
                    "message": f"{name} status changed: {prev_state['status']} → {current_status.get('status')}",
                })

        # Update last state
        self.last_agent_states[agent_id] = {
            "status": current_status.get("status"),
            "activity": current_status.get("activity", 0),
            "last_output": current_status.get("last_output", ""),
            "last_updated": current_status.get("last_updated"),
        }

        return alerts

    def check_dashboard_status(self) -> List[Dict]:
        """Check if squad dashboard is accessible"""
        import requests

        alerts = []

        try:
            response = requests.get(self.config["dashboard_url"], timeout=10)
            if response.status_code != 200:
                alerts.append({
                    "type": "dashboard_down",
                    "severity": "critical",
                    "message": f"Dashboard is down (HTTP {response.status_code}) at {self.config['dashboard_url']}",
                })
        except requests.RequestException as e:
            alerts.append({
                "type": "dashboard_down",
                "severity": "critical",
                "message": f"Dashboard is unreachable: {e}",
            })

        return alerts

    def check_missing_learnings(self, agent_id: str, current_status: Dict) -> List[Dict]:
        """Check if agent has missing learnings"""
        learnings_dir = Path.home() / ".openclaw" / "learnings"

        if not learnings_dir.exists():
            return []

        alerts = []
        name = AGENTS[agent_id]["name"]

        # Find most recent learning for this agent
        agent_learnings = sorted(learnings_dir.glob(f"*-{agent_id}.md"), reverse=True)

        if agent_learnings:
            most_recent = agent_learnings[0]
            hours_old = (datetime.now() - datetime.fromtimestamp(most_recent.stat().st_mtime)).total_seconds() / 3600

            if hours_old > self.config["alerts"]["missing_learnings"]["threshold_hours"]:
                alerts.append({
                    "type": "missing_learnings",
                    "agent": name,
                    "severity": "warning",
                    "message": f"{name} has no learnings for {hours_old:.1f} hours",
                })
        else:
            alerts.append({
                "type": "missing_learnings",
                "agent": name,
                "severity": "warning",
                "message": f"{name} has never produced learnings",
            })

        return alerts

    def send_alert(self, alert: Dict) -> bool:
        """Send alert to configured channels"""
        sent = False

        # Email notification
        if self.config["notifications"]["email"]["enabled"]:
            try:
                sent = self._send_email(alert)
            except Exception as e:
                print(f"{Colors.RED}Failed to send email: {e}{Colors.RESET}")

        # Slack notification
        if self.config["notifications"]["slack"]["enabled"]:
            try:
                sent = sent or self._send_slack(alert)
            except Exception as e:
                print(f"{Colors.RED}Failed to send Slack: {e}{Colors.RESET}")

        # Always print to console
        self._print_alert(alert)

        return sent

    def _send_email(self, alert: Dict) -> bool:
        """Send email alert"""
        email_config = self.config["notifications"]["email"]

        subject = f"[{alert['severity'].upper()}] {alert['type']}: {alert.get('agent', 'Squad')}"
        body = alert["message"]

        msg = f"""Subject: {subject}

{body}
---
Generated by Squad Alerting System
"""

        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(email_config["smtp_user"], email_config["smtp_password"])
            server.sendmail(email_config["from_address"], email_config["to_addresses"], msg.as_string())
            server.quit()

        return True

    def _send_slack(self, alert: Dict) -> bool:
        """Send Slack webhook alert"""
        slack_config = self.config["notifications"]["slack"]

        webhook_url = slack_config["webhook_url"]
        channel = slack_config["channel"]

        message = {
            "text": f"[{alert['severity'].upper()}] {alert['message']}",
            "channel": channel,
            "username": "Squad Alerts",
        }

        import requests
        response = requests.post(webhook_url, json=message, timeout=10)
        return response.status_code == 200

    def _print_alert(self, alert: Dict):
        """Print alert to console with formatting"""
        severity_colors = {
            "critical": Colors.RED,
            "warning": Colors.YELLOW,
            "info": Colors.BLUE,
        }

        color = severity_colors.get(alert["severity"], Colors.RESET)
        severity = alert["severity"].upper()

        print(f"\n{color}[{severity}]{Colors.RESET} {alert['message']}")

    def check_once(self):
        """Run a single check cycle"""
        print(f"\n{Colors.BOLD}Squad Alerting System{Colors.RESET}")
        print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")

        agents = self.load_agent_status()
        all_alerts = []

        if agents:
            for agent in agents:
                agent_id = agent.get("name", "").lower()
                if agent_id in AGENTS:
                    alerts = self.check_agent_status(agent_id, agent)
                    alerts.extend(self.check_missing_learnings(agent_id, agent))

            # Check dashboard status
            dashboard_alerts = self.check_dashboard_status()
            alerts.extend(dashboard_alerts)

            # Send all alerts
            for alert in alerts:
                if alert not in self.alerts_history:
                    self.alerts_history.append(alert)
                    self.send_alert(alert)

            # Trim history (keep last 100)
            self.alerts_history = self.alerts_history[-100:]

            # Summary
            if alerts:
                print(f"\n{Colors.YELLOW}Total alerts generated: {len(alerts)}{Colors.RESET}")
            else:
                print(f"\n{Colors.GREEN}No alerts{Colors.RESET}")

    def run_daemon(self):
        """Run as continuous daemon"""
        print(f"{Colors.BOLD}Starting Squad Alerting System Daemon{Colors.RESET}")
        print(f"Check interval: {self.config['check_interval']} seconds")
        print(f"Press Ctrl+C to stop\n")

        try:
            while self.running:
                self.check_once()
                time.sleep(self.config["check_interval"])
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Stopping daemon...{Colors.RESET}")
            self.running = False

    def save_config_template(self, output_path: Path):
        """Save a default config template to file"""
        import yaml

        template = """# Squad Alerting System Configuration

check_interval: 300  # Check interval in seconds (default: 5 minutes)

# Dashboard URL to monitor
dashboard_url: "http://100.100.56.102:8080"

# Alert thresholds
alerts:
  agent_down:
    enabled: true
    threshold_hours: 2  # Alert if no heartbeat for 2 hours

  low_activity:
    enabled: true
    threshold_hours: 24  # Alert if no activity for 24 hours
    min_activity: 20  # Activity score below 20

  status_change:
    enabled: true  # Alert on agent status changes

  dashboard_down:
    enabled: true
    threshold_hours: 1  # Alert if dashboard down for 1 hour

  missing_learnings:
    enabled: true
    threshold_hours: 48  # Alert if no learnings for 48 hours

# Email notifications (optional)
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

# Slack notifications (optional)
notifications:
  slack:
    enabled: false
    webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    channel: "#alerts"
"""
        output_path.write_text(template)
        print(f"Config template saved to {output_path}")
        print(f"Edit the file to configure your alerts")

    def stop(self):
        """Stop the daemon"""
        self.running = False


def main():
    parser = argparse.ArgumentParser(
        description="Proactive monitoring and alerting for OpenSeneca squad"
    )
    parser.add_argument(
        "--check-once",
        "-c",
        action="store_true",
        help="Check status once and exit",
    )
    parser.add_argument(
        "--daemon",
        "-d",
        action="store_true",
        help="Run as daemon (continuous monitoring)",
    )
    parser.add_argument(
        "--config",
        "-f",
        type=Path,
        help="Path to configuration file (YAML)",
    )
    parser.add_argument(
        "--generate-config",
        "-g",
        type=Path,
        help="Generate config template file",
    )
    args = parser.parse_args()

    # Handle config generation
    if args.generate_config:
        system = SquadAlerts()
        system.save_config_template(args.generate_config)
        sys.exit(0)

    # Create and run alerting system
    system = SquadAlerts(config_path=args.config)

    if args.check_once:
        system.check_once()
    elif args.daemon:
        system.run_daemon()
    else:
        print(f"{Colors.YELLOW}Error: Must specify --check-once or --daemon{Colors.RESET}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
