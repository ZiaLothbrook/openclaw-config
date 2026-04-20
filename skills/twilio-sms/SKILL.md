# twilio-sms

Send and check SMS messages via Twilio.

## Version

1.0.0

## Usage

```bash
# Send SMS to Ziah
./skills/twilio-sms/twilio-sms send "+13033453071" "Your reminder, sir."

# Check delivery status of a message
./skills/twilio-sms/twilio-sms status SM1234567890abcdef
```

## When to Use

Use this skill whenever you need to:
- Send a proactive notification or reminder to Ziah
- Reply to an incoming SMS (the gateway will provide the sender number)
- Confirm completion of a task via text

**This is the primary outbound channel.** Default to SMS for proactive outreach unless
the message originated from Slack, in which case reply via Slack.

## Environment Variables

Loaded from macOS Keychain by `gateway/start-gateway.sh`:

| Variable | Keychain Service | Purpose |
|---|---|---|
| `TWILIO_ACCOUNT_SID` | `jarvis-twilio-sid` | Account identifier |
| `TWILIO_AUTH_TOKEN` | `jarvis-twilio-auth-token` | API auth |
| `TWILIO_PHONE_NUMBER` | `jarvis-twilio-phone` | Outbound number (+17202608108) |

## Error Handling

The script exits non-zero on any Twilio API error and prints the error message to stderr.
Common errors:
- 21211: Invalid 'To' phone number
- 21608: Unverified number (Trial account limitation)
- 30003: Unreachable destination handset

## Dependencies

- `httpx>=0.28` (managed by UV inline script metadata)
- No other dependencies — UV handles the environment automatically
