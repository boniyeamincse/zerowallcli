#!/bin/bash

# ZeroWall Local Installer for Kali Linux

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./scripts/install.sh)"
  exit 1
fi

echo "Installing ZeroWall CLI..."

# Get the absolute path to the project root
PROJECT_ROOT=$(pwd)

# 1. Create directory for core library
LIB_DIR="/usr/lib/zerowall"
mkdir -p "$LIB_DIR"
cp -r "$PROJECT_ROOT/core" "$LIB_DIR/"

# 2. Create the executable symlink
BIN_PATH="/usr/local/bin/zerowall"
rm -f "$BIN_PATH" # Remove old one if exists

# Create a small wrapper script in /usr/local/bin
cat <<EOF > "$BIN_PATH"
#!/bin/bash
export PYTHONPATH=\$PYTHONPATH:/usr/lib/zerowall
python3 /usr/lib/zerowall/core/../bin/zerowall "\$@"
EOF

# Copy the bin content safely
mkdir -p /usr/lib/zerowall/bin
cp "$PROJECT_ROOT/bin/zerowall" /usr/lib/zerowall/bin/zerowall

# Fix the wrapper to point correctly
cat <<EOF > "$BIN_PATH"
#!/bin/bash
export PYTHONPATH=\$PYTHONPATH:/usr/lib/zerowall
python3 /usr/lib/zerowall/bin/zerowall "\$@"
EOF

chmod +x "$BIN_PATH"
chmod +x /usr/lib/zerowall/bin/zerowall

# 3. Ensure log directory exists
mkdir -p /var/log/zerowall
touch /var/log/zerowall/firewall.log
chmod 666 /var/log/zerowall/firewall.log

echo "-----------------------------------------------"
echo "ZeroWall successfully installed to $BIN_PATH"
echo "Try running: sudo zerowall --help"
echo "-----------------------------------------------"
