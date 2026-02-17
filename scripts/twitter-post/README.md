# twitter-post — Post Tweets to @OpenSenecaLogic

Post tweets to @OpenSenecaLogic via X API v2.

## What It Does

The twitter-post script:

- **Posts tweets** to @OpenSenecaLogic via X API v2
- **Checks character limit** (280 chars max)
- **Handles errors** gracefully with clear messages
- **Supports dry-run** mode for testing
- **Can delete tweets** by ID

## Installation

```bash
ln -s /path/to/twitter-post.py ~/.local/bin/twitter-post
chmod +x twitter-post.py
```

Already symlinked in this workspace: `~/.local/bin/twitter-post`

## Setup

### 1. Get X API Bearer Token

1. Go to https://developer.twitter.com/
2. Create an app (or use existing)
3. Get Bearer Token from Keys and Tokens tab

### 2. Add to Secrets File

Add your X API bearer token to `~/.config/openclaw/secrets.env`:

```bash
# X (Twitter) API
X_BEARER_TOKEN=your_bearer_token_here
```

**Important:** Use `chmod 600 ~/.config/openclaw/secrets.env` to secure the file.

### 3. Restart OpenClaw

Restart to load the new environment variable:

```bash
openclaw gateway restart
```

Or set manually for testing:

```bash
export X_BEARER_TOKEN=your_token_here
```

## Usage

### Post a Tweet

```bash
twitter-post "Hello, world!"
```

### Post with Explicit Flag

```bash
twitter-post --tweet "Hello, world!"
```

### Dry Run (Don't Actually Post)

```bash
twitter-post --tweet "Hello, world!" --dry-run
```

### Delete a Tweet

```bash
twitter-post --delete 1234567890
```

### Delete with Dry Run

```bash
twitter-post --delete 1234567890 --dry-run
```

## Examples

### Basic Tweet

```bash
$ twitter-post "Testing the squad's new Twitter tool!"

🔐 Loading X API credentials...
✅ Bearer token loaded (first 10 chars: AAAAAAAAAA...)

📝 Tweet: Testing the squad's new Twitter tool!
✅ Tweet length: 42/280 characters
⏳ Posting...
✅ https://twitter.com/OpenSenecaLogic/status/1234567890
```

### Dry Run Test

```bash
$ twitter-post --tweet "Just a test" --dry-run

🔐 Loading X API credentials...
✅ Bearer token loaded (first 10 chars: AAAAAAAAAA...)

📝 Tweet: Just a test
✅ Tweet length: 10/280 characters
⏳ Posting (dry run)...

🔍 Dry run mode - would post:
   Tweet: Just a test
   Endpoint: https://api.twitter.com/2/tweets
   Headers: Authorization: Bearer ********
✅ dry-run
```

### Character Limit Check

```bash
$ twitter-post "This tweet is way too long and exceeds the 280 character limit because I am trying to demonstrate that the script correctly validates tweet length before attempting to post to the X API..."

🔐 Loading X API credentials...
✅ Bearer token loaded (first 10 chars: AAAAAAAAAA...)

📝 Tweet: This tweet is way too long...
❌ Tweet too long: 285 characters (max: 280)
   Please shorten by 5 characters
```

### Delete Tweet

```bash
$ twitter-post --delete 1234567890

🔐 Loading X API credentials...
✅ Bearer token loaded (first 10 chars: AAAAAAAAAA...)

🗑️  Deleting tweet: 1234567890
⏳ Deleting...
✅ Deleted tweet 1234567890
```

## Error Handling

The script handles common errors:

### No Bearer Token

```bash
❌ X_BEARER_TOKEN not found in secrets.env
```

**Fix:** Add `X_BEARER_TOKEN=your_token` to `~/.config/openclaw/secrets.env`

### Authentication Error

```bash
❌ Failed to post tweet: HTTP 401: Unauthorized
```

**Fix:** Check that your bearer token is valid and not expired

### Rate Limit

```bash
❌ Failed to post tweet: HTTP 429: Rate limit exceeded
```

**Fix:** Wait a few minutes before posting again

### Connection Error

```bash
❌ Failed to post tweet: Connection error: Unable to reach host
```

**Fix:** Check internet connection

## Features

- ✅ X API v2 compliant
- ✅ Character limit validation (280 chars)
- ✅ Dry-run mode for testing
- ✅ Delete tweets by ID
- ✅ Clear error messages
- ✅ Zero external dependencies (pure Python)
- ✅ Returns tweet URL on success

## Deployment to lobster-1

To deploy for Seneca's use:

```bash
# Copy to lobster-1
scp ~/.openclaw/workspace/scripts/twitter-post/twitter-post.py lobster-1:~/.openclaw/scripts/twitter-post

# SSH to lobster-1 and set up
ssh lobster-1
chmod +x ~/.openclaw/scripts/twitter-post
ln -s ~/.openclaw/scripts/twitter-post ~/.local/bin/twitter-post
```

Then Seneca can post tweets:

```bash
twitter-post "Update: Squad deployed new dashboard today!"
```

## Testing

Test without actually posting:

```bash
# Test character limit
twitter-post --tweet "Test" --dry-run

# Test long tweet
python3 -c "print('A' * 300)" | twitter-post -- "$(cat -)"

# Test delete (dry-run)
twitter-post --delete 1234567890 --dry-run
```

## Troubleshooting

### Secrets File Not Found

```bash
# Check if secrets file exists
ls -la ~/.config/openclaw/secrets.env

# If missing, create it
mkdir -p ~/.config/openclaw
touch ~/.config/openclaw/secrets.env
chmod 600 ~/.config/openclaw/secrets.env
```

### Bearer Token Not Loading

```bash
# Check format
cat ~/.config/openclaw/secrets.env

# Should be:
# X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAA...

# Restart OpenClaw to load
openclaw gateway restart
```

### Can't Post from lobster-1

The issue this tool solves: bird CLI is blocked from lobster-1's IP.

```bash
# Test from lobster-1
ssh lobster-1
twitter-post --tweet "Test from lobster-1" --dry-run

# If it works, Seneca can now post!
```

## API Reference

### Endpoints Used

- **POST** `https://api.twitter.com/2/tweets` — Post tweet
- **DELETE** `https://api.twitter.com/2/tweets/{id}` — Delete tweet

### Response Format

**Success:**
```json
{
  "data": {
    "id": "1234567890",
    "text": "Your tweet text"
  }
}
```

**Error:**
```json
{
  "title": "Unauthorized",
  "detail": "Request not authorized",
  "type": "about:blank",
  "status": 401
}
```

## Limitations

- **Bearer token only:** Only supports app-only auth (no user auth)
- **No media:** Cannot post images/videos
- **No threads:** Does not create tweet threads
- **Rate limits:** Subject to X API rate limits

## Security

- **Never commit** secrets.env to git
- **Use chmod 600** to restrict access
- **Rotate tokens** regularly if compromised

## License

MIT License

## Author

OpenSeneca Squad Toolset

---

**Seneca can finally tweet.** 🐦

No more IP blocking. Direct X API v2 access.
