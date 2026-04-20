# TOOLS.md — Jarvis Local Environment

Skills define *how* tools work. This file is for the Jarvis-specific setup — things
unique to this instance.

## Contacts

### Ziah Orion (Primary)
- Phone: +13033453071
- SMS: Yes (primary channel via Twilio)
- Slack: DeepGem workspace, @ziah

## Messaging

### Twilio SMS
- Jarvis outbound number: +13136312257
- Authorized inbound callers: +13033453071 (Ziah only)
- Credentials in Keychain: `jarvis-twilio-sid`, `jarvis-twilio-auth-token`, `jarvis-twilio-phone`
- Send SMS: `./skills/twilio-sms/twilio-sms send "+13033453071" "message"`
- Jarvis number (for reference): +13136312257

### Slack
- Workspace: DeepGem Interactive
- Key channels: `#general`, `#jarvis-alerts`, `#jarvis-briefings`, `#engineering`
- Credentials in Keychain: `jarvis-slack-bot-token`, `jarvis-slack-signing-secret`
- Send to Slack: `./skills/slack-notify/slack-notify send "#jarvis-alerts" "message"`

## Email

- Jarvis inbox: jarvis@deepgeminteractive.com (Google Workspace)
- Credentials in Keychain: `jarvis-google-oauth`
- Email steward workflow handles monitoring and triage

## Task Management

- Platform: Asana
- Credentials in Keychain: `jarvis-asana-token`
- Use `./skills/asana/asana list-tasks` to check tasks

## Webpage Summarization

- Use `./skills/parallel/parallel extract <url>` to extract and summarize any webpage
- No additional setup needed — parallel handles JS rendering and PDFs

## Infrastructure

- Host: Jarviss-MacBook-Pro.local (192.168.0.67)
- Gateway port: 18789 (localhost only, Cloudflare Tunnel for external access)
- Gateway health: `curl http://localhost:18789/health`
- Logs: `~/Library/Logs/Jarvis/`
- Cloudflare Tunnel: routes `jarvis.deepgem.com` → `localhost:18789`

## Credentials in Keychain

All secrets stored via: `security find-generic-password -a jarvis -s <service> -w`

| Service Name | Purpose |
|---|---|
| `jarvis-anthropic-key` | Anthropic API (Claude Code) |
| `jarvis-twilio-sid` | Twilio Account SID |
| `jarvis-twilio-auth-token` | Twilio Auth Token |
| `jarvis-twilio-phone` | Twilio outbound number (+17202608108) |
| `jarvis-slack-bot-token` | Slack Bot OAuth token |
| `jarvis-slack-signing-secret` | Slack signing secret for webhook verification |
| `jarvis-google-oauth` | Google OAuth JSON for Gmail/Calendar |
| `jarvis-asana-token` | Asana personal access token |
| `jarvis-fireflies-key` | Fireflies API key |
| `jarvis-omi-secret` | Omi webhook bearer token |
| `jarvis-parallel-key` | Parallel.ai API key |
| `jarvis-limitless-key` | Limitless API key |
