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

subprocess.run([RUFF, "check", fp, "--fix", "--config", PYPROJECT], capture_output=True)
subprocess.run([RUFF, "format", fp, "--config", PYPROJECT], capture_output=True)
sys.exit(0)
