#!/bin/bash
# Jarvis Gateway — startup wrapper
# Loads secrets from .env file (primary) or macOS Keychain (fallback).
# This script is what launchd actually runs.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JARVIS_CONFIG_DIR="${SCRIPT_DIR%/gateway}"

# ── Load from .env file (preferred for headless/SSH environments) ─────────────

ENV_FILE="${JARVIS_CONFIG_DIR}/.env"
if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
fi

# ── Fallback: load missing values from macOS Keychain ────────────────────────

load_secret() {
    local service="$1"
    security find-generic-password -a jarvis -s "$service" -w 2>/dev/null || echo ""
}

[[ -z "$TWILIO_ACCOUNT_SID" ]]    && export TWILIO_ACCOUNT_SID="$(load_secret 'jarvis-twilio-sid')"
[[ -z "$TWILIO_AUTH_TOKEN" ]]     && export TWILIO_AUTH_TOKEN="$(load_secret 'jarvis-twilio-auth-token')"
[[ -z "$TWILIO_PHONE_NUMBER" ]]   && export TWILIO_PHONE_NUMBER="$(load_secret 'jarvis-twilio-phone')"
[[ -z "$SLACK_BOT_TOKEN" ]]       && export SLACK_BOT_TOKEN="$(load_secret 'jarvis-slack-bot-token')"
[[ -z "$SLACK_SIGNING_SECRET" ]]  && export SLACK_SIGNING_SECRET="$(load_secret 'jarvis-slack-signing-secret')"
[[ -z "$OMI_WEBHOOK_SECRET" ]]    && export OMI_WEBHOOK_SECRET="$(load_secret 'jarvis-omi-secret')"
[[ -z "$ANTHROPIC_API_KEY" ]]     && export ANTHROPIC_API_KEY="$(load_secret 'jarvis-anthropic-key')"

export JARVIS_CONFIG_DIR
export AUTHORIZED_CALLERS="${AUTHORIZED_CALLERS:-+13033453071}"

# ── Validate required secrets ─────────────────────────────────────────────────

warn_missing() {
    local name="$1" value="$2"
    if [[ -z "$value" ]]; then
        echo "[gateway] WARNING: $name not set — related webhooks will reject all requests"
    fi
}

warn_missing "TWILIO_AUTH_TOKEN"  "$TWILIO_AUTH_TOKEN"
warn_missing "SLACK_SIGNING_SECRET" "$SLACK_SIGNING_SECRET"

if [[ -z "$ANTHROPIC_API_KEY" ]]; then
    echo "[gateway] ERROR: ANTHROPIC_API_KEY not set — Claude Code will not work"
    echo "[gateway] Add it to ${ENV_FILE}"
fi

echo "[gateway] Starting on port 18789..."
echo "[gateway] Config dir: ${JARVIS_CONFIG_DIR}"
echo "[gateway] Env file: ${ENV_FILE}"

# ── Start uvicorn ─────────────────────────────────────────────────────────────

cd "${JARVIS_CONFIG_DIR}/gateway"

# Add uv and node to PATH (for claude CLI invocations spawned by the gateway)
export PATH="${HOME}/.local/bin:/usr/local/bin:${PATH}"

exec uv run \
    --with "fastapi[standard]>=0.115" \
    --with "uvicorn[standard]>=0.34" \
    uvicorn gateway:app \
    --host 127.0.0.1 \
    --port 18789 \
    --log-level info \
    --access-log
