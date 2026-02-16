#!/usr/bin/env python3
"""
http — HTTP Client for API Testing

Simple HTTP client for making requests, testing APIs, debugging web services.
"""

import sys
import argparse
import json
from typing import Dict, Optional, List, Tuple
import urllib.request
import urllib.error
from urllib.parse import urlparse, urlencode
from datetime import datetime
import time


class HTTPClient:
    """Simple HTTP client."""

    def __init__(self, timeout: float = 10.0, verbose: bool = False):
        self.timeout = timeout
        self.verbose = verbose
        self.history: List[Dict] = []

    def request(self,
               method: str,
               url: str,
               headers: Optional[Dict[str, str]] = None,
               data: Optional[str] = None,
               params: Optional[Dict[str, str]] = None,
               json_data: Optional[Dict] = None,
               auth: Optional[Tuple[str, str]] = None) -> Dict:
        """Make HTTP request."""
        start_time = time.time()

        # Add query parameters
        if params:
            parsed = urlparse(url)
            query = urlencode(params)
            url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"

        # Prepare request
        req = urllib.request.Request(url)

        # Set method
        req.method = method.upper()

        # Set headers
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)

        # Set content type for JSON
        if json_data:
            data = json.dumps(json_data)
            req.add_header('Content-Type', 'application/json')

        # Set data
        if data:
            req.data = data.encode('utf-8')

        # Set auth
        if auth:
            import base64
            credentials = f"{auth[0]}:{auth[1]}"
            encoded = base64.b64encode(credentials.encode()).decode()
            req.add_header('Authorization', f'Basic {encoded}')

        if self.verbose:
            print(f"\n{'=' * 60}")
            print(f"Request: {method.upper()} {url}")
            if headers:
                print(f"Headers:")
                for key, value in headers.items():
                    print(f"  {key}: {value}")
            if data:
                print(f"Body:\n{data}")
            print(f"{'=' * 60}\n")

        # Make request
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode('utf-8')
                status_code = response.status
                response_headers = dict(response.headers)

                elapsed_time = time.time() - start_time

                result = {
                    'url': url,
                    'method': method.upper(),
                    'status': status_code,
                    'headers': response_headers,
                    'body': response_data,
                    'elapsed': elapsed_time,
                    'success': 200 <= status_code < 300,
                    'timestamp': datetime.now().isoformat()
                }

                self.history.append(result)
                return result

        except urllib.error.HTTPError as e:
            elapsed_time = time.time() - start_time
            response_data = e.read().decode('utf-8') if e.fp else ''

            result = {
                'url': url,
                'method': method.upper(),
                'status': e.code,
                'headers': dict(e.headers) if e.headers else {},
                'body': response_data,
                'elapsed': elapsed_time,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

            self.history.append(result)
            return result

        except urllib.error.URLError as e:
            elapsed_time = time.time() - start_time

            result = {
                'url': url,
                'method': method.upper(),
                'status': None,
                'headers': {},
                'body': '',
                'elapsed': elapsed_time,
                'success': False,
                'error': str(e.reason),
                'timestamp': datetime.now().isoformat()
            }

            self.history.append(result)
            return result

        except Exception as e:
            elapsed_time = time.time() - start_time

            result = {
                'url': url,
                'method': method.upper(),
                'status': None,
                'headers': {},
                'body': '',
                'elapsed': elapsed_time,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

            self.history.append(result)
            return result

    def get(self, url: str, params: Optional[Dict[str, str]] = None,
           headers: Optional[Dict[str, str]] = None) -> Dict:
        """GET request."""
        return self.request('GET', url, params=params, headers=headers)

    def post(self, url: str, data: Optional[str] = None,
            json_data: Optional[Dict] = None,
            headers: Optional[Dict[str, str]] = None) -> Dict:
        """POST request."""
        return self.request('POST', url, data=data, json_data=json_data, headers=headers)

    def put(self, url: str, data: Optional[str] = None,
           json_data: Optional[Dict] = None,
           headers: Optional[Dict[str, str]] = None) -> Dict:
        """PUT request."""
        return self.request('PUT', url, data=data, json_data=json_data, headers=headers)

    def delete(self, url: str,
              headers: Optional[Dict[str, str]] = None) -> Dict:
        """DELETE request."""
        return self.request('DELETE', url, headers=headers)


def format_response(result: Dict, json_output: bool = False, show_headers: bool = False,
                   show_body: bool = True, pretty: bool = True) -> str:
    """Format HTTP response."""
    if json_output:
        return json.dumps(result, indent=2 if pretty else None)

    output = []

    # Status line
    status_icon = "✅" if result['success'] else "❌"
    status = result['status'] if result['status'] else "ERROR"
    output.append(f"{status_icon} {result['method']} {result['url']}")
    output.append(f"   Status: {status}")
    output.append(f"   Time: {result['elapsed']:.3f}s\n")

    # Headers
    if show_headers and result['headers']:
        output.append("Headers:")
        for key, value in result['headers'].items():
            output.append(f"  {key}: {value}")
        output.append("")

    # Body
    if show_body and result['body']:
        output.append("Body:")

        # Try to format as JSON
        if pretty:
            try:
                body_json = json.loads(result['body'])
                output.append(json.dumps(body_json, indent=2))
            except json.JSONDecodeError:
                output.append(result['body'])
        else:
            output.append(result['body'])

    # Error
    if not result['success'] and result.get('error'):
        if output:
            output.append("")
        output.append(f"Error: {result['error']}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='http — HTTP Client for API Testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  http get http://example.com
  http get http://api.example.com/users
  http post http://api.example.com/users -j '{"name":"John"}'
  http put http://api.example.com/users/1 -j '{"name":"Jane"}'
  http delete http://api.example.com/users/1
  http get http://api.example.com/users --headers "Authorization:Bearer token"
  http post http://api.example.com/users -j '{"name":"John"}' --verbose

Common Use Cases:
  - Test REST APIs
  - Debug web services
  - Check HTTP status codes
  - Test authentication
  - Send JSON data
  - Inspect response headers
        """
    )

    # Methods
    subparsers = parser.add_subparsers(dest='method', help='HTTP method')

    # GET
    get_parser = subparsers.add_parser('get', help='GET request')
    get_parser.add_argument('url', help='URL to request')
    get_parser.add_argument('--params', help='Query parameters (JSON or key=value,key=value)')
    get_parser.add_argument('--headers', help='Headers (JSON or key:value,key:value)')

    # POST
    post_parser = subparsers.add_parser('post', help='POST request')
    post_parser.add_argument('url', help='URL to request')
    post_parser.add_argument('--data', help='Request body')
    post_parser.add_argument('--json', '-j', help='JSON body')
    post_parser.add_argument('--headers', help='Headers (JSON or key:value,key:value)')

    # PUT
    put_parser = subparsers.add_parser('put', help='PUT request')
    put_parser.add_argument('url', help='URL to request')
    put_parser.add_argument('--data', help='Request body')
    put_parser.add_argument('--json', '-j', help='JSON body')
    put_parser.add_argument('--headers', help='Headers (JSON or key:value,key:value)')

    # DELETE
    delete_parser = subparsers.add_parser('delete', help='DELETE request')
    delete_parser.add_argument('url', help='URL to request')
    delete_parser.add_argument('--headers', help='Headers (JSON or key:value,key:value)')

    # Common options
    parser.add_argument('--timeout', type=float, default=10.0,
                      help='Request timeout in seconds (default: 10.0)')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Show request details')
    parser.add_argument('--show-headers', action='store_true',
                      help='Show response headers')
    parser.add_argument('--hide-body', action='store_true',
                      help='Hide response body')
    parser.add_argument('--no-pretty', action='store_true',
                      help='Don\'t pretty-print JSON')
    parser.add_argument('--json-output', action='store_true',
                      help='Output as JSON')

    args = parser.parse_args()

    if not args.method:
        parser.print_help()
        return 1

    # Parse params
    params = None
    if hasattr(args, 'params') and args.params:
        if args.params.startswith('{'):
            params = json.loads(args.params)
        else:
            params = {}
            for pair in args.params.split(','):
                key, value = pair.split('=', 1)
                params[key] = value

    # Parse headers
    headers = None
    if hasattr(args, 'headers') and args.headers:
        if args.headers.startswith('{'):
            headers = json.loads(args.headers)
        else:
            headers = {}
            for pair in args.headers.split(','):
                key, value = pair.split(':', 1)
                headers[key.strip()] = value.strip()

    # Parse JSON data
    json_data = None
    if hasattr(args, 'json') and args.json:
        json_data = json.loads(args.json)

    # Make request
    client = HTTPClient(timeout=args.timeout, verbose=args.verbose)

    result = None
    if args.method == 'get':
        result = client.get(args.url, params=params, headers=headers)
    elif args.method == 'post':
        result = client.post(args.url, data=args.data, json_data=json_data, headers=headers)
    elif args.method == 'put':
        result = client.put(args.url, data=args.data, json_data=json_data, headers=headers)
    elif args.method == 'delete':
        result = client.delete(args.url, headers=headers)

    # Format and print
    output = format_response(
        result,
        json_output=args.json_output,
        show_headers=args.show_headers or args.verbose,
        show_body=not args.hide_body,
        pretty=not args.no_pretty
    )
    print(output)

    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
