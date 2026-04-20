# omi-handler

Handle incoming transcripts from the Omi wearable device.

## Version

1.0.0

## How It Works

Omi transcripts arrive via webhook at `/webhook/omi` on the gateway. The gateway
verifies the bearer token and fires a Claude Code session with the transcript text.

This SKILL.md defines what Jarvis should DO with the transcript when it arrives.

## Instructions for Jarvis

When you receive an Omi transcript via webhook, do the following:

1. **Filter for signal.** Not every conversation snippet is worth keeping. Skip ambient
   noise, filler words, and context-free fragments under 20 words.

2. **Extract meaningful content** — things worth remembering:
   - Decisions made ("we decided to...")
   - Action items ("I need to...", "remind me to...")
   - People mentioned with context
   - Project status updates
   - Ideas worth capturing

3. **Check for explicit requests** — if the transcript contains:
   - "Jarvis, remind me to [X] at [time]" → create a reminder
   - "Jarvis, [any direct request]" → execute it
   - "Note that..." / "Remember that..." → save to memory

4. **Save to today's daily note** (`memory/YYYY-MM-DD.md`) under an `## Omi` section.
   Keep it brief — a few bullets or a short paragraph.

5. **Do not reply via SMS** unless an explicit action was requested. Ambient transcripts
   are background capture; don't interrupt Ziah with confirmations.

## Example

Incoming transcript: "Yeah, the client call went well. We're moving forward with the
redesign, target launch is end of May. I need to send them the proposal by Thursday."

What to save to `memory/YYYY-MM-DD.md`:
```
## Omi (2026-04-20 14:32)
- Client call successful → moving forward with redesign
- Target launch: end of May
- Action: Send client proposal by Thursday (2026-04-23)
```
