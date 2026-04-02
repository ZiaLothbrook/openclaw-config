# Learning Loop — Rules

Configuration for the self-improvement system. Edit these thresholds to tune how
aggressively the learning loop captures, detects, and promotes.

## Thresholds

- **Pattern threshold:** 2 — how many times a correction must appear across different
  sessions before becoming a pattern candidate
- **Detection window:** 30 days — how far back to look during pattern detection (matches
  correction decay period so no corrections fall through the gap)
- **Validation trigger:** 3 unvalidated candidates — triggers an immediate validation
  run instead of waiting for the weekly cron
- **Promotable confidence:** high and medium — only these confidence levels proceed to
  validation. Low-confidence candidates accumulate more evidence first.

## Decay Periods

- **Correction decay:** 30 days — unmatched corrections are archived after this
- **Pattern decay:** 60 days — unvalidated pattern candidates are archived after this
- **Rule staleness:** 90 days — promoted rules not triggered in this period are flagged
  for review (NOT auto-deleted — flagged for human review)

## Promotion Gates

**Self-promote without human approval:**

- Workflow-specific patterns → that workflow's `agent_notes.md`
- General knowledge → `memory/topics/learnings-*.md`

**Require human approval before promotion:**

- Fundamental operating principles → `AGENTS.md`
- Personality or values changes → `SOUL.md`

## Notification

When a learning needs human review, alert via the configured channel. To change this to
silent mode (just update `patterns.md` status without alerting), edit this line:

- **Human review notification:** alert
