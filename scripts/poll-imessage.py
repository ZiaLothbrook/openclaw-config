#!/usr/bin/env python3
"""
iMessage Poller — watches ~/Library/Messages/chat.db for new messages
from authorized contacts and fires Claude Code to handle them.

Runs every 30 seconds via launchd (com.deepgem.imessage-poller.plist).
Tracks last-processed message via a state file to avoid double-processing.
"""

import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time

# ── Config ──────────────────────────────────────────────────────────────────

CHAT_DB = os.path.expanduser("~/Library/Messages/chat.db")
STATE_FILE = os.path.expanduser("~/jarvis-config/.imessage-last-rowid")
JARVIS_CONFIG_DIR = os.path.expanduser("~/jarvis-config")
AUTHORIZED_SENDERS = {"+13033453071", "+13033453071"}  # Ziah's number

# Load env from .env file for ANTHROPIC_API_KEY
ENV_FILE = os.path.join(JARVIS_CONFIG_DIR, ".env")
env = {**os.environ}
if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()

# ── State ────────────────────────────────────────────────────────────────────

def get_last_rowid() -> int:
    if os.path.exists(STATE_FILE):
        try:
            return int(open(STATE_FILE).read().strip())
        except (ValueError, OSError):
            pass
    return 0


def save_last_rowid(rowid: int) -> None:
    with open(STATE_FILE, "w") as f:
        f.write(str(rowid))


# ── Database ─────────────────────────────────────────────────────────────────

def get_new_messages(last_rowid: int) -> list[dict]:
    """Read new inbound messages from chat.db since last_rowid."""
    if not os.path.exists(CHAT_DB):
        print(f"[imessage-poller] chat.db not found at {CHAT_DB}", file=sys.stderr)
        return []

    # Copy DB to temp file to avoid locking issues with Messages.app
    tmp = tempfile.mktemp(suffix=".db")
    try:
        shutil.copy2(CHAT_DB, tmp)
        conn = sqlite3.connect(tmp)
        conn.row_factory = sqlite3.Row

        # Get messages newer than last_rowid that are inbound (is_from_me = 0)
        rows = conn.execute("""
            SELECT
                m.ROWID,
                m.text,
                m.date,
                m.is_from_me,
                h.id AS sender
            FROM message m
            JOIN handle h ON m.handle_id = h.ROWID
            WHERE m.ROWID > ?
              AND m.is_from_me = 0
              AND m.text IS NOT NULL
              AND m.text != ''
            ORDER BY m.ROWID ASC
        """, (last_rowid,)).fetchall()

        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[imessage-poller] DB error: {e}", file=sys.stderr)
        return []
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


# ── Claude invocation ─────────────────────────────────────────────────────────

def run_claude(sender: str, text: str) -> None:
    prompt = (
        f'Incoming iMessage from {sender}: "{text}"\n\n'
        f"The sender is Ziah. Read your identity files (SOUL.md, USER.md, AGENTS.md), "
        f"then handle this message. Reply via iMessage using: "
        f"./skills/imessage/imessage send \"{sender}\" \"your reply\""
    )

    subprocess.Popen(
        ["claude", "--print", "--bare", "--dangerously-skip-permissions", prompt],
        cwd=JARVIS_CONFIG_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"[imessage-poller] Fired Claude for message from {sender}: {text[:60]!r}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    last_rowid = get_last_rowid()

    # On very first run with no state, initialize to current max rowid
    # so we don't replay old messages
    if last_rowid == 0:
        tmp = tempfile.mktemp(suffix=".db")
        try:
            shutil.copy2(CHAT_DB, tmp)
            conn = sqlite3.connect(tmp)
            row = conn.execute("SELECT MAX(ROWID) FROM message").fetchone()
            conn.close()
            if row and row[0]:
                save_last_rowid(row[0])
                print(f"[imessage-poller] Initialized at rowid {row[0]}")
            os.unlink(tmp)
        except Exception as e:
            print(f"[imessage-poller] Init error: {e}", file=sys.stderr)
        return

    messages = get_new_messages(last_rowid)

    for msg in messages:
        sender = msg["sender"]
        text = msg["text"].strip()
        rowid = msg["ROWID"]

        # Normalize sender number
        normalized = sender if sender.startswith("+") else f"+{sender}"

        if normalized in AUTHORIZED_SENDERS and text:
            run_claude(normalized, text)

        # Always advance the pointer, even for unauthorized senders
        last_rowid = max(last_rowid, rowid)

    if messages:
        save_last_rowid(last_rowid)


if __name__ == "__main__":
    main()
