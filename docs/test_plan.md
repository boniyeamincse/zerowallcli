# QA Test Plan - ZeroWall CLI

This plan outlines the testing strategy for ZeroWall to ensure functional correctness and security enforcement.

## Test Scenarios

| Category | Test Case | Action | Expected Result |
| :--- | :--- | :--- | :--- |
| **Basic** | Help Command | `zerowall --help` | Display help message with usage. |
| **Basic** | Version | `zerowall -v` | Display version `1.0.0`. |
| **Logic** | Allow Port | `sudo zerowall allow 80` | Rule added to `INPUT` chain for port 80. |
| **Logic** | Block IP | `sudo zerowall block 1.2.3.4` | Rule added to `INPUT` chain for source 1.2.3.4 with DROP. |
| **Logic** | Unblock IP | `sudo zerowall unblock 1.2.3.4` | Rule removed from `INPUT` chain. |
| **Logic** | Status | `sudo zerowall status` | Output contains existing rules. |
| **Logic** | Reset | `sudo zerowall reset` | INPUT chain flushed, default DROP set, loopback allowed. |
| **Logic** | Logs | `sudo zerowall logs` | Logs show recent activities. |
| **Edge** | Invalid Port | `sudo zerowall allow 70000` | Error message (invalid port range). |
| **Edge** | Invalid IP | `sudo zerowall block 999.999.999.999` | Error message (invalid IP format). |
| **Edge** | Duplicate | `sudo zerowall allow 80` (twice) | Warning that rule already exists. |

## Verification Method

1. **Internal Verification**: Check `zerowall status` and application logs.
2. **System Verification**: Use `iptables -L INPUT -n` to check actual kernel state.
3. **Automated Testing**: Python script to run these in sequence.
