import subprocess
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
            cmd = ["iptables", "-L", chain, "-n", "-v"]
        else:
            cmd = ["iptables", "-L", "-n", "-v"]
        return self.run_command(cmd)

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
