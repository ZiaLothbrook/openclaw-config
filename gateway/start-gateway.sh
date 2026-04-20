#!/bin/bash
# Jarvis Gateway — startup wrapper
# Loads secrets from macOS Keychain and starts the FastAPI gateway.
# This script is what launchd actually runs.

set -e

# ── Load secrets from Keychain ──────────────────────────────────────────────

load_secret() {
    local service="$1"
    security find-generic-password -a jarvis -s "$service" -w 2>/dev/null || echo ""
}

export TWILIO_ACCOUNT_SID="$(load_secret 'jarvis-twilio-sid')"
export TWILIO_AUTH_TOKEN="$(load_secret 'jarvis-twilio-auth-token')"
export TWILIO_PHONE_NUMBER="$(load_secret 'jarvis-twilio-phone')"
export SLACK_BOT_TOKEN="$(load_secret 'jarvis-slack-bot-token')"
export SLACK_SIGNING_SECRET="$(load_secret 'jarvis-slack-signing-secret')"
export OMI_WEBHOOK_SECRET="$(load_secret 'jarvis-omi-secret')"
export ANTHROPIC_API_KEY="$(load_secret 'jarvis-anthropic-key')"

# Also export Twilio auth token as SLACK_SIGNING_SECRET alias if needed
export JARVIS_CONFIG_DIR="${HOME}/jarvis-config"
export AUTHORIZED_CALLERS="+13033453071"

# ── Validate required secrets ────────────────────────────────────────────────

check_secret() {
    local name="$1"
    local value="$2"
    if [[ -z "$value" ]]; then
        echo "[gateway] WARNING: $name not found in Keychain — related webhooks will reject all requests"
    fi
}

check_secret "TWILIO_AUTH_TOKEN" "$TWILIO_AUTH_TOKEN"
check_secret "SLACK_SIGNING_SECRET" "$SLACK_SIGNING_SECRET"
check_secret "ANTHROPIC_API_KEY" "$ANTHROPIC_API_KEY"

echo "[gateway] Starting on port 18789..."
echo "[gateway] Config dir: ${JARVIS_CONFIG_DIR}"
echo "[gateway] Authorized callers: ${AUTHORIZED_CALLERS}"

# ── Start uvicorn ─────────────────────────────────────────────────────────────

cd "${JARVIS_CONFIG_DIR}/gateway"

exec uv run \
    --with "fastapi[standard]>=0.115" \
    --with "uvicorn[standard]>=0.34" \
    uvicorn gateway:app \
    --host 127.0.0.1 \
    --port 18789 \
    --log-level info \
    --access-log
