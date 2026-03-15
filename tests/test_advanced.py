import os
import unittest
import sys
import subprocess

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.validators import sanitize_port, validate_ip, validate_interface
from core.firewall_engine import FirewallEngine

class TestAdvancedFeatures(unittest.TestCase):
    
    def test_port_range_validation(self):
        self.assertEqual(sanitize_port("80-90"), "80:90")
        self.assertEqual(sanitize_port("80:90"), "80:90")
        self.assertEqual(sanitize_port("100"), "100")
        self.assertIsNone(sanitize_port("70000"))
        self.assertIsNone(sanitize_port("80-70")) # start > end
    
    def test_interface_validation(self):
        self.assertTrue(validate_interface("eth0"))
        self.assertTrue(validate_interface("wlan0.1"))
        self.assertFalse(validate_interface("eth0; rm -rf /"))
        self.assertTrue(validate_interface(None))
        
    def test_security_permissions(self):
        """Verify that the rules file is saved with 0600 permissions."""
        if os.geteuid() != 0:
            self.skipTest("Requires root permissions")
            
        engine = FirewallEngine()
        test_rules = "/tmp/zerowall_test_rules.v4"
        engine.controller.save_rules(test_rules)
        
        mode = os.stat(test_rules).st_mode
        self.assertEqual(oct(mode & 0o777), '0o600')
        os.remove(test_rules)

    def test_logger_permissions(self):
        """Verify that the log file has 0600 permissions."""
        log_file = "/var/log/zerowall/firewall.log"
        if os.path.exists(log_file):
            mode = os.stat(log_file).st_mode
            self.assertEqual(oct(mode & 0o777), '0o600')
        else:
            self.skipTest("Log file does not exist yet")

if __name__ == "__main__":
    unittest.main()
