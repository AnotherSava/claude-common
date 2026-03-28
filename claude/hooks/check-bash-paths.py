#!/usr/bin/env python3
"""PreToolUse hook: reject Bash commands that use `cd` prefixes or absolute paths."""

import json
import os
import sys

try:
    tool_input = json.load(sys.stdin)["tool_input"]
    cmd = tool_input["command"].strip()
except (json.JSONDecodeError, KeyError):
    sys.exit(0)

cwd = os.getcwd().replace(os.sep, "/").lower()
cl = cmd.lower().replace(os.sep, "/")

# On Windows, cwd looks like "d:/foo/bar" — build the Unix-style "/d/foo/bar" variant.
# On Linux/macOS, cwd already starts with "/" so no conversion is needed.
if len(cwd) >= 2 and cwd[1] == ":":
    unix = "/" + cwd[0] + cwd[2:]
else:
    unix = None


def _contains_path(haystack: str, path: str) -> bool:
    """Check if haystack contains path as a complete path prefix (not just a substring)."""
    start = 0
    while True:
        idx = haystack.find(path, start)
        if idx == -1:
            return False
        end = idx + len(path)
        # Accept if the match is followed by /, whitespace, end-of-string, or common delimiters
        if end >= len(haystack) or haystack[end] in ("/ \t\"';|&)"):
            return True
        start = idx + 1


if cmd.startswith("cd ") or cmd == "cd":
    msg = "Never prepend cd to commands."
elif _contains_path(cl, cwd) or (unix and _contains_path(cl, unix)):
    msg = "Use relative paths, not absolute."
else:
    sys.exit(0)

print(f"{msg} Working directory is already {os.getcwd()}.", file=sys.stderr)
sys.exit(2)
