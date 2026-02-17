#!/usr/bin/env python3
"""
twitter-post — Post tweets to @OpenSenecaLogic via X API v2

Usage:
    twitter-post "Your tweet text here"
    twitter-post --tweet "Your tweet" --dry-run
    twitter-post --delete <tweet-id>
"""

import argparse
import json
import os
import sys
from pathlib import Path


# API endpoints
API_BASE = "https://api.twitter.com/2"
TWEET_URL = f"{API_BASE}/tweets"
DELETE_URL = f"{API_BASE}/tweets/{{id}}"


def load_bearer_token():
    """Load X API bearer token from secrets.env"""
    secrets_path = Path.home() / ".config/openclaw/secrets.env"

    if not secrets_path.exists():
        print(f"❌ Secrets file not found: {secrets_path}")
        print("   Add X_BEARER_TOKEN to ~/.config/openclaw/secrets.env")
        sys.exit(1)

    # Read secrets file
    with open(secrets_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('X_BEARER_TOKEN=') or line.startswith('TWITTER_BEARER_TOKEN='):
                # Extract token (remove quotes, handle various formats)
                token = line.split('=', 1)[1].strip().strip('"').strip("'")
                if token:
                    return token

    print("❌ X_BEARER_TOKEN not found in secrets.env")
    sys.exit(1)


def check_tweet_length(tweet_text):
    """Check if tweet is within character limit (280 chars)"""
    length = len(tweet_text)
    if length > 280:
        print(f"❌ Tweet too long: {length} characters (max: 280)")
        print(f"   Please shorten by {length - 280} characters")
        return False
    print(f"✅ Tweet length: {length}/280 characters")
    return True


def post_tweet(tweet_text, bearer_token, dry_run=False):
    """Post tweet to X API v2"""
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "text": tweet_text
    }

    if dry_run:
        print("\n🔍 Dry run mode - would post:")
        print(f"   Tweet: {tweet_text}")
        print(f"   Endpoint: {TWEET_URL}")
        print(f"   Headers: Authorization: Bearer ********")
        return True, "dry-run"

    try:
        import urllib.request
        import urllib.error

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(TWEET_URL, data=data, headers=headers, method='POST')

        with urllib.request.urlopen(req, timeout=30) as response:
            response_data = json.loads(response.read().decode('utf-8'))

            if 'data' in response_data and 'id' in response_data['data']:
                tweet_id = response_data['data']['id']
                tweet_url = f"https://twitter.com/OpenSenecaLogic/status/{tweet_id}"
                return True, tweet_url
            else:
                return False, "No tweet ID in response"

    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        try:
            error_data = json.loads(error_msg)
            error_detail = error_data.get('detail', error_msg)
        except:
            error_detail = error_msg

        return False, f"HTTP {e.code}: {error_detail}"
    except urllib.error.URLError as e:
        return False, f"Connection error: {e.reason}"
    except Exception as e:
        return False, f"Error: {e}"


def delete_tweet(tweet_id, bearer_token, dry_run=False):
    """Delete tweet by ID"""
    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }

    delete_url = DELETE_URL.format(id=tweet_id)

    if dry_run:
        print(f"\n🔍 Dry run mode - would delete:")
        print(f"   Tweet ID: {tweet_id}")
        print(f"   Endpoint: {delete_url}")
        return True, "dry-run"

    try:
        import urllib.request
        import urllib.error

        req = urllib.request.Request(delete_url, headers=headers, method='DELETE')

        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                return True, f"Deleted tweet {tweet_id}"
            else:
                return False, f"HTTP {response.status}"

    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        try:
            error_data = json.loads(error_msg)
            error_detail = error_data.get('detail', error_msg)
        except:
            error_detail = error_msg

        return False, f"HTTP {e.code}: {error_detail}"
    except urllib.error.URLError as e:
        return False, f"Connection error: {e.reason}"
    except Exception as e:
        return False, f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Post tweets to @OpenSenecaLogic via X API v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Post a tweet
  twitter-post "Hello, world!"

  # Post with explicit flag
  twitter-post --tweet "Hello, world!"

  # Dry run (don't actually post)
  twitter-post --tweet "Hello, world!" --dry-run

  # Delete a tweet
  twitter-post --delete 1234567890

  # Delete with dry run
  twitter-post --delete 1234567890 --dry-run

The script uses X_BEARER_TOKEN from ~/.config/openclaw/secrets.env
        """
    )

    parser.add_argument(
        '--tweet',
        help='Tweet text to post',
    )

    parser.add_argument(
        '--delete',
        help='Tweet ID to delete',
        metavar='ID'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be posted/deleted without actually doing it'
    )

    args = parser.parse_args()

    # Check if we have an action
    if not args.tweet and not args.delete:
        parser.print_help()
        print("\n❌ Error: Please provide --tweet or --delete")
        sys.exit(1)

    # Load bearer token
    print("🔐 Loading X API credentials...")
    bearer_token = load_bearer_token()
    print(f"✅ Bearer token loaded (first 10 chars: {bearer_token[:10]}...)")

    # Post tweet
    if args.tweet:
        tweet_text = args.tweet

        print(f"\n📝 Tweet: {tweet_text}")

        # Check character limit
        if not check_tweet_length(tweet_text):
            sys.exit(1)

        # Post tweet
        print(f"⏳ Posting{' (dry run)' if args.dry_run else ''}...")

        success, result = post_tweet(tweet_text, bearer_token, dry_run=args.dry_run)

        if success:
            print(f"✅ {result}")
        else:
            print(f"❌ Failed to post tweet: {result}")
            sys.exit(1)

    # Delete tweet
    elif args.delete:
        tweet_id = args.delete

        print(f"\n🗑️  Deleting tweet: {tweet_id}")

        # Delete tweet
        print(f"⏳ Deleting{' (dry run)' if args.dry_run else ''}...")

        success, result = delete_tweet(tweet_id, bearer_token, dry_run=args.dry_run)

        if success:
            print(f"✅ {result}")
        else:
            print(f"❌ Failed to delete tweet: {result}")
            sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
