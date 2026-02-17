# dns — DNS Lookup Tool

Query DNS records (A, AAAA, MX, NS, TXT, CNAME, SOA) with simple CLI.

## What It Does

A fast, scriptable DNS lookup tool that provides:

- **Multiple Record Types** — A, AAAA, MX, NS, TXT, CNAME, SOA
- **Reverse Lookup** — IP to hostname resolution
- **All Records** — Query all record types at once
- **Multiple Domains** — Process multiple domains in one command
- **Get IPs Only** — For scripting and automation

## Installation

### Option 1: Symlink (Linux/macOS)

```bash
git clone https://github.com/OpenSeneca/dns.git
cd dns

ln -s $(pwd)/dns.py ~/.local/bin/dns
chmod +x dns.py
```

### Option 2: Global Install (Python)

```bash
pip install git+https://github.com/OpenSeneca/dns.git
```

### Option 3: Run Directly

```bash
python dns.py
```

## Requirements

- Python 3.6+
- `dig` command (optional, for extended record types)

## Usage

### Query A Record (Default)

```bash
dns example.com
```

### Query Specific Records

```bash
dns example.com -t MX      # MX records
dns example.com -t NS      # NS records
dns example.com -t TXT     # TXT records
dns example.com -t CNAME   # CNAME records
dns example.com -t SOA     # SOA records
```

### Query All Records

```bash
dns example.com --all
```

### Reverse DNS Lookup

```bash
dns 8.8.8.8 --reverse
```

### Get IPs Only (Scripting)

```bash
dns example.com --ip
```

### Multiple Domains

```bash
dns example.com google.com github.com
```

## Examples

### Query A Record

```bash
$ dns google.com

74.125.142.101
74.125.142.113
74.125.142.100
```

### Query MX Records

```bash
$ dns example.com -t MX

10 smtp.example.com
```

### Query All Records

```bash
$ dns example.com --all

============================================================
Domain: example.com
============================================================

A:
  104.18.26.120
  104.18.27.120

MX:
  0 .

NS:
  hera.ns.cloudflare.com.
  elliott.ns.cloudflare.com.

TXT:
  v=spf1 -all
```

### Reverse Lookup

```bash
$ dns 8.8.8.8 --reverse

8.8.8.8 → dns.google
```

## Use Cases

### Troubleshooting DNS Issues

```bash
dns example.com --all
dns example.com -t MX
```

### Email Configuration

```bash
dns example.com -t MX
dns example.com -t TXT
```

### Security Verification

```bash
dns example.com -t TXT
dns _dmarc.example.com -t TXT
```

### Network Diagnostics

```bash
dns api.example.com
dns 1.2.3.4 --reverse
```

## DNS Record Types

| Type | Description | Use Case |
|------|-------------|-----------|
| A | IPv4 address | Get domain IP |
| AAAA | IPv6 address | Get domain IPv6 |
| MX | Mail server | Email configuration |
| NS | Name server | DNS configuration |
| TXT | Text records | SPF, DKIM, DMARC |
| CNAME | Alias | Domain aliases |
| SOA | Start of Authority | DNS zone info |

## Troubleshooting

### "No records found"

```bash
# Check domain spelling
dns example.com

# Check specific record type
dns example.com --all
```

### DNS Propagation

```bash
# DNS changes can take up to 48 hours
# Check with multiple tools:
dns example.com
nslookup example.com
dig example.com
```

## Features

- ✅ Query A, AAAA, MX, NS, TXT, CNAME, SOA records
- ✅ Reverse DNS lookup
- ✅ Query all record types at once
- ✅ Multiple domain support
- ✅ Get IPs only (for scripting)
- ✅ Uses dig for extended record types

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) file for details.

## Author

OpenSeneca - https://github.com/OpenSeneca

## See Also

- [OpenSeneca/cli-tools](https://github.com/OpenSeneca/cli-tools)
- [OpenSeneca/awesome-openclaw-tools](https://github.com/OpenSeneca/awesome-openclaw-tools)

---

**Query. Resolve. Troubleshoot.**

DNS lookups made simple.
