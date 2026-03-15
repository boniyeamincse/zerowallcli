from .iptables_controller import IptablesController
from .logger import logger

import os
import json

class FirewallEngine:
    """High-level engine that implements firewall logic with Zones and Persistence."""

    def __init__(self):
        self.controller = IptablesController()
        self.config_dir = "/etc/zerowall"
        self.rules_file = os.path.join(self.config_dir, "rules.v4")
        self.zones_file = os.path.join(self.config_dir, "zones.json")
        self._ensure_config_dir()
        self.zones = self._load_zones()

    def _ensure_config_dir(self):
        if not os.path.exists(self.config_dir):
            try:
                os.makedirs(self.config_dir)
            except PermissionError:
                # If we don't have permission now, we will fail later if needed
                pass

    def _load_zones(self):
        if os.path.exists(self.zones_file):
            with open(self.zones_file, 'r') as f:
                return json.load(f)
        return ["public", "home", "work", "internal"]

    def _save_zones(self):
        with open(self.zones_file, 'w') as f:
            json.dump(self.zones, f)

    def _get_chain(self, zone):
        if not zone:
            return "INPUT"
        zone_chain = f"ZW-ZONE-{zone.upper()}"
        # Check if chain exists first to avoid noisy error logs
        try:
            self.controller.run_command(["iptables", "-L", zone_chain])
        except:
            self.controller.create_chain(zone_chain)
        
        # Ensure the zone is jumped to from INPUT if it's a zone rule
        jump_params = ["-j", zone_chain]
        if not self.controller.check_rule_exists("INPUT", jump_params):
            self.controller.append_rule("INPUT", jump_params)
        return zone_chain

    def allow_port(self, port, protocol='tcp', zone=None, permanent=False):
        """Allows incoming traffic on a specific port."""
        chain = self._get_chain(zone)
        params = ["-p", protocol, "--dport", str(port), "-j", "ACCEPT"]
        
        if self.controller.check_rule_exists(chain, params):
            return f"Port {port}/{protocol} is already allowed in zone {zone or 'default'}."
        
        self.controller.append_rule(chain, params)
        if permanent:
            self.controller.save_rules(self.rules_file)
            
        logger.info(f"Successfully allowed port {port}/{protocol} in zone {zone or 'default'}.")
        return f"Successfully allowed port {port}/{protocol} in zone {zone or 'default'}."

    def block_ip(self, ip, zone=None, permanent=False):
        """Blocks all traffic from a specific IP address."""
        chain = self._get_chain(zone)
        params = ["-s", ip, "-j", "DROP"]
        if self.controller.check_rule_exists(chain, params):
            return f"IP {ip} is already blocked in zone {zone or 'default'}."
            
        self.controller.append_rule(chain, params)
        if permanent:
            self.controller.save_rules(self.rules_file)
        logger.info(f"Successfully blocked IP: {ip} in zone {zone or 'default'}.")
        return f"Successfully blocked IP: {ip} in zone {zone or 'default'}."

    def unblock_ip(self, ip, zone=None, permanent=False):
        """Removes a block rule for a specific IP address."""
        chain = self._get_chain(zone)
        params = ["-s", ip, "-j", "DROP"]
        if not self.controller.check_rule_exists(chain, params):
            return f"IP {ip} is not currently blocked in zone {zone or 'default'}."
            
        self.controller.delete_rule(chain, params)
        if permanent:
            self.controller.save_rules(self.rules_file)
        logger.info(f"Successfully unblocked IP: {ip} in zone {zone or 'default'}.")
        return f"Successfully unblocked IP: {ip} in zone {zone or 'default'}."

    def get_status(self, zone=None):
        """Returns the current status of the firewall (raw iptables)."""
        chain = self._get_chain(zone) if zone else None
        return self.controller.list_rules(chain)

    def list_all(self, zone=None):
        """Returns active settings in a human-readable format."""
        chain = self._get_chain(zone)
        raw_rules = self.controller.list_rules(chain)
        lines = raw_rules.split('\n')
        active_settings = [f"--- ZeroWall Active Settings (Zone: {zone or 'default'}) ---"]
        active_settings.append(f"Default Policy: {self._get_default_policy()}")
        active_settings.append("\nActive Rules:")
        for line in lines:
            if "ACCEPT" in line or "DROP" in line or "REJECT" in line:
                active_settings.append(line.strip())
        return "\n".join(active_settings)

    def list_ports(self, zone=None):
        """Returns only the list of open ports."""
        chain = self._get_chain(zone)
        raw_rules = self.controller.list_rules(chain)
        ports = []
        import re
        pattern = re.compile(r'dpt:(\d+)')
        for line in raw_rules.split('\n'):
            if "ACCEPT" in line:
                match = pattern.search(line)
                if match:
                    ports.append(match.group(1))
        
        if not ports:
            return f"No open ports found in zone {zone or 'default'}."
        return f"Open Ports ({zone or 'default'}): " + ", ".join(sorted(list(set(ports))))

    def list_services(self, zone=None):
        """Returns only the enabled services based on port mapping."""
        service_map = {'22': 'ssh', '80': 'http', '443': 'https', '21': 'ftp', '25': 'smtp', '53': 'dns', '3306': 'mysql', '5432': 'postgresql', '6379': 'redis'}
        chain = self._get_chain(zone)
        raw_rules = self.controller.list_rules(chain)
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
            return f"No services enabled in zone {zone or 'default'}."
        return f"Enabled Services ({zone or 'default'}): " + ", ".join(sorted(list(set(services))))

    def get_zones(self):
        return "Available Zones: " + ", ".join(self.zones)

    def get_active_zones(self):
        # In this simple model, all defined zones are active if they have rules
        active = []
        for z in self.zones:
            chain = f"ZW-ZONE-{z.upper()}"
            # Check if chain has rules
            status = self.controller.list_rules(chain)
            if "pt" in status or "ACCEPT" in status:
                active.append(z)
        return "Active Zones: " + ", ".join(active) if active else "No specialized active zones."

    def get_default_zone(self):
        return "Default Zone: public"

    def reload_firewall(self):
        """Reloads rules from the permanent storage."""
        if os.path.exists(self.rules_file):
            return self.controller.restore_rules(self.rules_file)
        return "Error: No permanent rules found to reload."

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
        # Find all custom ZW chains and flush/delete
        for z in self.zones:
            chain = f"ZW-ZONE-{z.upper()}"
            try:
                self.controller.flush_chain(chain)
                self.controller.delete_chain(chain)
            except:
                pass
        
        self.controller.append_rule("INPUT", ["-m", "conntrack", "--ctstate", "ESTABLISHED,RELATED", "-j", "ACCEPT"])
        self.controller.append_rule("INPUT", ["-i", "lo", "-j", "ACCEPT"])
        self.controller.set_policy("INPUT", "DROP")
        logger.info("Firewall reset complete. Default policy set to DROP.")
        return "Firewall reset complete. Default policy set to DROP (established connections maintained)."
