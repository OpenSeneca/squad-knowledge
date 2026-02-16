#!/usr/bin/env python3
"""
dns — DNS Lookup Tool

Query DNS records (A, AAAA, MX, NS, TXT, CNAME, SOA).
"""

import sys
import argparse
import socket
from typing import List, Optional, Dict, Any
import subprocess


class DNSTool:
    """DNS lookup tool."""

    def __init__(self):
        self.record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']

    def resolve(self, domain: str, record_type: str = 'A') -> List[str]:
        """Resolve DNS record."""
        record_type = record_type.upper()

        if record_type == 'A':
            return self._resolve_a(domain)
        elif record_type == 'AAAA':
            return self._resolve_aaaa(domain)
        elif record_type == 'MX':
            return self._resolve_mx(domain)
        elif record_type == 'NS':
            return self._resolve_ns(domain)
        elif record_type == 'TXT':
            return self._resolve_txt(domain)
        elif record_type == 'CNAME':
            return self._resolve_cname(domain)
        elif record_type == 'SOA':
            return self._resolve_soa(domain)
        else:
            return []

    def _resolve_a(self, domain: str) -> List[str]:
        """Resolve A record."""
        try:
            result = socket.getaddrinfo(domain, None)
            return list({addr[4][0] for addr in result if addr[0] == socket.AF_INET})
        except Exception:
            return []

    def _resolve_aaaa(self, domain: str) -> List[str]:
        """Resolve AAAA record."""
        try:
            result = socket.getaddrinfo(domain, None)
            return list({addr[4][0] for addr in result if addr[0] == socket.AF_INET6})
        except Exception:
            return []

    def _resolve_mx(self, domain: str) -> List[str]:
        """Resolve MX record using dig."""
        try:
            result = subprocess.run(
                ['dig', '+short', 'MX', domain],
                capture_output=True,
                text=True,
                timeout=10
            )
            return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            return []

    def _resolve_ns(self, domain: str) -> List[str]:
        """Resolve NS record using dig."""
        try:
            result = subprocess.run(
                ['dig', '+short', 'NS', domain],
                capture_output=True,
                text=True,
                timeout=10
            )
            return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            return []

    def _resolve_txt(self, domain: str) -> List[str]:
        """Resolve TXT record using dig."""
        try:
            result = subprocess.run(
                ['dig', '+short', 'TXT', domain],
                capture_output=True,
                text=True,
                timeout=10
            )
            return [line.strip().strip('"') for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            return []

    def _resolve_cname(self, domain: str) -> List[str]:
        """Resolve CNAME record using dig."""
        try:
            result = subprocess.run(
                ['dig', '+short', 'CNAME', domain],
                capture_output=True,
                text=True,
                timeout=10
            )
            return [line.strip().rstrip('.') for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            return []

    def _resolve_soa(self, domain: str) -> List[str]:
        """Resolve SOA record using dig."""
        try:
            result = subprocess.run(
                ['dig', '+short', 'SOA', domain],
                capture_output=True,
                text=True,
                timeout=10
            )
            return [line.strip().rstrip('.') for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            return []

    def resolve_all(self, domain: str) -> Dict[str, List[str]]:
        """Resolve all record types."""
        results = {}
        for record_type in self.record_types:
            records = self.resolve(domain, record_type)
            if records:
                results[record_type] = records
        return results

    def reverse_lookup(self, ip: str) -> Optional[str]:
        """Reverse DNS lookup."""
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except Exception:
            return None

    def get_ip(self, domain: str) -> List[str]:
        """Get IP addresses for domain."""
        return self._resolve_a(domain)


def main():
    parser = argparse.ArgumentParser(
        description='dns — DNS Lookup Tool'
    )

    # Query
    parser.add_argument('domain', nargs='+', help='Domain(s) to query')

    # Options
    parser.add_argument('--type', '-t', default='A',
                      choices=['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA'],
                      help='DNS record type (default: A)')
    parser.add_argument('--all', '-a', action='store_true',
                      help='Query all record types')
    parser.add_argument('--reverse', '-r', action='store_true',
                      help='Reverse DNS lookup')
    parser.add_argument('--ip', action='store_true',
                      help='Get IP addresses only')

    args = parser.parse_args()

    tool = DNSTool()

    # Reverse lookup
    if args.reverse:
        for ip in args.domain:
            hostname = tool.reverse_lookup(ip)
            if hostname:
                print(f"{ip} → {hostname}")
            else:
                print(f"{ip} → No hostname found")

        return 0

    # Get IP only
    if args.ip:
        for domain in args.domain:
            ips = tool.get_ip(domain)
            if ips:
                for ip in ips:
                    print(ip)

        return 0

    # Query all record types
    if args.all:
        for domain in args.domain:
            print(f"\n{'=' * 60}")
            print(f"Domain: {domain}")
            print('=' * 60)

            results = tool.resolve_all(domain)

            if results:
                for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']:
                    if record_type in results:
                        print(f"\n{record_type}:")
                        for record in results[record_type]:
                            print(f"  {record}")
            else:
                print("\nNo records found")

        return 0

    # Query specific record type
    for domain in args.domain:
        records = tool.resolve(domain, args.type)

        if records:
            for record in records:
                print(record)
        else:
            print(f"No {args.type} records found for {domain}", file=sys.stderr)

    return 0


if __name__ == '__main__':
    sys.exit(main())
