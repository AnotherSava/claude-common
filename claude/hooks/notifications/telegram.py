#!/usr/bin/env python3
import hashlib
import os
import sys
import tempfile
import time
from pathlib import Path

from dotenv import load_dotenv
import requests

load_dotenv(Path(__file__).resolve().parent / ".env")

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
if not TOKEN or not CHAT_ID:
    sys.exit(0)

def notify(text: str) -> None:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    r = requests.post(url, json=params, timeout=10)
    r.raise_for_status()

PROJECT_ROOT = Path.cwd()
PROJECT_NAME = PROJECT_ROOT.name
_project_id = hashlib.md5(str(PROJECT_ROOT).encode()).hexdigest()[:12]
LAST_ACTIVE_FILE = Path(tempfile.gettempdir()) / f"claude-last-active-{_project_id}"
NOTIFICATION_DELAY = 60  # seconds

def last_active_info() -> tuple[bool, str]:
    """Return (was_recently_active, last_prompt)."""
    try:
        age = time.time() - LAST_ACTIVE_FILE.stat().st_mtime
        prompt = LAST_ACTIVE_FILE.read_text(encoding="utf-8").strip()
        return age < NOTIFICATION_DELAY, prompt
    except FileNotFoundError:
        return False, ""

if __name__ == "__main__":
    import json
    if not sys.stdin.isatty():
        hook_input = json.loads(sys.stdin.read())
        message = hook_input.get("message", "")
        if message:
            time.sleep(NOTIFICATION_DELAY)
            active, last_prompt = last_active_info()
            if not active:
                text = f"[{PROJECT_NAME}] {message}"
                if last_prompt:
                    text += f":\n\n{last_prompt[:200]}"
                notify(text)
    elif len(sys.argv) >= 2:
        notify(sys.argv[1])
    else:
        print("Usage: telegram.py 'message text'", file=sys.stderr)
        sys.exit(1)
