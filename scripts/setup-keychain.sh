#!/bin/bash
# Jarvis — Keychain Setup
# Run this on the Jarvis Mac to store all required secrets.
# Usage: ./scripts/setup-keychain.sh
# You will be prompted for each value.

set -e

store_secret() {
    local service="$1"
    local prompt="$2"
    echo -n "$prompt: "
    read -rs value
    echo
    if [[ -n "$value" ]]; then
        security add-generic-password -a jarvis -s "$service" -w "$value" -U 2>/dev/null || \
        security add-generic-password -a jarvis -s "$service" -w "$value"
        echo "  ✓ Stored $service"
    else
        echo "  — Skipped $service (empty)"
    fi
}

echo "Jarvis Keychain Setup"
echo "====================================="
echo "All secrets stored under account: jarvis"
echo ""

store_secret "jarvis-anthropic-key"        "Anthropic API Key (sk-ant-...)"
store_secret "jarvis-twilio-sid"            "Twilio Account SID (ACxxxxxxxxx)"
store_secret "jarvis-twilio-auth-token"     "Twilio Auth Token"
store_secret "jarvis-twilio-phone"          "Twilio Phone Number (e.g. +17202608108)"
store_secret "jarvis-slack-bot-token"       "Slack Bot Token (xoxb-...)"
store_secret "jarvis-slack-signing-secret"  "Slack Signing Secret"
store_secret "jarvis-google-oauth"          "Google OAuth JSON (paste the entire JSON)"
store_secret "jarvis-asana-token"           "Asana Personal Access Token"
store_secret "jarvis-fireflies-key"         "Fireflies API Key"
store_secret "jarvis-omi-secret"            "Omi Webhook Bearer Token"
store_secret "jarvis-parallel-key"          "Parallel.ai API Key"
store_secret "jarvis-limitless-key"         "Limitless API Key"

echo ""
echo "Done. Verify with:"
echo "  security find-generic-password -a jarvis -s jarvis-anthropic-key -w"
