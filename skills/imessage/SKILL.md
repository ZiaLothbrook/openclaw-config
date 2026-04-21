# imessage

Send iMessages via AppleScript on the Jarvis Mac.

## Version

1.0.0

## Usage

```bash
./skills/imessage/imessage send "+13033453071" "Message text here, sir."
```

## When to Use

Use this skill to reply to Ziah via iMessage while the Twilio A2P campaign is pending
approval. Once A2P is approved and the SMS webhook is live, prefer the twilio-sms skill
for outbound messages (more reliable delivery tracking).

**Requires:** Messages.app running on the Jarvis Mac with the Mint Mobile eSIM active.

## Notes

- The Mint Mobile number (+17202608108) is registered and approved for iMessage
- Replies come from +17202608108 (Jarvis's iMessage number)
- No external API needed — uses macOS AppleScript directly
- Messages.app must be open and signed in for this to work
