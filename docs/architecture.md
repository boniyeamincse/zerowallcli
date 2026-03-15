# ZeroWall Architecture

ZeroWall is designed as a modular, lightweight CLI firewall management tool for Linux. It provides a user-friendly abstraction over `iptables` to manage host-based security policies.

## System Components

### 1. CLI Entry Point (`bin/zerowall`)
- **Responsibility**: Interface with the user, parse arguments, and enforce root privileges.
- **Technology**: Python 3.x, `argparse`.

### 2. Firewall Engine (`core/firewall_engine.py`)
- **Responsibility**: Orchestrates high-level security operations. It translates user commands into logical sequences of firewall rule changes.
- **Key Methods**:
    - `allow_port(port, protocol)`
    - `block_ip(ip)`
    - `unblock_ip(ip)`
    - `get_status()`
    - `reset_firewall()`

### 3. Iptables Controller (`core/iptables_controller.py`)
- **Responsibility**: Direct communication with the Linux kernel's `iptables` subsystem.
- **Technology**: `subprocess` for executing system commands.
- **Functions**: Handles rule insertion (`-A`), deletion (`-D`), and listing (`-L`).

### 4. Logger (`core/logger.py`)
- **Responsibility**: Provides structured logging for all firewall changes.
- **Destination**: `/var/log/zerowall/firewall.log`.

### 5. Rule Manager (`core/rule_manager.py`)
- **Responsibility**: Manages persistence and state verification. Ensures rules are applied consistently.

## Data Flow

1. User executes `zerowall allow 80`.
2. `bin/zerowall` parses the command and arguments.
3. `firewall_engine` receives the request and calls `iptables_controller` to append a rule.
4. `iptables_controller` executes `sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT`.
5. `logger` records the event: `[INFO] Allowed port 80/tcp`.
6. Control returns to the user with a success message.

## Security Considerations
- **Privilege Escalation**: The tool must run with `sudo` privileges.
- **Fail-Safe**: `reset` command provides a way to restore default "DENY ALL" or "ALLOW ALL" policies in case of misconfiguration.
- **Validation**: Strict validation of IP addresses and port numbers to prevent injection attacks.
