#!/usr/bin/env python
"""PostToolUse hook: ruff check --fix + ruff format after MCP file write tools.

MCP tools use tool_input.path (repo-relative), unlike native Write which uses
tool_input.file_path (absolute). Also checks tool_response.success before running.
"""

import json
import subprocess
import sys
from pathlib import Path

RUFF = "C:/Users/Avshalom/anaconda3/envs/seleniumbase-python/Scripts/ruff.exe"
# Derive repo root dynamically: .claude/hooks/ → .claude/ → repo root
REPO = Path(__file__).parent.parent.parent.resolve()
PYPROJECT = str(REPO / "pyproject.toml")

data = json.load(sys.stdin)

# Only run if the MCP tool reported success
response = data.get("tool_response", {})
if isinstance(response, str):
    try:
        response = json.loads(response)
    except Exception:
        sys.exit(0)
if not response.get("success", False):
    sys.exit(0)

rel_path = data.get("tool_input", {}).get("path", "")
if not rel_path.endswith(".py"):
    sys.exit(0)

abs_path = str(REPO / rel_path)
r1 = subprocess.run([RUFF, "check", abs_path, "--fix", "--config", PYPROJECT], capture_output=True)
r2 = subprocess.run([RUFF, "format", abs_path, "--config", PYPROJECT], capture_output=True)

if r1.returncode != 0:
    print(f"[ruff-hook] ruff check failed on {rel_path}:\n{r1.stderr.decode()}", file=sys.stderr)
if r2.returncode != 0:
    print(f"[ruff-hook] ruff format failed on {rel_path}:\n{r2.stderr.decode()}", file=sys.stderr)

sys.exit(0)
