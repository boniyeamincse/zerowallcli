# Installation Guide for ZeroWall

ZeroWall supports two main installation methods for Linux (Debian, Ubuntu, Kali, etc.).

## 📋 Prerequisites
- Linux OS (Debian-based preferred)
- Python 3.6+
- `iptables`
- sudo privileges

---

## 1. Debian Package Installation (.deb)
This is the cleanest method as it allows for easy updates and removal via `apt` or `dpkg`.

### Build from source:
1. Install build tools:
   ```bash
   sudo apt update && sudo apt install -y debhelper dh-python devscripts build-essential
   ```
2. Build the package:
   ```bash
   dpkg-buildpackage -us -uc -b
   ```

### Install:
```bash
sudo dpkg -i ../zerowallcli_1.0.0-1_all.deb
```

---

## 2. Source Installation (Manual/Script)
Best for developers or if you want to run the latest code directly from GitHub.

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/boniyeamincse/zerowallcli.git
   cd zerowallcli
   ```
2. Run the installer script:
   ```bash
   sudo chmod +x scripts/install.sh
   sudo ./scripts/install.sh
   ```

The script will:
- Copy core modules to `/usr/lib/zerowall/`.
- Create a global symlink at `/usr/local/bin/zerowall`.
- Initialize logging at `/var/log/zerowall/`.

---

## 🔍 Post-Installation Check
Verify the installation by running:
```bash
zerowall --version
sudo zerowall status
```
