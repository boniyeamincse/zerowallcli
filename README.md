# ZeroWall - Lightweight CLI Linux Firewall

ZeroWall is a modular, production-ready CLI-based host firewall tool for Linux that simplifies `iptables` management.

## Features
- **Simple Interface**: Easy-to-remember commands like `allow`, `block`, and `status`.
- **Modular Design**: Separated CLI, Engine, and Controller layers.
- **Production Ready**: Full logging to `/var/log/zerowall/` and support for Debian packaging.
- **Fail-Safe**: Maintains established connections during resets.

## Installation

### From .deb Package
```bash
sudo dpkg -i zerowall_1.0.0-1_all.deb
sudo apt-get install -f
```

### From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/zerowall/zerowallcli.git
   cd zerowallcli
   ```
2. Make the binary executable:
   ```bash
   chmod +x bin/zerowall
   ```
3. (Optional) Symlink to `/usr/local/bin`:
   ```bash
   sudo ln -s $(pwd)/bin/zerowall /usr/local/bin/zerowall
   ```

## Usage

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

## Security Best Practices
1. **Principle of Least Privilege**: Only allow necessary ports.
2. **Logs Monitoring**: Regularly check `zerowall logs` for suspicious activity.
3. **Backup Rules**: Always verify your rules after a `reset` to ensure you haven't locked yourself out (though ZeroWall attempts to keep established sessions).

## License
MIT License. See [LICENSE](LICENSE) for details.
