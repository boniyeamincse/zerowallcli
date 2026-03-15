# ZeroWall CLI Commands Cheatsheet 🛡️

Zerowall — Simple Firewall Management CLI

## 🚀 Usage Guide

### Commands
- **Allow Port**: `sudo zerowall allow <port>`
- **Block IP**: `sudo zerowall block <ip>`
- **Unblock IP**: `sudo zerowall unblock <ip>`
- **Status (Raw)**: `sudo zerowall status`

### Information Commands

## 💡 Examples
```bash
# View configuration
zerowall --list-all
zerowall --list-ports

# Manage rules
zerowall allow 22
zerowall block 192.168.1.100 --permanent

# Zone inspection
zerowall --zone public --list-all

# Reload rules
zerowall --reload
```

---
*Note: All commands except help and version require **sudo** privileges.*
