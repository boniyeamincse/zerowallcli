# ZeroWall CLI Commands Cheatsheet 🛡️

A quick reference guide for managing your Linux firewall with ZeroWall.

## 🚀 Core Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| **Allow Port** | Opens a specific TCP/UDP port. | `sudo zerowall allow 80` |
| **Block IP** | Drops all traffic from a specific IP. | `sudo zerowall block 1.2.3.4` |
| **Unblock IP** | Removes a block rule for an IP. | `sudo zerowall unblock 1.2.3.4` |
| **Status** | Shows current rules and stats (raw). | `sudo zerowall status` |
| **List All** | Shows active settings (human-readable). | `sudo zerowall list-all` |
| **List Ports** | Shows only open/allowed ports. | `sudo zerowall list-ports` |
| **List Services** | Shows only enabled services (ssh, http, etc). | `sudo zerowall list-services` |
| **Reset** | Wipes rules and sets secure defaults. | `sudo zerowall reset` |
| **Logs** | Shows recent firewall activity. | `sudo zerowall logs` |

## ⚙️ Options

- `-h, --help`: Show help message and exit.
- `-v, --version`: Show program version.
- `--protocol [tcp|udp]`: Specify protocol for `allow` (default: tcp).
- `--zone [zone]`: Specify a firewall zone (e.g., public, home, work).
- `--permanent`: Save the rule to permanent storage.
- `--reload`: Reload rules from permanent storage.
- `--list-all`: List all active settings (use with `--zone`).
- `--list-ports`: List only open ports.
- `--list-services`: List enabled services.
- `--get-zones`: Show all available zones.
- `--get-active-zones`: Show zones with active rules.
- `--get-default-zone`: Show the default zone.

## 💡 Common Scenarios

### Secure a new web server:
1. `sudo zerowall reset` (Starts with secure default drop)
2. `sudo zerowall allow 22` (Allow SSH)
3. `sudo zerowall allow 80` (Allow HTTP)
4. `sudo zerowall allow 443` (Allow HTTPS)

### Investigate a blocked attack:
1. `sudo zerowall logs` (Find the IP)
2. `sudo zerowall block [IP]` (Ensure it's permanently blocked)
3. `sudo zerowall status` (Verify rule is active)

---
*Note: All commands except help and version require **sudo** privileges.*
