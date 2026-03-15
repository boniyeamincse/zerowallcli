# ZeroWall CLI Commands Cheatsheet 🛡️

Zerowall - Simple Firewall Management CLI

## 🚀 Usage Guide

### Information Commands
- **List all active settings**: `sudo zerowall --list-all`
- **Show all open ports**: `sudo zerowall --list-ports`
- **Show all enabled services**: `sudo zerowall --list-services`
- **Show specific zone config**: `sudo zerowall --zone=<zone> --list-all`
- **Show permanent rules**: `sudo zerowall --permanent --list-all`

### Zone Management
- **List all available zones**: `sudo zerowall --get-zones`
- **Show active zones**: `sudo zerowall --get-active-zones`
- **Show default zone**: `sudo zerowall --get-default-zone`

### Firewall Control
- **Reload rules**: `sudo zerowall --reload`
- **Reset configuration**: `sudo zerowall --reset`

### Core Rule Management
- **Allow Port**: `sudo zerowall allow 80 [--protocol tcp|udp]`
- **Block IP**: `sudo zerowall block 1.2.3.4`
- **Unblock IP**: `sudo zerowall unblock 1.2.3.4`

## 💡 Examples
```bash
zerowall --list-all
zerowall --list-ports
zerowall --list-services
zerowall --zone=public --list-all
zerowall --permanent --list-all
zerowall --reload
```

---
*Note: All commands except help and version require **sudo** privileges.*
