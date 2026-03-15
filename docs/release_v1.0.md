# ZeroWall v1.0 Release Instructions

To finalize the installation and test ZeroWall on your host PC, please follow these steps.

## 1. Install Build Dependencies
Building the `.deb` package requires `debhelper`.
```bash
sudo apt-get update
sudo apt-get install -y debhelper devscripts build-essential python3-all
```

## 2. Build the Debian Package
In the project root directory, run:
```bash
dpkg-buildpackage -us -uc -b
```

## 3. Install the Package
The `.deb` file will be created in the parent directory.
```bash
sudo dpkg -i ../zerowall_1.0.0-1_all.deb
sudo apt-get install -f
```

## 4. Run Functional Tests
Verify everything is working correctly:
```bash
sudo python3 tests/test_firewall.py
```

## 5. Tag Release on GitHub
After verifying, you can tag the release:
```bash
git tag -a v1.0 -m "Release version 1.0"
git push origin v1.0
```

## Final Verification Commands
```bash
# Check if binary is in PATH
zerowall --version

# Test a firewall rule
sudo zerowall allow 8080
sudo zerowall status | grep 8080

# Clean up
sudo zerowall reset
```
