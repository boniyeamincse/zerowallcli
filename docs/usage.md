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

### `status`
Displays current `iptables` rules with packet counts and statistics.

### `list-all`
Lists all active firewall settings in a human-readable format.

### `list-ports`
Lists only the open/allowed ports.

### `list-services`
Lists enabled services based on the open ports.

### `reset`
Resets the firewall to a "Secure Default" state:
1. Flushes all rules in the `INPUT` chain.
2. Allows established and related traffic (to prevent disconnecting your current session).
3. Allows all traffic on the loopback (`lo`) interface.
4. Sets the default policy to `DROP` for the `INPUT` chain.

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
