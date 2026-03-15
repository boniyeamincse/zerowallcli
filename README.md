# ZeroWall — Lightweight CLI Linux Firewall

ZeroWall is a modular, production-ready CLI-based host firewall tool for Linux that simplifies `iptables` management.

## 🚀 Features
- **Standardized Interface**: Zerowall — Simple Firewall Management CLI.
- **Firewall Zones**: Group rules into logical zones like `public`, `home`, and `work`.
- **Rule Persistence**: Optional `--permanent` flag to save rules across reboots.
- **Fail-Safe**: Maintains established connections during resets to prevent lockouts.
- **Production Ready**: Full logging to `/var/log/zerowall/` and support for Debian packaging.

## 📦 Installation Methods

### Option 1: Debian Package (.deb) - Recommended
Download the latest `.deb` release and install it:
```bash
sudo dpkg -i zerowallcli_1.0.0-1_all.deb
sudo apt-get install -f
```

### Option 2: Source Installation (GitHub)
Clone the repo and run the automated installer:
```bash
git clone https://github.com/boniyeamincse/zerowallcli.git
cd zerowallcli
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

## 🛠️ Usage

```bash
# List all active settings
sudo zerowall --list-all

# Show open ports & services
sudo zerowall --list-ports
sudo zerowall --list-services

# Allow a specific port
sudo zerowall allow 80

# Block/Unblock an IP
sudo zerowall block 1.2.3.4
sudo zerowall unblock 1.2.3.4

# Save rules permanently
sudo zerowall allow 443 --permanent

# Reload/Reset
sudo zerowall --reload
sudo zerowall --reset
```

## 📄 Documentation
- [Architecture](docs/architecture.md)
- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [Commands Cheatsheet](docs/cheatsheet.md)
- [QA Test Report](docs/qa_report.md)

## 🛡️ Security Best Practices
1. **Principle of Least Privilege**: Only allow necessary ports.
2. **Logs Monitoring**: Regularly check `zerowall logs` for suspicious activity.
3. **Backup Rules**: Always verify your rules after a `reset`.

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.
