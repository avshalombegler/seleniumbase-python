#!/usr/bin/env python
"""PreToolUse hook: block bare python/python3 Bash calls not using the conda env.

Exits 2 (blocking) with a corrective message when a bare 'python' or 'python3'
invocation is detected that doesn't reference the project conda environment.
"""

import json
import re
import sys

CONDA = "C:/Users/Avshalom/anaconda3/envs/seleniumbase-python/python.exe"

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

# Match 'python ' or 'python3 ' at command start, after shell operators (&&, |, ;, newline),
# or inside subshell $(...) invocations.
if re.search(r"(?:^|&&|\||;|\n|\$\()\s*(python3?)\s", cmd) and CONDA not in cmd:
    print(
        f"Use the project conda Python explicitly:\n"
        f"  {CONDA}\n"
        f"Or for linting/formatting use taskipy:\n"
        f"  task check   # ruff check .\n"
        f"  task fix     # ruff check . --fix && ruff format .",
        file=sys.stderr,
    )
    sys.exit(2)

sys.exit(0)
