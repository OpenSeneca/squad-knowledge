# dns — DNS Lookup Tool

Query DNS records (A, AAAA, MX, NS, TXT, CNAME, SOA).

**Location:** `~/workspace/tools/dns/`

**Install:** Symlink to `~/.local/bin/dns`

```bash
ln -s ~/workspace/tools/dns/dns.py ~/.local/bin/dns
chmod +x ~/workspace/tools/dns/dns.py
```

## Features

- **A Records** — IPv4 addresses
- **AAAA Records** — IPv6 addresses
- **MX Records** — Mail servers
- **NS Records** — Name servers
- **TXT Records** — Text records
- **CNAME Records** — Alias records
- **SOA Records** — Start of Authority
- **Reverse Lookup** — IP to hostname
- **All Records** — Query all record types
- **No External Dependencies** — Uses dig when available

## Key Commands

### Query Specific Records

- `dns <domain>` — Query A record (default)
- `dns <domain> -t A` — Query A record
- `dns <domain> -t AAAA` — Query AAAA record
- `dns <domain> -t MX` — Query MX record
- `dns <domain> -t NS` — Query NS record
- `dns <domain> -t TXT` — Query TXT record
- `dns <domain> -t CNAME` — Query CNAME record
- `dns <domain> -t SOA` — Query SOA record

### Query All Records

- `dns <domain> --all` — Query all record types

### Reverse Lookup

- `dns <ip> --reverse` — Reverse DNS lookup

### Get IPs Only

- `dns <domain> --ip` — Get IP addresses only

### Multiple Domains

- `dns example.com google.com` — Query multiple domains

## DNS Record Types

| Type | Description | Use Case |
|------|-------------|-----------|
| A | IPv4 address | Get domain IP |
| AAAA | IPv6 address | Get domain IPv6 |
| MX | Mail server | Email configuration |
| NS | Name server | DNS configuration |
| TXT | Text records | SPF, DKIM, verification |
| CNAME | Alias | Domain aliases |
| SOA | Start of Authority | DNS zone info |

## Examples

### Query A Record

```bash
# Query A record
dns example.com

# Output:
# 93.184.216.34
```

### Query MX Records

```bash
# Query MX records
dns example.com -t MX

# Output:
# 10 mail.example.com
```

### Query NS Records

```bash
# Query NS records
dns example.com -t NS

# Output:
# ns1.example.com
# ns2.example.com
```

### Query TXT Records

```bash
# Query TXT records
dns example.com -t TXT

# Output:
# v=spf1 include:_spf.example.com ~all
```

### Query All Records

```bash
# Query all records
dns example.com --all

# Output:
# ============================================================
# Domain: example.com
# ============================================================
#
# A:
#   93.184.216.34
#
# MX:
#   10 mail.example.com
#
# NS:
#   ns1.example.com
#   ns2.example.com
```

### Reverse DNS Lookup

```bash
# Reverse lookup
dns 93.184.216.34 --reverse

# Output:
# 93.184.216.34 → example.com
```

### Get IPs Only

```bash
# Get IPs only (for scripting)
dns example.com --ip

# Output:
# 93.184.216.34
```

### Multiple Domains

```bash
# Query multiple domains
dns example.com google.com github.com

# Output:
# 93.184.216.34
# 142.250.81.110
# 140.82.112.4
```

## Use Cases

### Troubleshooting DNS Issues

```bash
# Check if domain resolves
dns example.com

# Check specific record
dns example.com -t MX

# Check all records
dns example.com --all
```

### Email Configuration

```bash
# Check MX records
dns example.com -t MX

# Check TXT records (SPF, DKIM)
dns example.com -t TXT
```

### Network Diagnostics

```bash
# Check domain resolution
dns api.example.com

# Reverse lookup IP
dns 1.2.3.4 --reverse
```

### Security Verification

```bash
# Check SPF records
dns example.com -t TXT

# Check DMARC records
dns _dmarc.example.com -t TXT
```

### Migration Planning

```bash
# Check current DNS before migration
dns example.com --all > current-dns.txt

# Verify after migration
dns example.com --all > new-dns.txt

# Compare
diff current-dns.txt new-dns.txt
```

### Integration with Other Tools

### With port (port checker)

```bash
# Check DNS then port
dns api.example.com
port check api.example.com 443
```

### With httpc (HTTP client)

```bash
# Resolve domain then test API
dns api.example.com
httpc get https://api.example.com/health
```

### With fhash (file hash calculator)

```bash
# Verify DNS-based content
dns cdn.example.com
# Download and verify
fhash downloaded-file -v expected-hash
```

### With logfind (log file search)

```bash
# Find DNS-related logs
logfind --pattern "DNS|resolve" logs/app.log

# Verify DNS issues
dns problematic-domain.com
```

### With notes (note taking)

```bash
# Note DNS configuration
dns example.com --all | notes add "DNS config for example.com"

# Note DNS issues
dns problematic.com | notes add "DNS not resolving"
```

### With run (command runner)

```bash
# Store DNS check command
run add check-dns "dns example.com"

# Run check
run check-dns
```

### With quick (CLI utilities)

```bash
# Quick IP lookup
dns example.com | quick ip-info

# Quick reverse lookup
dns 1.2.3.4 --reverse
```

### With archive (archive tool)

```bash
# Backup DNS records
dns example.com --all > dns-records.txt
archive create dns-records.txt -o dns-backup.zip
```

## Output Formats

### Single Record

```
<record_value>
```

### All Records

```
============================================================
Domain: <domain>
============================================================

<TYPE>:
  <record>
  <record>
```

### Reverse Lookup

```
<ip> → <hostname>
```

### IPs Only

```
<ip1>
<ip2>
```

## Best Practices

### Troubleshooting

**Check all record types:**
```bash
dns example.com --all
```

**Use reverse lookup for IP analysis:**
```bash
dns 1.2.3.4 --reverse
```

### Email Configuration

**Check MX and TXT records:**
```bash
dns example.com -t MX
dns example.com -t TXT
```

### Security

**Verify SPF/DKIM/DMARC records:**
```bash
dns example.com -t TXT
dns _dmarc.example.com -t TXT
```

### Migration

**Backup DNS before changes:**
```bash
dns example.com --all > backup.txt
```

## Troubleshooting

### No Records Found

**Check domain spelling:**
```bash
dns example.com
# Ensure correct domain
```

**Check specific record type:**
```bash
dns example.com --all
# Shows all available records
```

### DNS Propagation

**Wait for propagation:**
```bash
# DNS changes can take up to 48 hours
# Check with multiple tools:
dns example.com
nslookup example.com
dig example.com
```

### Reverse Lookup Fails

**Check IP has PTR record:**
```bash
dns 1.2.3.4 --reverse
# May return "No hostname found"
```

## Technical Details

**DNS Resolution:**
- A/AAAA: Uses Python's socket.getaddrinfo()
- MX/NS/TXT/CNAME/SOA: Uses `dig` command (if available)
- Falls back to empty result if dig not available

**Record Types:**
- A: IPv4 address (32-bit)
- AAAA: IPv6 address (128-bit)
- MX: Mail exchange (priority + server)
- NS: Name server (delegation)
- TXT: Text records (SPF, DKIM, DMARC)
- CNAME: Canonical name (alias)
- SOA: Start of Authority (zone info)

**Timeout:**
- DNS queries timeout after 10 seconds
- Use `dig` for extended queries

## Requirements

- Python 3.6+
- `dig` command (optional, for extended record types)
- Works on Linux, macOS, Windows (limited)

## DNS Tools Comparison

**vs `nslookup`:**
- `nslookup`: Interactive, more features
- `dns`: Simple, scriptable, multiple domains

**vs `dig`:**
- `dig`: Powerful, complex output
- `dns`: Simple, clean output, multiple types

**vs `host`:**
- `host`: Simple, one record type
- `dns`: Multiple types, multiple domains

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Query. Resolve. Troubleshoot.**

DNS lookups made simple.
