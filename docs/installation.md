# Installation Guide for ZeroWall

ZeroWall can be installed as a Debian package or directly from source.

## Prerequisites
- Linux OS (Ubuntu, Debian, or similar)
- Python 3.6+
- `iptables` installed and available in `$PATH`
- Root privileges (`sudo`)

## Debian Package Installation (Recommended)
Building the package:
```bash
sudo apt-get install devscripts debhelper
dpkg-buildpackage -us -uc -b
```

Installing the package:
```bash
sudo dpkg -i ../zerowall_1.0.0-1_all.deb
```

## Source Installation
For developers or quick testing:
1. Clone the repo.
2. Ensure you have root access.
3. Run `bin/zerowall`.

## Post-Installation
ZeroWall logs activity to `/var/log/zerowall/firewall.log`. Ensure the directory exists and is writable by the user running the tool.
