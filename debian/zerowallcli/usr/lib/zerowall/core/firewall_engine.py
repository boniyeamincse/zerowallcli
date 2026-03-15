from .iptables_controller import IptablesController
from .logger import logger

class FirewallEngine:
    """High-level engine that implements firewall logic."""

    def __init__(self):
        self.controller = IptablesController()

    def allow_port(self, port, protocol='tcp'):
        """Allows incoming traffic on a specific port."""
        params = ["-p", protocol, "--dport", str(port), "-j", "ACCEPT"]
        if self.controller.check_rule_exists("INPUT", params):
            logger.warning(f"Port {port}/{protocol} is already allowed.")
            return f"Port {port}/{protocol} is already allowed."
        
        self.controller.append_rule("INPUT", params)
        logger.info(f"Successfully allowed port {port}/{protocol}.")
        return f"Successfully allowed port {port}/{protocol}."

    def block_ip(self, ip):
        """Blocks all traffic from a specific IP address."""
        params = ["-s", ip, "-j", "DROP"]
        if self.controller.check_rule_exists("INPUT", params):
            logger.warning(f"IP {ip} is already blocked.")
            return f"IP {ip} is already blocked."
            
        self.controller.append_rule("INPUT", params)
        logger.info(f"Successfully blocked IP: {ip}.")
        return f"Successfully blocked IP: {ip}."

    def unblock_ip(self, ip):
        """Removes a block rule for a specific IP address."""
        params = ["-s", ip, "-j", "DROP"]
        if not self.controller.check_rule_exists("INPUT", params):
            logger.warning(f"IP {ip} is not currently blocked.")
            return f"IP {ip} is not currently blocked."
            
        self.controller.delete_rule("INPUT", params)
        logger.info(f"Successfully unblocked IP: {ip}.")
        return f"Successfully unblocked IP: {ip}."

    def get_status(self):
        """Returns the current status of the firewall."""
        return self.controller.list_rules()

    def reset_firewall(self):
        """Resets the firewall to a safe default state (DROP all incoming)."""
        logger.info("Resetting firewall to default state...")
        self.controller.flush_chain("INPUT")
        # Allow established connections to prevent lockouts
        self.controller.append_rule("INPUT", ["-m", "conntrack", "--ctstate", "ESTABLISHED,RELATED", "-j", "ACCEPT"])
        # Allow loopback
        self.controller.append_rule("INPUT", ["-i", "lo", "-j", "ACCEPT"])
        # Set default policy
        self.controller.set_policy("INPUT", "DROP")
        logger.info("Firewall reset complete. Default policy set to DROP.")
        return "Firewall reset complete. Default policy set to DROP (established connections maintained)."
