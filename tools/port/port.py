#!/usr/bin/env python3
"""
port — Port Checker and Scanner

Check if ports are open, scan hosts, test connectivity.
"""

import socket
import sys
import argparse
import json
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
import time
import concurrent.futures
from pathlib import Path


class PortChecker:
    """Port checker and scanner."""

    def __init__(self, timeout: float = 2.0):
        self.timeout = timeout
        self.common_ports = {
            # Web servers
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            587: 'SMTP (submission)',
            631: 'CUPS',
            993: 'IMAPS',
            995: 'POP3S',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5672: 'RabbitMQ',
            6379: 'Redis',
            8000: 'HTTP (alt)',
            8080: 'HTTP (proxy)',
            8443: 'HTTPS (alt)',
            9000: 'HTTP (alt)',
            27017: 'MongoDB',
            3000: 'Node.js',
            5000: 'Flask',
            5001: 'AirPlay',
            5432: 'PostgreSQL',
            5900: 'VNC',
            6443: 'Kubernetes API',
            9000: 'SonarQube',
            9200: 'Elasticsearch',
        }

    def is_open(self, host: str, port: int) -> Tuple[bool, Optional[str]]:
        """Check if a single port is open."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                return True, None
            else:
                return False, None
        except socket.gaierror as e:
            return False, f"DNS resolution failed: {e}"
        except socket.timeout:
            return False, f"Connection timeout"
        except Exception as e:
            return False, f"Error: {e}"

    def check_port(self, host: str, port: int, verbose: bool = False) -> Dict:
        """Check a single port and return details."""
        is_open, error = self.is_open(host, port)

        result = {
            'host': host,
            'port': port,
            'service': self.common_ports.get(port, 'unknown'),
            'open': is_open,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }

        return result

    def scan_ports(self, host: str, ports: List[int], threads: int = 10) -> List[Dict]:
        """Scan multiple ports."""
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.check_port, host, port): port for port in ports}
            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        'host': host,
                        'port': port,
                        'service': 'unknown',
                        'open': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })

        return results

    def scan_common(self, host: str) -> List[Dict]:
        """Scan common ports."""
        return self.scan_ports(host, list(self.common_ports.keys()))

    def scan_range(self, host: str, start: int, end: int, threads: int = 50) -> List[Dict]:
        """Scan a range of ports."""
        ports = list(range(start, end + 1))
        return self.scan_ports(host, ports, threads)

    def scan_multiple_hosts(self, hosts: List[str], ports: List[int], threads: int = 20) -> List[Dict]:
        """Scan multiple hosts."""
        all_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(self.check_port, host, port): (host, port)
                for host in hosts
                for port in ports
            }
            for future in concurrent.futures.as_completed(futures):
                host, port = futures[future]
                try:
                    result = future.result()
                    all_results.append(result)
                except Exception as e:
                    all_results.append({
                        'host': host,
                        'port': port,
                        'service': 'unknown',
                        'open': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })

        return all_results


def format_result(result: Dict, show_closed: bool = False, show_errors: bool = True) -> str:
    """Format a single result."""
    if not result['open']:
        if show_closed:
            status = "❌ Closed"
            service = f" ({result['service']})" if result['service'] != 'unknown' else ""
            if result['error'] and show_errors:
                return f"{result['host']}:{result['port']}{service} — {status} ({result['error']})"
            else:
                return f"{result['host']}:{result['port']}{service} — {status}"
        else:
            return ""

    status = "✅ Open"
    service = f" — {result['service']}" if result['service'] != 'unknown' else ""
    return f"{result['host']}:{result['port']}{service} — {status}"


def main():
    parser = argparse.ArgumentParser(
        description='port — Port Checker and Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  port check 100.93.69.117 80
  port check 100.93.69.117 80,443,3000
  port scan 100.93.69.117 --common
  port scan 100.93.69.117 --range 1 1000
  port scan 100.93.69.117 --range 8000 9000
  port scan 100.93.69.117 22,80,443,8080
  port scan 100.93.69.117,100.98.223.103 22,80,443

Common Use Cases:
  - Check if a specific port is open
  - Scan common ports on a host
  - Scan a range of ports
  - Scan multiple hosts
  - Find open services
  - Troubleshoot connectivity
        """
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Check command
    check_parser = subparsers.add_parser('check', help='Check if ports are open')
    check_parser.add_argument('host', help='Host to check')
    check_parser.add_argument('ports', help='Port(s) to check (comma-separated or range)')
    check_parser.add_argument('--timeout', type=float, default=2.0,
                           help='Connection timeout in seconds (default: 2.0)')
    check_parser.add_argument('--json', action='store_true',
                           help='Output as JSON')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan ports on a host')
    scan_parser.add_argument('hosts', help='Host(s) to scan (comma-separated)')
    scan_parser.add_argument('--ports', help='Ports to scan (comma-separated)')
    scan_parser.add_argument('--range', nargs=2, type=int, metavar=('START', 'END'),
                          help='Port range to scan')
    scan_parser.add_argument('--common', action='store_true',
                          help='Scan common ports')
    scan_parser.add_argument('--threads', type=int, default=10,
                          help='Number of threads (default: 10)')
    scan_parser.add_argument('--timeout', type=float, default=2.0,
                          help='Connection timeout in seconds (default: 2.0)')
    scan_parser.add_argument('--show-closed', action='store_true',
                          help='Show closed ports')
    scan_parser.add_argument('--json', action='store_true',
                          help='Output as JSON')

    # List common ports
    list_parser = subparsers.add_parser('list', help='List common ports')
    list_parser.add_argument('--port', type=int,
                          help='Get service name for a port')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    checker = PortChecker(timeout=args.timeout if hasattr(args, 'timeout') else 2.0)

    # Check command
    if args.command == 'check':
        # Parse ports
        ports = []
        for part in args.ports.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))

        results = []
        for port in ports:
            result = checker.check_port(args.host, port)
            results.append(result)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"🔍 Checking {args.host}...\n")
            for result in results:
                print(format_result(result, show_closed=True, show_errors=True))

        return 0

    # Scan command
    elif args.command == 'scan':
        hosts = [h.strip() for h in args.hosts.split(',')]

        # Determine ports to scan
        if args.common:
            ports = list(checker.common_ports.keys())
        elif args.range:
            ports = list(range(args.range[0], args.range[1] + 1))
        elif args.ports:
            ports = []
            for part in args.ports.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    ports.extend(range(start, end + 1))
                else:
                    ports.append(int(part))
        else:
            print("❌ Please specify --common, --range, or --ports")
            return 1

        # Scan
        if len(hosts) == 1:
            results = checker.scan_ports(hosts[0], ports, threads=args.threads)
        else:
            results = checker.scan_multiple_hosts(hosts, ports, threads=args.threads)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"🔍 Scanning {len(hosts)} host(s) for {len(ports)} port(s)...\n")

            # Group results by host
            by_host = {}
            for result in results:
                host = result['host']
                if host not in by_host:
                    by_host[host] = []
                by_host[host].append(result)

            # Print results
            for host, host_results in by_host.items():
                print(f"📡 {host}:\n")

                # Find open ports first
                open_ports = [r for r in host_results if r['open']]
                if open_ports:
                    print(f"  Open ports:")
                    for result in open_ports:
                        print(f"    {format_result(result)}")
                    print()
                else:
                    print(f"  ❌ No open ports found\n")

                # Show closed if requested
                if args.show_closed:
                    closed_ports = [r for r in host_results if not r['open']]
                    print(f"  Closed ports:")
                    for result in closed_ports:
                        print(f"    {format_result(result, show_closed=True)}")
                    print()

        return 0

    # List command
    elif args.command == 'list':
        if args.port:
            service = checker.common_ports.get(args.port, 'unknown')
            print(f"{args.port}: {service}")
        else:
            print("📋 Common Ports:\n")
            for port, service in sorted(checker.common_ports.items()):
                print(f"  {port:5d} — {service}")

        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
