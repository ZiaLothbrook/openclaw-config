# Daily Briefing Workflow

Fires every weekday at 7:00 AM Mountain Time.

Produce a concise morning briefing for Ziah and deliver it via SMS + Slack.

## Instructions

### 1. Gather Context

Collect the following (skip gracefully if a source is unavailable):

- **Calendar**: Today's meetings and time blocks. Note any back-to-back or high-stakes events.
- **Tasks**: Overdue items and things due today (use Asana skill: `./skills/asana/asana list-tasks`)
- **Email**: Any urgent or flagged emails from the past 24h (check memory for email triage summaries)
- **Yesterday's memory**: Read `memory/YYYY-MM-DD.md` from yesterday — any unfinished work?

### 2. Compose the Briefing

Keep it tight. Ziah wants facts, not fluff.

**Format for SMS (primary):**
```
Good morning, sir. [Day], [Date].

Meetings: [list with times, or "Clear calendar today"]
Tasks: [N overdue, M due today, or "All clear"]
[1-2 lines of anything notable: urgent email, flagged risk, etc.]
```

**Format for Slack (secondary, #jarvis-briefings):**
Same content but with Slack markdown. Can include more detail here since it's async
and formatted. Use bullet lists. No tables.

### 3. Deliver

1. Send SMS to +13033453071 via `./skills/twilio-sms/twilio-sms send "+13033453071" "..."`
2. Post to Slack via `./skills/slack-notify/slack-notify briefing "..."`

### 4. Save to Memory

Append a brief record to today's daily note (`memory/YYYY-MM-DD.md`):
```
## Daily Briefing Sent
- [HH:MM MT] Briefing delivered. N meetings, M tasks.
```

## Tone

Jarvis voice. Confident, dry wit welcome. "One meeting at 2 PM, sir. You're free until
then, which I assume you'll use productively." Short enough to read before coffee.

## Rules

- If it's a weekend or holiday: skip. Do not send.
- If calendar is empty: say so briefly ("Clear calendar today, sir.")
- If Asana is unavailable: skip tasks, note the skip
- Never fabricate calendar or task data — only report what you can verify
