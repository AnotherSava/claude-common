#!/usr/bin/env python3
"""UserPromptSubmit hook: record the last prompt for idle-notification checks."""

import hashlib
import json
import sys
import tempfile
from pathlib import Path

try:
    data = json.loads(sys.stdin.read())
    prompt = data.get("prompt", "") if isinstance(data, dict) else ""
except json.JSONDecodeError:
    sys.exit(0)

project_id = hashlib.md5(str(Path.cwd()).encode()).hexdigest()[:12]
last_active = Path(tempfile.gettempdir()) / f"claude-last-active-{project_id}"
last_active.write_text(prompt, encoding="utf-8")
last_active.chmod(0o600)
