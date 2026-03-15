# ZeroWall — Usage Guide

Detailed command reference for ZeroWall CLI.

## 🚀 Information Commands

### `list-all [--zone=<zone>]`
Lists all active firewall settings in a human-readable format.
```bash
sudo zerowall --list-all --zone=public
```

### `list-ports [--zone=<zone>]`
Lists only the open/allowed ports.

### `list-services [--zone=<zone>]`
Lists enabled services based on the open ports.

## 🛡️ Rule Management

### `allow <port> [--protocol tcp|udp] [--permanent]`
Allows incoming traffic on the specified port. Use `--permanent` to save across reboots.

### `block <ip> [--permanent]`
Immediately drops all incoming traffic from the specified IP address.

### `unblock <ip> [--permanent]`
Removes a previously added block rule for the IP.

## ⚙️ Control & Configuration

### `reload`
Reloads permanently saved firewall rules from `/etc/zerowall/rules.v4`.

### `reset`
Resets the firewall to a "Secure Default" state and removes all custom zone chains.

### `status`
Displays current raw `iptables` rules with packet counts.

### `logs`
Displays the contents of `/var/log/zerowall/firewall.log`.

## 🌐 Zones

ZeroWall supports **Zones** (like `public`, `home`, `work`) to group rules.
By default, rules are **temporary**. To make them survive a reboot or reload, use the `--permanent` flag.

**Example: Add permanent rule to home zone**
```bash
sudo zerowall allow 8080 --zone=home --permanent
```
