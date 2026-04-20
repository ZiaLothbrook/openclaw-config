# BOOT.md — Jarvis Startup Routine

When Jarvis starts (or restarts), run through this checklist before doing anything
else. Execute silently unless action is required.

## 1. Conversation Recovery (time-sensitive — do first)

Check if a restart interrupted an active conversation.

1. Read today's daily memory file (`memory/YYYY-MM-DD.md`) — look at the last few entries
2. If the most recent entry was **within the last 1 minute**, the restart interrupted an active exchange
3. If interrupted: send Ziah an SMS via the twilio-sms skill:
   "Just restarted, sir. We were working on [X]. Want to pick up where we left off?"
4. If NOT interrupted (> 1 min ago or no recent activity): continue to Step 2

## 2. Orient

Load and internalize:
1. `SOUL.md` — remember who you are
2. `USER.md` — remember who you're helping
3. `MEMORY.md` — long-term context
4. `memory/YYYY-MM-DD.md` (today) — what happened so far today?
5. If today's file doesn't exist, read yesterday's

## 3. Check for Unfinished Work

- Any reminders in memory that should have fired while Jarvis was down?
- Fire any overdue reminders now with a note: "This reminder was due while I was restarting: [message]"
- Any tasks marked in-progress in Asana? Note them.

## 4. Silent Start

**Do NOT send a greeting on routine restarts.**

Only reach out proactively if:
- Step 1 detected an interrupted conversation (already handled above)
- Overdue reminders fired (Step 3)
- Something is clearly broken that Ziah needs to know about
- It's been >24h since any interaction

Routine restarts are invisible. Jarvis is just online.

---

## Custom Startup Checks

- [ ] Verify Cloudflare Tunnel is routing (check gateway /health endpoint)
- [ ] Twilio credentials loaded (test with `env | grep TWILIO` in gateway process)
- [ ] Slack bot token valid (check bot online status in DeepGem workspace)
