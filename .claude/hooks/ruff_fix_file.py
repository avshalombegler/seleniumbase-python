#!/usr/bin/env python
"""PostToolUse hook: ruff check --fix + ruff format after Write/Edit on .py files."""

import json
import subprocess
import sys

RUFF = "C:/Users/Avshalom/anaconda3/envs/seleniumbase-python/Scripts/ruff.exe"
PYPROJECT = "E:/VSCodeProjects/seleniumbase-python/pyproject.toml"

data = json.load(sys.stdin)
fp = data.get("tool_input", {}).get("file_path", "")

if not fp.endswith(".py"):
    sys.exit(0)

r1 = subprocess.run([RUFF, "check", fp, "--fix", "--config", PYPROJECT], capture_output=True)
r2 = subprocess.run([RUFF, "format", fp, "--config", PYPROJECT], capture_output=True)

if r1.returncode != 0:
    print(f"[ruff-hook] ruff check failed on {fp}:\n{r1.stderr.decode()}", file=sys.stderr)
if r2.returncode != 0:
    print(f"[ruff-hook] ruff format failed on {fp}:\n{r2.stderr.decode()}", file=sys.stderr)

sys.exit(0)
