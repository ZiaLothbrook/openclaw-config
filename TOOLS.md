# TOOLS.md — Local Environment Notes

Skills define *how* tools work. This file is for your instance-specific setup.
Keep phone numbers, IPs, and credentials in `CLAUDE.local.md` (gitignored).

## Messaging

### Twilio SMS
- Send: `./skills/twilio-sms/twilio-sms send "<number>" "<message>"`
- Check status: `./skills/twilio-sms/twilio-sms status <SID>`
- Credentials: set `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` in `.env`

### Slack
- Send to channel: `./skills/slack-notify/slack-notify send "#channel" "<message>"`
- Alert: `./skills/slack-notify/slack-notify alert "<message>"`
- Credentials: set `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET` in `.env`

### iMessage (macOS only)
- Send: `./skills/imessage/imessage send "<number>" "<message>"`
- Requires Messages.app open and signed in
- Incoming messages polled via `scripts/poll-imessage.py` (needs Full Disk Access)

## Email
- Managed by `workflows/email-steward/` using the agentmail or Gmail skill
- Credentials: set `GOOGLE_OAUTH_JSON` in `.env`

## Tasks
- Platform: Asana (or Apple Notes / `~/tasks.md` as fallback)
- See `AGENTS.md` Q&A vs Task section for routing logic
- Credentials: set `ASANA_TOKEN` in `.env`

## Webpage Summarization
- `./skills/parallel/parallel extract <url>` — extracts and summarizes any URL

## Gateway
- FastAPI webhook receiver: `gateway/gateway.py`
- Start: `gateway/start-gateway.sh` (loads `.env`, starts uvicorn on port 18789)
- Health: `curl http://localhost:18789/health`
- Logs: `~/Library/Logs/Jarvis/`
- Install as service: `./scripts/install-gateway.sh`

## Credentials (.env)

Copy `.env.example` to `.env` and fill in your values:

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API (Claude Code) |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Twilio outbound number |
| `SLACK_BOT_TOKEN` | Slack Bot OAuth token |
| `SLACK_SIGNING_SECRET` | Slack signing secret |
| `GOOGLE_OAUTH_JSON` | Google OAuth JSON |
| `ASANA_TOKEN` | Asana personal access token |
| `FIREFLIES_API_KEY` | Fireflies API key |
| `OMI_WEBHOOK_SECRET` | Omi webhook bearer token |
| `PARALLEL_API_KEY` | Parallel.ai API key |
| `LIMITLESS_API_KEY` | Limitless API key |
| `AUTHORIZED_CALLERS` | Comma-separated phone numbers allowed to message Jarvis |
| `JARVIS_CONFIG_DIR` | Path to this repo (default: `~/jarvis-config`) |
