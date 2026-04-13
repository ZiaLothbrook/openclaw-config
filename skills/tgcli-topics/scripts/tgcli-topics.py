#!/usr/bin/env python3
"""Single ready-to-run entrypoint for Telegram forum topic discovery.

This wrapper bootstraps Telethon into ~/.tgcli/venv when needed, converts tgcli's
session into Telethon format when missing or stale, then executes the discovery helper.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

TGCLI_DIR = Path("~/.tgcli").expanduser()
VENV_DIR = TGCLI_DIR / "venv"
VENV_PYTHON = VENV_DIR / "bin" / "python3"
DISCOVER_SCRIPT = Path(__file__).with_name("discover-topics.py")
CONVERT_SCRIPT = Path(__file__).with_name("convert-session.py")
TGCLI_SESSION = TGCLI_DIR / "session.json"
TELETHON_SESSION = TGCLI_DIR / "telethon-session.session"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)  # noqa: S603


def ensure_venv() -> None:
    if not VENV_PYTHON.exists():
        run([sys.executable, "-m", "venv", str(VENV_DIR)])


def ensure_telethon() -> None:
    probe = subprocess.run(  # noqa: S603
        [str(VENV_PYTHON), "-c", "import telethon"],
        check=False,
        capture_output=True,
        text=True,
    )
    if probe.returncode == 0:
        return
    run([str(VENV_PYTHON), "-m", "pip", "install", "telethon"])


def session_needs_conversion() -> bool:
    if not TGCLI_SESSION.exists():
        raise SystemExit(
            f"tgcli session not found at {TGCLI_SESSION}. Run `tgcli login` first."
        )
    if not TELETHON_SESSION.exists():
        return True
    return TGCLI_SESSION.stat().st_mtime > TELETHON_SESSION.stat().st_mtime


def ensure_converted_session() -> None:
    if session_needs_conversion():
        run([sys.executable, str(CONVERT_SCRIPT), "--force"])


def main() -> None:
    ensure_venv()
    ensure_telethon()
    ensure_converted_session()
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), str(DISCOVER_SCRIPT), *sys.argv[1:]])  # noqa: S606


if __name__ == "__main__":
    main()
