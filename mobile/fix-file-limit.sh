#!/bin/bash

# Fix "EMFILE: too many open files" error on macOS

echo " Fixing file watcher limits..."
echo ""

# Check current limit
CURRENT=$(ulimit -n)
echo "Current limit: $CURRENT"

# Set new limit
echo "Setting limit to 4096..."
ulimit -n 4096

# Verify
NEW=$(ulimit -n)
echo "New limit: $NEW"
echo ""

if [ $NEW -ge 4096 ]; then
    echo "[OK] File limit increased successfully!"
    echo ""
    echo "Now run:"
    echo "  npm start"
    echo ""
    echo "To make this permanent, add to ~/.zshrc:"
    echo "  echo 'ulimit -n 4096' >> ~/.zshrc"
else
    echo "[WARNING]  Failed to increase limit. Try:"
    echo "  sudo launchctl limit maxfiles 65536 200000"
fi
