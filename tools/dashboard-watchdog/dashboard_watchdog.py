#!/usr/bin/env python3
"""
Dashboard Watchdog - Auto-restart squad-dashboard when it goes down.

Monitors squad-dashboard at configured URL and restarts it automatically
if it becomes unresponsive. Logs all restarts for troubleshooting.

Usage:
    dashboard-watchdog [options]

Options:
    --url URL           Dashboard URL to monitor (default: http://localhost:8080)
    --interval SECONDS   Check interval in seconds (default: 60)
    --max-restarts N     Maximum number of auto-restarts before giving up (default: 10)
    --log-file PATH     Log file path (default: /tmp/dashboard-watchdog.log)
    --dry-run          Show what would happen without taking action
    --help              Show this help message
"""

import argparse
import time
import logging
import subprocess
import sys
import requests
from datetime import datetime
from pathlib import Path


class DashboardWatchdog:
    """Monitor and auto-restart squad-dashboard."""
    
    def __init__(self, url: str, interval: int, max_restarts: int, 
                 log_file: str, dry_run: bool = False):
        self.url = url
        self.interval = interval
        self.max_restarts = max_restarts
        self.log_file = log_file
        self.dry_run = dry_run
        self.restart_count = 0
        self.last_up_time = datetime.now()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('DashboardWatchdog')
    
    def check_dashboard(self) -> bool:
        """Check if dashboard is responding."""
        try:
            response = requests.get(
                f"{self.url}/api/status",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"Dashboard UP - Agents: {len(data.get('agents', []))}")
                return True
            else:
                self.logger.warning(f"Dashboard DOWN - Status code: {response.status_code}")
                return False
        except requests.RequestException as e:
            self.logger.warning(f"Dashboard DOWN - Request failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Dashboard check error: {e}")
            return False
    
    def restart_dashboard(self) -> bool:
        """Restart the dashboard."""
        if self.restart_count >= self.max_restarts:
            self.logger.error(f"Max restarts ({self.max_restarts}) reached. Giving up.")
            return False
        
        self.restart_count += 1
        self.logger.info(f"Restart attempt #{self.restart_count}")
        
        if self.dry_run:
            self.logger.info("[DRY RUN] Would restart dashboard")
            return True
        
        try:
            # Kill existing node processes on port 8080
            subprocess.run(
                ["pkill", "-f", "node.*server.js"],
                stderr=subprocess.DEVNULL
            )
            time.sleep(2)
            
            # Start dashboard with nohup
            subprocess.Popen(
                [
                    "nohup", "node", "server.js",
                    ">", "/tmp/dashboard.log", "2>&1", "&"
                ],
                cwd="/home/exedev/.openclaw/workspace/tools/squad-dashboard",
                env={"PORT": "8080"},
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            self.logger.info("Dashboard restarted successfully")
            self.last_up_time = datetime.now()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restart dashboard: {e}")
            return False
    
    def get_uptime(self) -> float:
        """Get uptime in minutes since last successful check."""
        uptime = datetime.now() - self.last_up_time
        return uptime.total_seconds() / 60
    
    def run(self):
        """Main monitoring loop."""
        self.logger.info(f"Starting dashboard watchdog for {self.url}")
        self.logger.info(f"Check interval: {self.interval}s")
        self.logger.info(f"Max restarts: {self.max_restarts}")
        self.logger.info(f"Dry run: {self.dry_run}")
        
        try:
            # Initial check
            if self.check_dashboard():
                self.logger.info("Dashboard is up and running")
            else:
                self.logger.warning("Dashboard is down on startup")
                if self.restart_dashboard():
                    # Wait for dashboard to stabilize
                    time.sleep(10)
            
            # Main monitoring loop
            while True:
                time.sleep(self.interval)
                
                if not self.check_dashboard():
                    uptime_min = self.get_uptime()
                    self.logger.warning(f"Dashboard down after {uptime_min:.1f} minutes uptime")
                    
                    if self.restart_dashboard():
                        # Wait for dashboard to stabilize
                        time.sleep(10)
                    else:
                        self.logger.error("Failed to restart dashboard. Exiting.")
                        break
                else:
                    self.last_up_time = datetime.now()
                    
        except KeyboardInterrupt:
            self.logger.info("Watchdog stopped by user")
        except Exception as e:
            self.logger.error(f"Watchdog error: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Dashboard Watchdog - Auto-restart squad-dashboard when it goes down',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Monitor dashboard with defaults
  dashboard-watchdog

  # Monitor every 30 seconds, max 5 restarts
  dashboard-watchdog --interval 30 --max-restarts 5

  # Dry run to test without taking action
  dashboard-watchdog --dry-run

  # Monitor custom URL with custom log file
  dashboard-watchdog --url http://localhost:3000 --log-file /var/log/dashboard-watchdog.log
"""
    )
    
    parser.add_argument(
        '--url',
        default='http://localhost:8080',
        help='Dashboard URL to monitor (default: http://localhost:8080)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Check interval in seconds (default: 60)'
    )
    parser.add_argument(
        '--max-restarts',
        type=int,
        default=10,
        help='Maximum number of auto-restarts (default: 10)'
    )
    parser.add_argument(
        '--log-file',
        default='/tmp/dashboard-watchdog.log',
        help='Log file path (default: /tmp/dashboard-watchdog.log)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would happen without taking action'
    )
    
    args = parser.parse_args()
    
    watchdog = DashboardWatchdog(
        url=args.url,
        interval=args.interval,
        max_restarts=args.max_restarts,
        log_file=args.log_file,
        dry_run=args.dry_run
    )
    
    watchdog.run()


if __name__ == '__main__':
    main()
