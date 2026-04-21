#!/usr/bin/env python3
"""
Jarvis Webhook Gateway

The ONLY always-running process. Translates HTTP webhooks into claude CLI invocations.
Has no business logic — just receives, verifies, and fires.

Routes:
  POST /webhook/sms    — Incoming Twilio SMS
  POST /webhook/slack  — Slack events (messages, mentions)
  POST /webhook/omi    — Omi wearable transcripts
  GET  /health         — Liveness check
"""

import hashlib
import hmac
import os
import subprocess
import time
import urllib.parse
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse

# ── Config ──────────────────────────────────────────────────────────────────

TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", "")
OMI_WEBHOOK_SECRET = os.environ.get("OMI_WEBHOOK_SECRET", "")
JARVIS_CONFIG_DIR = os.environ.get("JARVIS_CONFIG_DIR", os.path.expanduser("~/jarvis-config"))
AUTHORIZED_CALLERS = set(
    filter(None, os.environ.get("AUTHORIZED_CALLERS", "").split(","))
)

# ── Signature verification ───────────────────────────────────────────────────


def verify_twilio_signature(body: bytes, signature: str, url: str) -> bool:
    """Twilio HMAC-SHA1 webhook verification.
    See: https://www.twilio.com/docs/usage/security#validating-signatures-from-twilio
    """
    if not TWILIO_AUTH_TOKEN:
        return False
    # For POST with form data: sort params alphabetically, append to URL, then HMAC
    try:
        params = urllib.parse.parse_qs(body.decode(), keep_blank_values=True)
        sorted_params = "".join(
            f"{k}{''.join(sorted(v))}"
            for k, v in sorted(params.items())
        )
    except Exception:
        sorted_params = ""

    message = (url + sorted_params).encode()
    expected = hmac.new(TWILIO_AUTH_TOKEN.encode(), message, hashlib.sha1).digest()
    import base64
    expected_b64 = base64.b64encode(expected).decode()
    return hmac.compare_digest(expected_b64, signature)


def verify_slack_signature(body: bytes, timestamp: str, signature: str) -> bool:
    """Slack HMAC-SHA256 webhook verification."""
    if not SLACK_SIGNING_SECRET:
        return False
    try:
        ts = int(timestamp)
    except (ValueError, TypeError):
        return False
    if abs(time.time() - ts) > 300:  # 5-minute window
        return False
    base = f"v0:{timestamp}:{body.decode()}"
    expected = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(), base.encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


# ── Claude invocation ────────────────────────────────────────────────────────

# Rate limiting: track last invocation time per source
_last_invocation: dict[str, float] = {}
RATE_LIMIT_SECONDS = 5.0


def run_claude(prompt: str, source: str = "webhook") -> None:
    """Fire-and-forget: invoke claude CLI, don't wait for completion.

    Returns immediately — gateway doesn't wait for Claude to finish.
    This keeps webhook response times under 100ms regardless of AI processing time.
    """
    now = time.time()
    last = _last_invocation.get(source, 0)
    if now - last < RATE_LIMIT_SECONDS:
        # Still fire it, but log the overlap
        print(f"[gateway] Note: rapid invocation from {source} ({now - last:.1f}s since last)")

    _last_invocation[source] = now

    subprocess.Popen(
        ["claude", "--print", "--bare", "--dangerously-skip-permissions", prompt],
        cwd=JARVIS_CONFIG_DIR,
        env={**os.environ},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(title="Jarvis Gateway", docs_url=None, redoc_url=None)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "jarvis-gateway", "config_dir": JARVIS_CONFIG_DIR}


@app.post("/webhook/sms")
async def sms_webhook(request: Request):
    """Handle incoming Twilio SMS messages."""
    body = await request.body()
    form = await request.form()

    from_number = str(form.get("From", ""))
    message_body = str(form.get("Body", "")).strip()
    to_number = str(form.get("To", ""))

    # Authorization check — only accept from known contacts
    if AUTHORIZED_CALLERS and from_number not in AUTHORIZED_CALLERS:
        print(f"[gateway] Rejected SMS from unauthorized number: {from_number}")
        return Response(
            content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
            media_type="application/xml",
        )

    if message_body:
        prompt = (
            f'Incoming SMS from {from_number}: "{message_body}"\n\n'
            f"The sender is Ziah. Read your identity files, then handle this message. "
            f"If a reply is needed, use the twilio-sms skill to send it to {from_number}."
        )
        run_claude(prompt, source=f"sms:{from_number}")
        print(f"[gateway] SMS from {from_number}: {message_body[:60]!r}")

    # Return empty TwiML — Claude will reply async via the skill
    return Response(
        content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
        media_type="application/xml",
    )


@app.post("/webhook/slack")
async def slack_webhook(request: Request):
    """Handle Slack event callbacks."""
    body = await request.body()
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")

    if SLACK_SIGNING_SECRET and not verify_slack_signature(body, timestamp, signature):
        raise HTTPException(status_code=403, detail="Invalid Slack signature")

    data = await request.json()

    # Handle Slack's URL verification challenge (one-time during app setup)
    if data.get("type") == "url_verification":
        return JSONResponse({"challenge": data["challenge"]})

    event = data.get("event", {})
    event_type = event.get("type", "")

    # Skip bot messages to prevent loops
    if event.get("bot_id") or event.get("subtype") == "bot_message":
        return JSONResponse({"ok": True})

    if event_type == "message":
        text = event.get("text", "").strip()
        user = event.get("user", "unknown")
        channel = event.get("channel", "unknown")
        ts = event.get("ts", "")

        if text:
            prompt = (
                f'Incoming Slack message in channel {channel} from user {user}: "{text}"\n\n'
                f"Handle this message as Jarvis. If a response is needed, use the "
                f"slack-notify skill to reply to channel {channel}."
            )
            run_claude(prompt, source=f"slack:{channel}")
            print(f"[gateway] Slack {channel} from {user}: {text[:60]!r}")

    elif event_type == "app_mention":
        text = event.get("text", "").strip()
        user = event.get("user", "unknown")
        channel = event.get("channel", "unknown")

        if text:
            prompt = (
                f'Jarvis was mentioned in Slack channel {channel} by user {user}: "{text}"\n\n'
                f"Handle this as Jarvis. Respond via the slack-notify skill to channel {channel}."
            )
            run_claude(prompt, source=f"slack_mention:{channel}")

    return JSONResponse({"ok": True})


@app.post("/webhook/omi")
async def omi_webhook(request: Request):
    """Handle incoming Omi wearable transcripts."""
    # Verify bearer token if configured
    if OMI_WEBHOOK_SECRET:
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {OMI_WEBHOOK_SECRET}":
            raise HTTPException(status_code=403, detail="Invalid Omi token")

    data = await request.json()
    segments = data.get("segments", [])
    text = " ".join(s.get("text", "") for s in segments if s.get("text", "").strip())

    if text.strip():
        prompt = (
            f'Omi wearable transcript received:\n\n"{text}"\n\n'
            f"Follow the instructions in skills/omi-handler/SKILL.md to process this transcript. "
            f"Save meaningful content to memory. Execute any explicit requests (reminders, etc.)."
        )
        run_claude(prompt, source="omi")
        print(f"[gateway] Omi transcript: {text[:80]!r}")

    return JSONResponse({"message": "ok"})
