# port — Port Checker and Scanner

Check if ports are open, scan hosts, test connectivity. Perfect for troubleshooting network issues and server deployments.

**Location:** `~/workspace/tools/port/`

**Install:** Symlink to `~/.local/bin/port`

```bash
ln -s ~/workspace/tools/port/port.py ~/.local/bin/port
chmod +x ~/workspace/tools/port/port.py
```

## Features

- **Single Port Check** — Check if a specific port is open
- **Multiple Port Check** — Check multiple ports at once
- **Port Ranges** — Check a range of ports (e.g., 8000-9000)
- **Common Port Scan** — Scan well-known/common ports
- **Custom Scans** — Scan specific ports
- **Multi-Host Scanning** — Scan multiple hosts simultaneously
- **Concurrent Scanning** — Multi-threaded for speed
- **Service Identification** — Identify common services
- **JSON Output** — Machine-readable output
- **Timeout Control** — Adjustable connection timeout
- **Error Reporting** — Detailed error messages

## Key Commands

### Check Single Port

- `port check <host> <port>` — Check if port is open
- `port check localhost 3000` — Check localhost:3000

### Check Multiple Ports

- `port check <host> <ports>` — Check multiple ports
- `port check 100.93.69.117 80,443,8080` — Check multiple ports
- `port check 100.93.69.117 22,80,443,3000,8080` — Check common ports

### Port Ranges

- `port check <host> <start>-<end>` — Check port range
- `port check 100.93.69.117 8000-9000` — Check 8000-9000
- `port check 100.93.69.117 3000-3010` — Check specific range

### Scan Common Ports

- `port scan <host> --common` — Scan common ports
- `port scan 100.93.69.117 --common` — Scan well-known ports

### Scan Port Range

- `port scan <host> --range <start> <end>` — Scan port range
- `port scan 100.93.69.117 --range 1 1000` — Scan first 1000 ports
- `port scan 100.93.69.117 --range 8000 9000` — Scan 8000-9000

### Scan Specific Ports

- `port scan <host> --ports <ports>` — Scan specific ports
- `port scan 100.93.69.117 --ports 22,80,443` — Scan specific ports

### Scan Multiple Hosts

- `port scan <hosts> <options>` — Scan multiple hosts
- `port scan 100.93.69.117,100.98.223.103 --common` — Scan common on 2 hosts

### List Common Ports

- `port list` — List all common ports
- `port list --port 80` — Get service name for port

### Advanced Options

- `--timeout <seconds>` — Set connection timeout (default: 2.0s)
- `--threads <n>` — Set number of threads (default: 10)
- `--show-closed` — Show closed ports
- `--json` — Output as JSON

## Examples

### Check Specific Port

```bash
# Check if SSH is open
port check localhost 22

# Check if HTTP is open
port check 100.93.69.117 80

# Check if database port is open
port check localhost 5432
```

### Check Multiple Ports

```bash
# Check web server ports
port check 100.93.69.117 80,443

# Check development server ports
port check localhost 3000,8000,8080,9000

# Check database ports
port check localhost 3306,5432,6379,27017
```

### Check Port Ranges

```bash
# Check range of ports
port check 100.93.69.117 8000-8010

# Check all development ports
port check localhost 3000-3010

# Check common HTTP ports
port check 100.93.69.117 80-90
```

### Scan Common Ports

```bash
# Scan common ports on a host
port scan 100.93.69.117 --common

# Scan common ports on localhost
port scan localhost --common

# Scan squad VMs
port scan 100.93.69.117,100.98.223.103 --common
```

### Scan Port Range

```bash
# Scan first 1000 ports
port scan 100.93.69.117 --range 1 1000

# Scan development port range
port scan 100.93.69.117 --range 8000 9000

# Scan HTTP port range
port scan 100.93.69.117 --range 80 90
```

### Scan Specific Ports

```bash
# Scan specific ports
port scan 100.93.69.117 --ports 22,80,443,8080

# Scan squad dashboard ports
port scan 100.93.69.117 --ports 22,80,8080

# Scan database ports
port scan localhost --ports 3306,5432,6379,27017
```

### Scan Multiple Hosts

```bash
# Scan common ports on multiple hosts
port scan 100.93.69.117,100.98.223.103 --common

# Scan specific ports on multiple hosts
port scan 100.93.69.117,100.98.223.103 --ports 22,80,443

# Scan port range on multiple hosts
port scan 100.93.69.117,100.98.223.103 --range 8000 9000
```

### List Common Ports

```bash
# List all common ports
port list

# Get service name for a port
port list --port 80

# Check what service is on port 22
port list --port 22
```

### JSON Output

```bash
# Check port with JSON output
port check 100.93.69.117 80 --json

# Scan with JSON output
port scan 100.93.69.117 --common --json

# Parse with jq
port scan 100.93.69.117 --common --json | jq '.[] | select(.open == true)'
```

### Show Closed Ports

```bash
# Show all ports (open and closed)
port scan 100.93.69.117 --common --show-closed

# Show closed ports in range
port scan 100.93.69.117 --range 8000 8010 --show-closed
```

### Adjust Timeout

```bash
# Increase timeout for slow connections
port check 100.93.69.117 80 --timeout 5

# Decrease timeout for fast scans
port scan 100.93.69.117 --common --timeout 1
```

### Adjust Threads

```bash
# Use more threads for faster scans
port scan 100.93.69.117 --range 1 1000 --threads 50

# Use fewer threads to reduce load
port scan 100.93.69.117 --common --threads 5
```

## Use Cases

### Troubleshoot Server Issues

```bash
# Check if web server is running
port check 100.93.69.117 80

# Check if database is accessible
port check localhost 5432

# Check all common services
port scan 100.93.69.117 --common
```

### Check Before Deployment

```bash
# Check if deployment port is available
port check localhost 8080

# Scan for conflicting ports
port scan localhost --range 3000 3100

# Verify all required ports are open
port check 100.93.69.117 22,80,443,8080
```

### Network Diagnostics

```bash
# Test connectivity to remote server
port check 100.93.69.117 22

# Check if firewall is blocking ports
port scan 100.93.69.117 --common --show-closed

# Test multiple servers
port scan 100.93.69.117,100.98.223.103 --common
```

### Find Open Services

```bash
# Find all open services
port scan 100.93.69.117 --common

# Find services on localhost
port scan localhost --common

# Scan for development servers
port scan localhost --range 3000 9000
```

### Verify Service Configuration

```bash
# Verify SSH is on port 22
port check 100.93.69.117 22

# Verify HTTP/HTTPS are accessible
port check 100.93.69.117 80,443

# Verify database ports
port check localhost 3306,5432,6379,27017
```

### Test Load Balancer

```bash
# Check all backend ports
port scan 10.0.1.10,10.0.1.11,10.0.1.12 --common

# Check if app port is open on all backends
port check 10.0.1.10,10.0.1.11,10.0.1.12 8080

# Scan for any unexpected open ports
port scan 10.0.1.10,10.0.1.11,10.0.1.12 --range 1 1000
```

### Security Auditing

```bash
# Find all open ports
port scan 100.93.69.117 --range 1 65535 --threads 100

# Check for unexpected services
port scan 100.93.69.117 --common --show-closed

# Scan for development services on production
port scan 100.93.69.117 --range 3000 9000
```

### Kubernetes/Container Troubleshooting

```bash
# Check if service port is exposed
port check localhost 3000

# Check Kubernetes API
port check k8s-api-server 6443

# Scan container ports
port scan localhost --ports 80,443,8080,3000
```

## Integration with Other Tools

### With ssh-helper (SSH diagnostics)

```bash
# Check SSH port first
port check 100.93.69.117 22

# If SSH is open, run ssh-helper diagnostics
ssh-helper check 100.93.69.117
```

### With notes (note taking)

```bash
# Note open ports
port scan 100.93.69.117 --common | notes add "Open ports on squad dashboard"

# Note connectivity issues
if ! port check 100.93.69.117 80; then
  notes add "Squad dashboard HTTP port 80 closed" -c debug
fi
```

### With run (command runner)

```bash
# Store common scan command
run add scan-squad "port scan 100.93.69.117 --common"

# Run stored command
run scan-squad
```

### With fsearch (file search)

```bash
# Search for port configurations
fsearch -p ".env,.config,.yaml" | grep "PORT"
```

### With fwatch (file watcher)

```bash
# Watch for port changes
fwatch -p ".env" -c "port scan 100.93.69.117 --common"
```

## Common Ports

The tool includes a built-in database of common ports:

| Port | Service |
|------|---------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 587 | SMTP (submission) |
| 993 | IMAPS |
| 995 | POP3S |
| 3306 | MySQL |
| 3389 | RDP |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8000 | HTTP (alt) |
| 8080 | HTTP (proxy) |
| 9000 | HTTP (alt) |
| 27017 | MongoDB |
| 3000 | Node.js |
| 5000 | Flask |
| 5900 | VNC |
| 6443 | Kubernetes API |
| 9200 | Elasticsearch |

## Best Practices

### Timeout Configuration

**Adjust timeout based on network:**
```bash
# Local network: fast
port check 100.93.69.117 80 --timeout 1

# Remote network: slower
port check remote-server.com 80 --timeout 5

# Unreliable network: longer timeout
port check unreliable-server.com 80 --timeout 10
```

### Thread Configuration

**Balance speed and load:**
```bash
# Fast scan (high CPU)
port scan 100.93.69.117 --range 1 1000 --threads 100

# Moderate scan (balanced)
port scan 100.93.69.117 --common --threads 10

# Slow scan (low CPU)
port scan 100.93.69.117 --common --threads 5
```

### Scanning Ranges

**Use common ports first:**
```bash
# Fast check of common ports
port scan 100.93.69.117 --common

# Then scan specific range if needed
port scan 100.93.69.117 --range 8000 9000
```

### Multiple Hosts

**Scan multiple hosts efficiently:**
```bash
# Common ports on multiple hosts
port scan host1,host2,host3 --common

# Specific ports on multiple hosts
port check host1,host2,host3 22,80,443
```

## Troubleshooting

### "DNS resolution failed"

**Check host name:**
```bash
# Hostname may be wrong
port check wrong-host.com 80

# Try IP instead
port check 100.93.69.117 80
```

### "Connection timeout"

**Check firewall/network:**
```bash
# Increase timeout
port check 100.93.69.117 80 --timeout 10

# Check if host is reachable
ping 100.93.69.117

# Check firewall rules
sudo iptables -L | grep 80
```

### No ports open

**Check if service is running:**
```bash
# Check if service is running
systemctl status nginx  # or your service

# Check if service is listening
sudo netstat -tlnp | grep :80

# Check service logs
journalctl -u nginx
```

### Scan is slow

**Increase threads:**
```bash
# Use more threads
port scan 100.93.69.117 --range 1 1000 --threads 50

# Reduce port range
port scan 100.93.69.117 --common

# Scan specific ports only
port scan 100.93.69.117 --ports 22,80,443
```

## Performance Tips

**For fast scans:**
- Use `--common` to scan well-known ports
- Use specific ports with `--ports`
- Increase threads for range scans
- Reduce timeout for known-good connections

**For thorough scans:**
- Use `--range` to scan full ranges
- Use `--show-closed` to see all ports
- Increase timeout for remote networks
- Scan common ports first, then ranges

## Comparison to Alternatives

**vs `netcat` (nc):**
- `nc`: More features, interactive
- `port`: Simpler, faster scans

**vs `nmap`:**
- `nmap`: Powerful, many options
- `port`: Simple, common port database

**vs `telnet`:**
- `telnet`: Interactive testing
- `port`: Automated scanning

## Technical Details

**Scanning Method:**
- Uses TCP SYN (connect) method
- Checks if port accepts connections
- Doesn't verify service type

**Timeout Handling:**
- Default timeout: 2 seconds
- Per-port timeout
- Returns error on timeout

**Concurrent Scanning:**
- Thread-based parallel scanning
- Default: 10 threads
- Configurable with `--threads`

**Service Identification:**
- Common port database
- Based on well-known port assignments
- Not verified (assumes service)

## Requirements

- Python 3.6+
- No external dependencies
- Network connectivity

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Check. Scan. Verify.**

Network connectivity made simple with intelligent port checking.
