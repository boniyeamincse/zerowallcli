# ZeroWall - Lightweight CLI Linux Firewall

ZeroWall is a modular, production-ready CLI-based host firewall tool for Linux that simplifies `iptables` management.

## 🚀 Features
- **Simple Interface**: Easy-to-remember commands like `allow`, `block`, and `status`.
- **Modular Design**: Separated CLI, Engine, and Controller layers.
- **Production Ready**: Full logging to `/var/log/zerowall/` and support for Debian packaging.
- **Fail-Safe**: Maintains established connections during resets.

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
# Allow SSH
sudo zerowall allow 22

# Block a malicious IP
sudo zerowall block 192.168.1.50

# Unblock an IP
sudo zerowall unblock 192.168.1.50

# Check status
sudo zerowall status

# Reset to secure default (DROP all incoming)
sudo zerowall reset

# View logs
sudo zerowall logs
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
