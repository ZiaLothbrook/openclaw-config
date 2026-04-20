# slack-notify

Send messages to Slack channels and users via the Slack Web API.

## Version

1.0.0

## Usage

```bash
# Send to a specific channel
./skills/slack-notify/slack-notify send "#general" "Message text here"

# Send an alert (goes to #jarvis-alerts)
./skills/slack-notify/slack-notify alert "Something needs attention"

# Post a daily briefing (goes to #jarvis-briefings)
./skills/slack-notify/slack-notify briefing "Daily briefing content..."

# DM a user by Slack user ID
./skills/slack-notify/slack-notify dm "U012AB3CD" "Direct message"

# Look up a channel's ID (useful for troubleshooting)
./skills/slack-notify/slack-notify channel-info general
```

## When to Use

- Posting async updates, briefings, code review results to channels
- Replying to Slack messages that came through the gateway
- Sending formatted content that doesn't fit in SMS (tables, code blocks, links)
- Posting to #jarvis-alerts when something needs Ziah's attention

**Prefer SMS for time-sensitive, personal outreach. Use Slack for workspace-level content.**

## Slack Markdown

Slack supports limited markdown:
- `*bold*`, `_italic_`, `~strikethrough~`
- `\`code\`` and ` ```code block``` `
- `<https://example.com|link text>` for hyperlinks
- No tables — use bullet lists instead

## Environment Variables

| Variable | Keychain Service | Purpose |
|---|---|---|
| `SLACK_BOT_TOKEN` | `jarvis-slack-bot-token` | Bot OAuth token (xoxb-...) |

## Channels

| Channel | Purpose |
|---|---|
| `#jarvis-alerts` | Time-sensitive notifications for Ziah |
| `#jarvis-briefings` | Daily briefings and summaries |
| `#engineering` | Code review results, deploy notices |
| `#general` | General workspace channel |

## Dependencies

- `httpx>=0.28` (UV managed)
