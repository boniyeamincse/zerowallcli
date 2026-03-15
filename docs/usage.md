# ZeroWall Usage Guide

Detailed command reference for ZeroWall CLI.

## Commands

### `allow <port> [--protocol tcp|udp]`
Allows incoming traffic on the specified port.
- **Default protocol**: `tcp`
- **Example**: `sudo zerowall allow 443 --protocol tcp`

### `block <ip>`
Immediately drops all incoming traffic from the specified IP address.
- **Example**: `sudo zerowall block 10.0.0.5`

### `unblock <ip>`
Removes a previously added block rule for the IP.
- **Example**: `sudo zerowall unblock 10.0.0.5`

### `list-all [--zone=<zone>]`
Lists all active firewall settings in a human-readable format.
```bash
sudo zerowall --list-all --zone=home
```

### `list-ports [--zone=<zone>]`
Lists only the open/allowed ports.

### `list-services [--zone=<zone>]`
Lists enabled services based on the open ports.

### `reload`
Reloads permanently saved firewall rules from `/etc/zerowall/rules.v4`.
```bash
sudo zerowall --reload
```

### `reset`
Resets the firewall to a "Secure Default" state and removes all custom zone chains.

## 🌐 Zones & Persistence

ZeroWall supports **Zones** (like `public`, `home`, `work`) to group rules.
By default, rules are **temporary**. To make them survive a reboot or reload, use the `--permanent` flag.

**Example: Add permanent rule to home zone**
```bash
sudo zerowall allow 8080 --zone=home --permanent
```

### `logs`
Displays the contents of `/var/log/zerowall/firewall.log`.

## Common Tasks

### Securing a Web Server
```bash
sudo zerowall reset
sudo zerowall allow 80
sudo zerowall allow 443
sudo zerowall allow 22
```
