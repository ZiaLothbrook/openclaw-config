#!/bin/bash
# Jarvis — Gateway Installation
# Installs the gateway as a launchd service on the Jarvis Mac.
# Run once after cloning the repo.

set -e

JARVIS_HOME="${HOME}/jarvis-config"
PLIST_NAME="com.deepgem.gateway"
PLIST_SRC="${JARVIS_HOME}/gateway/${PLIST_NAME}.plist"
PLIST_DEST="${HOME}/Library/LaunchAgents/${PLIST_NAME}.plist"
LOG_DIR="${HOME}/Library/Logs/Jarvis"

echo "Jarvis Gateway Installation"
echo "============================="

# Create log directory
mkdir -p "$LOG_DIR"
echo "✓ Log directory: $LOG_DIR"

# Validate repo is in the right place
if [[ ! -f "${JARVIS_HOME}/AGENTS.md" ]]; then
    echo "ERROR: jarvis-config not found at ${JARVIS_HOME}"
    echo "  Clone the repo: git clone <repo-url> ~/jarvis-config"
    exit 1
fi
echo "✓ Repo found at ${JARVIS_HOME}"

# Unload existing service if running
if launchctl list | grep -q "$PLIST_NAME"; then
    echo "Stopping existing gateway service..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
fi

# Copy plist
cp "$PLIST_SRC" "$PLIST_DEST"
echo "✓ Plist installed: $PLIST_DEST"

# Load service
launchctl load "$PLIST_DEST"
echo "✓ Service loaded"

# Wait and verify
sleep 2
if launchctl list | grep -q "$PLIST_NAME"; then
    echo "✓ Gateway is running"
    echo ""
    echo "Test with: curl http://localhost:18789/health"
else
    echo "⚠ Gateway may not have started. Check logs:"
    echo "  tail -f ${LOG_DIR}/gateway-error.log"
fi

echo ""
echo "Logs: ${LOG_DIR}/"
echo "  gateway.log       — access logs"
echo "  gateway-error.log — error logs"
