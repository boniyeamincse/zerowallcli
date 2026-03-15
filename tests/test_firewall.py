import subprocess
import os
import sys
import unittest

# Path to the zerowall binary
ZEROWALL_BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bin', 'zerowall')

def run_zerowall(args, input_str=None):
    """Utility to run zerowall with sudo."""
    cmd = ["sudo", ZEROWALL_BIN] + args
    return subprocess.run(cmd, input=input_str, capture_output=True, text=True)

class TestZeroWall(unittest.TestCase):

    def setUp(self):
        """Ensure we are root for tests."""
        if os.geteuid() != 0:
            print("Tests must be run with sudo.")
            sys.exit(1)

    def test_01_help(self):
        """Test help command."""
        result = subprocess.run([ZEROWALL_BIN, "--help"], capture_output=True, text=True)
        self.assertIn("usage: zerowall", result.stdout)

    def test_02_allow_port(self):
        """Test allowing a port."""
        port = "8888"
        result = run_zerowall(["allow", port])
        self.assertIn(f"Successfully allowed port {port}/tcp", result.stdout)
        
        # Verify via iptables
        verify = subprocess.run(["iptables", "-L", "INPUT", "-n"], capture_output=True, text=True)
        self.assertIn(f"dpt:{port}", verify.stdout)

    def test_03_block_ip(self):
        """Test blocking an IP."""
        ip = "10.10.10.10"
        result = run_zerowall(["block", ip])
        self.assertIn(f"Successfully blocked IP: {ip}", result.stdout)

        # Verify via iptables
        verify = subprocess.run(["iptables", "-L", "INPUT", "-n"], capture_output=True, text=True)
        self.assertIn(ip, verify.stdout)

    def test_04_unblock_ip(self):
        """Test unblocking an IP."""
        ip = "10.10.10.10"
        result = run_zerowall(["unblock", ip])
        self.assertIn(f"Successfully unblocked IP: {ip}", result.stdout)

        # Verify via iptables
        verify = subprocess.run(["iptables", "-L", "INPUT", "-n"], capture_output=True, text=True)
        self.assertNotIn(ip, verify.stdout)

    def test_05_status(self):
        """Test status output."""
        result = run_zerowall(["status"])
        self.assertIn("Chain INPUT", result.stdout)

    def test_06_logs(self):
        """Test if logs are being captured."""
        result = run_zerowall(["logs"])
        self.assertTrue(len(result.stdout) > 0)

    def test_07_duplicate_rule(self):
        """Test duplicate rule handling."""
        port = "2222"
        run_zerowall(["allow", port])
        result = run_zerowall(["allow", port])
        self.assertIn("already allowed", result.stdout)

    def test_08_reset(self):
        """Test firewall reset."""
        # Provide 'y' as input to confirmation prompt
        result = run_zerowall(["reset"], input_str="y\n")
        self.assertIn("Firewall reset complete", result.stdout)
        
        # Verify default policy is DROP
        verify = subprocess.run(["iptables", "-L", "INPUT", "-n"], capture_output=True, text=True)
        self.assertIn("policy DROP", verify.stdout)

if __name__ == "__main__":
    unittest.main()
