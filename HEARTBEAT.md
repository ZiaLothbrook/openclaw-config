# HEARTBEAT.md — Jarvis Periodic Checklist

Runs every 15 minutes via cron. Rotate through 1-2 checks per cycle.

## Periodic Checks (Rotate)

- [ ] **Upcoming meetings** — if a meeting starts in <30 min and no prep was sent, trigger meeting-prep workflow
- [ ] **Overdue tasks** — if any Asana task is >24h overdue, nudge via Slack (once per day max)
- [ ] **Urgent emails** — if >4h since last email check and new high-priority email, alert via SMS
- [ ] **Calendar (next 24h)** — check if >8h since last check

## Daily Checks (at 7 AM, via daily-briefing workflow)

- [ ] Did the learning loop run last night?
- [ ] Are gateway logs clean? (no repeated errors)
- [ ] Config updates: `./skills/openclaw/openclaw sync` to pull upstream improvements

## Rules

- **Late night (23:00–08:00 MT):** Skip all checks unless URGENT (critical email, system down)
- **All clear:** No message. Reply `HEARTBEAT_OK` and move on.
- **Something needs attention:** Handle it first, then notify if necessary
- **Don't notify about things already resolved**
- **Don't celebrate the absence of problems**

## What "HEARTBEAT_OK" Means

Silent success. Checked everything, nothing needs Ziah's attention. The absence of a
message IS the message.
