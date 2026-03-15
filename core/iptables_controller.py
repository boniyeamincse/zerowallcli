import subprocess
import os
from .logger import logger

class IptablesController:
    """Low-level controller for executing iptables commands."""

    @staticmethod
    def run_command(command):
        """Executes a shell command and returns the output."""
        try:
            logger.info(f"Executing command: {' '.join(command)}")
            result = subprocess.run(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.stderr}")
            raise RuntimeError(f"Firewall command failed: {e.stderr}")

    def append_rule(self, chain, params):
        """Appends a rule to a specific chain."""
        cmd = ["iptables", "-A", chain] + params
        return self.run_command(cmd)

    def delete_rule(self, chain, params):
        """Deletes a rule from a specific chain."""
        cmd = ["iptables", "-D", chain] + params
        return self.run_command(cmd)

    def list_rules(self, chain=None):
        """Lists current firewall rules."""
        if chain:
            # For zones, we use custom chains
            cmd = ["iptables", "-L", chain, "-n", "-v"]
        else:
            cmd = ["iptables", "-L", "-n", "-v"]
        return self.run_command(cmd)

    def create_chain(self, chain):
        """Creates a custom chain."""
        try:
            cmd = ["iptables", "-N", chain]
            self.run_command(cmd)
        except RuntimeError:
            # Chain might already exist
            pass

    def delete_chain(self, chain):
        """Deletes a custom chain."""
        cmd = ["iptables", "-X", chain]
        return self.run_command(cmd)

    def save_rules(self, path):
        """Saves current iptables rules to a file with secure permissions."""
        cmd = ["iptables-save"]
        output = self.run_command(cmd)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Write with 0600 permissions
        with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), 'w') as f:
            f.write(output)
            
        return f"Rules saved to {path}"

    def restore_rules(self, path):
        """Restores iptables rules from a file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Backup file not found: {path}")
        
        # Use subprocess.run directly for pipe
        try:
            with open(path, 'r') as f:
                subprocess.run(["iptables-restore"], stdin=f, check=True)
            return "Rules reloaded successfully."
        except Exception as e:
            raise RuntimeError(f"Failed to restore rules: {e}")

    def flush_chain(self, chain):
        """Flushes all rules from a chain."""
        cmd = ["iptables", "-F", chain]
        return self.run_command(cmd)

    def set_policy(self, chain, policy):
        """Sets the default policy for a chain (ACCEPT/DROP)."""
        cmd = ["iptables", "-P", chain, policy]
        return self.run_command(cmd)

    def check_rule_exists(self, chain, params):
        """Checks if a rule already exists (to avoid duplicates)."""
        cmd = ["iptables", "-C", chain] + params
        try:
            subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
