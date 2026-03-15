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
        """Returns the current status of the firewall (raw iptables)."""
        return self.controller.list_rules()

    def list_all(self):
        """Returns active settings in a human-readable format."""
        raw_rules = self.controller.list_rules("INPUT")
        # Parse logic could be complex, for now we provide a filtered view
        lines = raw_rules.split('\n')
        active_settings = ["--- ZeroWall Active Settings ---"]
        active_settings.append(f"Default Policy: {self._get_default_policy()}")
        active_settings.append("\nActive Rules:")
        for line in lines:
            if "ACCEPT" in line or "DROP" in line or "REJECT" in line:
                active_settings.append(line.strip())
        return "\n".join(active_settings)

    def list_ports(self):
        """Returns only the list of open ports."""
        raw_rules = self.controller.list_rules("INPUT")
        ports = []
        import re
        # Regex to find dpt:<port>
        pattern = re.compile(r'dpt:(\d+)')
        for line in raw_rules.split('\n'):
            if "ACCEPT" in line:
                match = pattern.search(line)
                if match:
                    ports.append(match.group(1))
        
        if not ports:
            return "No open ports found."
        return "Open Ports: " + ", ".join(sorted(list(set(ports))))

    def list_services(self):
        """Returns only the enabled services based on port mapping."""
        # Common service mapping
        service_map = {
            '22': 'ssh',
            '80': 'http',
            '443': 'https',
            '21': 'ftp',
            '25': 'smtp',
            '53': 'dns',
            '3306': 'mysql',
            '5432': 'postgresql',
            '6379': 'redis'
        }
        
        raw_rules = self.controller.list_rules("INPUT")
        services = []
        import re
        pattern = re.compile(r'dpt:(\d+)')
        for line in raw_rules.split('\n'):
            if "ACCEPT" in line:
                match = pattern.search(line)
                if match:
                    port = match.group(1)
                    services.append(service_map.get(port, f"unknown({port})"))
        
        if not services:
            return "No services enabled."
        return "Enabled Services: " + ", ".join(sorted(list(set(services))))

    def _get_default_policy(self):
        """Helper to get current default policy."""
        try:
            raw = self.controller.list_rules("INPUT")
            if "policy DROP" in raw:
                return "DROP"
            return "ACCEPT"
        except:
            return "Unknown"

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
