"""
SeleniumBase MCP Server

Provides 19 tools across 5 groups for test execution, file I/O, HTML analysis,
code scaffolding, and session budget tracking. Used by sb-healer, sb-generator,
and sb-planner Claude Code agents.

Tool groups:
  Group 1 — Execution:  run_pytest, get_test_results
  Group 2 — File:       read_file, write_file, backup_file, cleanup_backups,
                        validate_python, insert_into_file, list_files, get_project_structure
  Group 3 — Analysis:   get_page_source, analyze_page_elements, parse_pytest_failure
  Group 4 — Scaffold:   create_test_file, create_page_object_file,
                        create_locators_file, get_code_template
  Group 5 — Budget:     get_session_stats, reset_session_stats
"""

from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# server.py is at tools/seleniumbase-mcp/server.py
# REPO_ROOT is three levels up: tools/seleniumbase-mcp -> tools -> repo_root
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
REPORT_PATH = REPO_ROOT / ".pytest_mcp_report.json"

# ---------------------------------------------------------------------------
# Session Budget System
# ---------------------------------------------------------------------------

SESSION_LIMITS = {
    "max_total_tool_calls": 200,
    "max_pytest_runs": 30,
    "max_browser_inspections": 15,
    "max_fixes_attempted": 25,
    "max_elapsed_minutes": 30,
    "caution_threshold_pct": 0.6,  # 60% of any limit → "caution"
    "critical_threshold_pct": 0.85,  # 85% of any limit → "critical"
}

_session_state: dict[str, Any] = {
    "total_tool_calls": 0,
    "total_pytest_runs": 0,
    "total_browser_inspections": 0,
    "total_fixes_attempted": 0,
    "total_fixes_succeeded": 0,
    "tests_remaining": 0,
    "session_start_time": None,
    "_pending_verification": False,
    "_call_history": {},  # key: (tool_name, frozen_args) → count
}


def _record_tool_call() -> None:
    """Increment total_tool_calls and set session_start_time on the first call."""
    if _session_state["session_start_time"] is None:
        _session_state["session_start_time"] = time.time()
    _session_state["total_tool_calls"] += 1


def _check_duplicate_call(tool_name: str, **kwargs) -> str | None:
    """Track tool calls by (tool_name, args). Return a warning if call count >= 3."""
    key = (tool_name, tuple(sorted((k, v if v is not None else "__NONE__") for k, v in kwargs.items())))
    _session_state["_call_history"][key] = _session_state["_call_history"].get(key, 0) + 1
    count = _session_state["_call_history"][key]
    if count >= 3:
        return (
            f"LOOP_WARNING: This exact {tool_name} call has been made {count} times "
            f"with identical arguments. This is likely a loop. Re-examine your assumptions "
            f"about file paths or nodeids before retrying. Use list_files or "
            f"run_pytest --collect-only to discover correct paths."
        )
    return None


def _compute_budget_status() -> str:
    """Return 'healthy', 'caution', or 'critical' based on current counters."""
    caution_pct = SESSION_LIMITS["caution_threshold_pct"]
    critical_pct = SESSION_LIMITS["critical_threshold_pct"]

    start = _session_state["session_start_time"]
    elapsed_minutes = (time.time() - start) / 60.0 if start else 0.0

    ratios = [
        _session_state["total_tool_calls"] / SESSION_LIMITS["max_total_tool_calls"],
        _session_state["total_pytest_runs"] / SESSION_LIMITS["max_pytest_runs"],
        _session_state["total_browser_inspections"] / SESSION_LIMITS["max_browser_inspections"],
        _session_state["total_fixes_attempted"] / SESSION_LIMITS["max_fixes_attempted"],
        elapsed_minutes / SESSION_LIMITS["max_elapsed_minutes"],
    ]

    max_ratio = max(ratios)
    if max_ratio >= critical_pct:
        return "critical"
    elif max_ratio >= caution_pct:
        return "caution"
    return "healthy"


# ---------------------------------------------------------------------------
# MCP server instance
# ---------------------------------------------------------------------------

mcp = FastMCP("seleniumbase")

# ===========================================================================
# Group 1: Execution Tools  (2 tools: run_pytest, get_test_results)
# ===========================================================================


@mcp.tool()
def run_pytest(
    test_path: str,
    markers: str | None = None,
    browser: str = "chrome",
    headless: bool = True,
    timeout: int = 300,
) -> dict[str, Any]:
    """Run pytest on a test path and return structured results.

    Use this tool to execute tests against the seleniumbase-python project.
    Supports running a single file, a directory, or a specific test node
    (e.g. 'tests/the_internet/ui_test_suite/test_ab_testing.py' or
    'tests/the_internet/ui_test_suite/test_ab_testing.py::TestABTesting::test_ab_testing_content').

    Args:
        test_path: Path to test file, directory, or nodeid relative to repo root.
        markers: Optional pytest -m expression (e.g. 'regression', 'smoke or ui').
        browser: Browser to use (default 'chrome').
        headless: Run browser in headless mode (default True).
        timeout: Subprocess timeout in seconds (default 300). Use higher values for
                 directory-level runs; lower values (e.g. 60) for single-test verification.

    Returns:
        dict with keys: exit_code, passed, failed, errors, duration, failures.
        Each item in failures has: nodeid, message, longrepr.
    """
    _record_tool_call()
    _session_state["total_pytest_runs"] += 1
    warning = _check_duplicate_call("run_pytest", test_path=test_path, markers=markers)

    abs_test_path = REPO_ROOT / test_path if not Path(test_path).is_absolute() else Path(test_path)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(abs_test_path),
        f"--browser={browser}",
        "--json-report",
        f"--json-report-file={REPORT_PATH}",
        "--tb=long",
        "--no-header",
        "-q",
    ]

    if headless:
        cmd.append("--headless")

    if markers:
        cmd.extend(["-m", markers])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(REPO_ROOT),
        )
    except subprocess.TimeoutExpired:
        _session_state["_pending_verification"] = False
        return {
            "exit_code": -1,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "duration": 0.0,
            "failures": [{"nodeid": test_path, "message": f"Timeout after {timeout}s", "longrepr": ""}],
        }

    # Parse report if it exists
    report = _parse_report(result.returncode)

    # Track fix verification: if a write was pending and this run passed, count it
    if _session_state["_pending_verification"]:
        if report.get("exit_code") == 0 and report.get("failed", 1) == 0 and report.get("errors", 1) == 0:
            _session_state["total_fixes_succeeded"] += 1
        _session_state["_pending_verification"] = False

    if warning:
        report["warning"] = warning
    return report


@mcp.tool()
def get_test_results() -> dict[str, Any]:
    """Read and return the structured results from the last run_pytest call.

    Returns the same schema as run_pytest: exit_code, passed, failed, errors,
    duration, failures (each with nodeid, message, longrepr).
    Returns {"error": "No report found"} if no report exists yet.
    """
    _record_tool_call()
    if not REPORT_PATH.exists():
        return {"error": "No report found"}
    return _parse_report(exit_code=None)


def _parse_report(exit_code: int | None) -> dict[str, Any]:
    """Internal helper: parse .pytest_mcp_report.json into a standard dict."""
    if not REPORT_PATH.exists():
        return {
            "exit_code": exit_code if exit_code is not None else -1,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "duration": 0.0,
            "failures": [{"nodeid": "", "message": "Report file not found", "longrepr": ""}],
        }

    try:
        with open(REPORT_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        return {
            "exit_code": exit_code if exit_code is not None else -1,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "duration": 0.0,
            "failures": [{"nodeid": "", "message": f"Failed to parse report: {exc}", "longrepr": ""}],
        }

    summary = data.get("summary", {})
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    errors = summary.get("error", 0)
    duration = data.get("duration", 0.0)

    failures = []
    for test in data.get("tests", []):
        outcome = test.get("outcome", "")
        if outcome in ("failed", "error"):
            call = test.get("call", {})
            longrepr = call.get("longrepr", "") or test.get("longrepr", "")
            crash = call.get("crash", {})
            message = crash.get("message", "") if crash else longrepr[:200]
            failures.append(
                {
                    "nodeid": test.get("nodeid", ""),
                    "message": message,
                    "longrepr": longrepr,
                }
            )

    return {
        "exit_code": exit_code if exit_code is not None else (0 if failed == 0 and errors == 0 else 1),
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "duration": duration,
        "failures": failures,
    }


# ===========================================================================
# Group 2: File Tools  (8 tools: read_file, write_file, backup_file,
#                       cleanup_backups, validate_python, insert_into_file,
#                       list_files, get_project_structure)
# ===========================================================================


@mcp.tool()
def read_file(path: str) -> str:
    """Read and return the full text content of any file in the repository.

    Args:
        path: Path relative to repo root (e.g. 'src/pages/base/base_page.py').

    Returns:
        Raw string content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    _record_tool_call()
    warning = _check_duplicate_call("read_file", path=path)
    abs_path = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)
    if not abs_path.exists():
        msg = f"File not found: {abs_path}"
        if warning:
            msg += f"\n\n{warning}"
        raise FileNotFoundError(msg)
    content = abs_path.read_text(encoding="utf-8")
    if warning:
        return f"⚠️ {warning}\n\n---\n\n{content}"
    return content


@mcp.tool()
def write_file(path: str, content: str) -> dict[str, Any]:
    """Write content to a file, creating parent directories if needed.

    For .py files, validates Python syntax before writing. Returns an error
    dict if syntax is invalid — the file is NOT written in that case.

    Args:
        path: Destination path relative to repo root.
        content: Text content to write.

    Returns:
        dict with keys: success (bool), path (str), bytes_written (int).
        On syntax error: success (False), error (str), path (str).
    """
    import py_compile
    import tempfile

    _record_tool_call()
    abs_path = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)

    # Validate Python syntax before writing
    if path.endswith(".py"):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", encoding="utf-8", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            py_compile.compile(tmp_path, doraise=True)
        except py_compile.PyCompileError as exc:
            Path(tmp_path).unlink(missing_ok=True)
            return {
                "success": False,
                "error": f"Python syntax error — file NOT written: {exc}",
                "path": path,
            }
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    abs_path.parent.mkdir(parents=True, exist_ok=True)
    encoded = content.encode("utf-8")
    abs_path.write_bytes(encoded)

    # Track fix attempts: any successful .py write counts as a fix attempt
    if path.endswith(".py"):
        _session_state["total_fixes_attempted"] += 1
        _session_state["_pending_verification"] = True

    return {"success": True, "path": str(abs_path.relative_to(REPO_ROOT)), "bytes_written": len(encoded)}


@mcp.tool()
def backup_file(path: str) -> dict[str, Any]:
    """Create a backup of a file before modifying it.

    Copies the file to <path>.bak in the same directory. Call this before
    any write_file call on an existing file so the original can be restored
    if the fix introduces new failures.

    Args:
        path: Path relative to repo root of the file to back up.

    Returns:
        dict with keys: success (bool), backup_path (str), original_path (str).
        Returns success: False with an error key if the file does not exist.
    """
    import shutil

    _record_tool_call()
    abs_path = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)
    if not abs_path.exists():
        return {"success": False, "error": f"File not found: {path}", "original_path": path}

    backup_path = abs_path.with_suffix(abs_path.suffix + ".bak")
    shutil.copy2(abs_path, backup_path)
    return {
        "success": True,
        "original_path": str(abs_path.relative_to(REPO_ROOT)),
        "backup_path": str(backup_path.relative_to(REPO_ROOT)),
    }


@mcp.tool()
def cleanup_backups(directory: str = ".") -> dict[str, Any]:
    """Delete all .bak files created by backup_file under a directory and the transient .pytest_mcp_report.json file.

    Call this after a fully successful healing session (final run passes with
    no failures) to remove backup files that are no longer needed.

    Args:
        directory: Directory path relative to repo root to search (default '.').

    Returns:
        dict with keys: deleted (list of deleted relative paths), count (int).
    """
    _record_tool_call()
    abs_dir = REPO_ROOT / directory if not Path(directory).is_absolute() else Path(directory)
    deleted = []
    for p in abs_dir.rglob("*.bak"):
        if p.is_file():
            rel = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
            p.unlink()
            deleted.append(rel)
    # Remove transient pytest report file
    if REPORT_PATH.exists():
        rel = str(REPORT_PATH.relative_to(REPO_ROOT)).replace("\\", "/")
        REPORT_PATH.unlink()
        deleted.append(rel)
    return {"deleted": sorted(deleted), "count": len(deleted)}


@mcp.tool()
def validate_python(code: str) -> dict[str, Any]:
    """Check a Python code string for syntax errors without writing to disk.

    Use this during code generation to validate snippets or complete file
    content before calling write_file or create_test_file.

    Args:
        code: Python source code string to validate.

    Returns:
        dict with keys:
          - valid (bool): True if syntax is correct
          - error (str | None): Syntax error message if invalid, None if valid
          - line (int | None): Line number of the error if invalid, None if valid
    """
    import py_compile
    import tempfile

    _record_tool_call()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", encoding="utf-8", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        py_compile.compile(tmp_path, doraise=True)
        return {"valid": True, "error": None, "line": None}
    except py_compile.PyCompileError as exc:
        msg = str(exc)
        line_match = re.search(r"line (\d+)", msg)
        line = int(line_match.group(1)) if line_match else None
        return {"valid": False, "error": msg, "line": line}
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@mcp.tool()
def insert_into_file(path: str, anchor: str, content: str, position: str = "after") -> dict[str, Any]:
    """Insert content into a file relative to an anchor string.

    Finds the first occurrence of `anchor` in the file and inserts `content`
    either immediately before or after it. For .py files, validates syntax
    after insertion before writing.

    Use this for surgical additions to shared files like main_page.py where
    writing the entire file risks corrupting existing content.

    Args:
        path: File path relative to repo root.
        anchor: Exact string to search for in the file (must be unique).
        content: Text to insert. For "after", inserted on a new line immediately
                 after the anchor line. For "before", inserted on a new line
                 immediately before the anchor line.
        position: "after" (default) or "before".

    Returns:
        dict with keys: success (bool), path (str), bytes_written (int).
        On anchor not found: success (False), error (str).
        On non-unique anchor: success (False), error (str).
        On syntax error: success (False), error (str) — file NOT written.
    """
    import py_compile
    import tempfile

    _record_tool_call()
    warning = _check_duplicate_call("insert_into_file", path=path, anchor=anchor, content=content, position=position)
    abs_path = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)
    if not abs_path.exists():
        result = {"success": False, "error": f"File not found: {path}", "path": path}
        if warning:
            result["warning"] = warning
        return result

    original = abs_path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)

    # Find anchor line
    anchor_indices = [i for i, line in enumerate(lines) if anchor in line]
    if not anchor_indices:
        result = {"success": False, "error": f"Anchor not found: {repr(anchor)}", "path": path}
        if warning:
            result["warning"] = warning
        return result
    if len(anchor_indices) > 1:
        result = {
            "success": False,
            "error": f"Anchor matches {len(anchor_indices)} lines — must be unique. "
            f"Found at lines: {[i + 1 for i in anchor_indices]}",
            "path": path,
        }
        if warning:
            result["warning"] = warning
        return result

    insert_idx = anchor_indices[0]
    insertion_line = content if content.endswith("\n") else content + "\n"

    if position == "after":
        lines.insert(insert_idx + 1, insertion_line)
    elif position == "before":
        lines.insert(insert_idx, insertion_line)
    else:
        result = {
            "success": False,
            "error": f"Invalid position: {repr(position)}. Must be 'after' or 'before'.",
            "path": path,
        }
        if warning:
            result["warning"] = warning
        return result

    new_content = "".join(lines)

    # Validate Python syntax before writing
    if path.endswith(".py"):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", encoding="utf-8", delete=False) as tmp:
            tmp.write(new_content)
            tmp_path = tmp.name
        try:
            py_compile.compile(tmp_path, doraise=True)
        except py_compile.PyCompileError as exc:
            Path(tmp_path).unlink(missing_ok=True)
            result = {
                "success": False,
                "error": f"Python syntax error after insertion — file NOT written: {exc}",
                "path": path,
            }
            if warning:
                result["warning"] = warning
            return result
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    encoded = new_content.encode("utf-8")
    abs_path.write_bytes(encoded)
    result = {
        "success": True,
        "path": str(abs_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "bytes_written": len(encoded),
    }
    if warning:
        result["warning"] = warning
    return result


@mcp.tool()
def list_files(directory: str = ".", pattern: str = "*.py") -> list[str]:
    """List all files under a directory matching a glob pattern.

    Args:
        directory: Directory path relative to repo root (default '.').
        pattern: Glob pattern to match filenames (e.g. 'test_*.py', '*.py').

    Returns:
        List of relative paths (from repo root) matching the pattern.
    """
    _record_tool_call()
    abs_dir = REPO_ROOT / directory if not Path(directory).is_absolute() else Path(directory)
    if not abs_dir.exists():
        return []

    results = []
    for p in abs_dir.rglob("*"):
        if p.is_file() and fnmatch.fnmatch(p.name, pattern):
            results.append(str(p.relative_to(REPO_ROOT)).replace("\\", "/"))
    return sorted(results)


@mcp.tool()
def get_project_structure() -> dict[str, Any]:
    """Return a structured snapshot of the project's test and page object landscape.

    Use this to understand what features already have coverage before planning
    new tests, or to detect naming collisions before creating new files.

    Returns:
        dict with keys:
          - features: list of feature dicts, each with:
              - name (str): feature directory name (snake_case)
              - has_locators (bool): locators.py exists
              - has_page_object (bool): at least one *_page.py exists
              - page_object_file (str | None): path to the page object file
              - test_files (list[str]): paths to test_*.py files in tests/ for this feature
          - untested_features: list of feature names that have page objects but no tests
          - total_tests: int
          - total_features: int
    """
    _record_tool_call()
    features_dir = REPO_ROOT / "src" / "pages" / "features"
    tests_dir = REPO_ROOT / "tests"

    features = []
    for feature_path in sorted(features_dir.iterdir()):
        if not feature_path.is_dir():
            continue

        name = feature_path.name
        has_locators = (feature_path / "locators.py").exists()

        page_files = list(feature_path.glob("*_page.py"))
        has_page_object = bool(page_files)
        page_object_file = str(page_files[0].relative_to(REPO_ROOT)).replace("\\", "/") if page_files else None

        # Find test files — search recursively under tests/ for files containing this feature name
        test_files = []
        for tf in tests_dir.rglob("test_*.py"):
            if name.replace("_", "") in tf.stem.replace("_", ""):
                test_files.append(str(tf.relative_to(REPO_ROOT)).replace("\\", "/"))

        features.append(
            {
                "name": name,
                "has_locators": has_locators,
                "has_page_object": has_page_object,
                "page_object_file": page_object_file,
                "test_files": sorted(test_files),
            }
        )

    untested = [f["name"] for f in features if f["has_page_object"] and not f["test_files"]]

    total_tests = sum(1 for _ in tests_dir.rglob("test_*.py"))

    return {
        "features": features,
        "untested_features": untested,
        "total_tests": total_tests,
        "total_features": len(features),
    }


# ===========================================================================
# Group 3: Analysis Tools  (3 tools: get_page_source, analyze_page_elements,
#                            parse_pytest_failure)
# ===========================================================================


@mcp.tool()
def get_page_source(url: str) -> str:
    """Fetch the raw HTML source of a URL using requests.

    Use this to retrieve a page's HTML before calling analyze_page_elements.

    Args:
        url: Full URL to fetch (e.g. 'https://the-internet.herokuapp.com/login').

    Returns:
        Raw HTML string, or a JSON-encoded error dict on failure.
    """
    _record_tool_call()
    _session_state["total_browser_inspections"] += 1
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        return json.dumps({"error": str(exc), "url": url})


@mcp.tool()
def analyze_page_elements(html: str) -> dict[str, Any]:
    """Parse HTML and return a structured summary of interactive elements.

    Use this after get_page_source to understand what selectors to use when
    writing page objects and locators.

    Args:
        html: Raw HTML string to parse.

    Returns:
        dict with keys:
          - inputs: list of {type, id, name, placeholder, selector}
          - buttons: list of {text, type, id, selector}
          - links: list of {text, href, selector}
          - selects: list of {id, name, options, selector}
          - forms: list of {action, method, field_count}
    """
    _record_tool_call()
    soup = BeautifulSoup(html, "html.parser")

    inputs = []
    for el in soup.find_all("input"):
        input_id = el.get("id", "")
        input_name = el.get("name", "")
        input_type = el.get("type", "text")
        placeholder = el.get("placeholder", "")

        # Build the best CSS selector
        if input_id:
            selector = f"#{input_id}"
        elif input_name:
            selector = f"input[name='{input_name}']"
        else:
            selector = f"input[type='{input_type}']"

        inputs.append(
            {
                "type": input_type,
                "id": input_id,
                "name": input_name,
                "placeholder": placeholder,
                "selector": selector,
            }
        )

    buttons = []
    for el in soup.find_all("button"):
        btn_id = el.get("id", "")
        btn_type = el.get("type", "button")
        text = el.get_text(strip=True)

        if btn_id:
            selector = f"#{btn_id}"
        else:
            selector = f"button[type='{btn_type}']" if btn_type else "button"

        buttons.append({"text": text, "type": btn_type, "id": btn_id, "selector": selector})

    # Also capture input[type=submit] and input[type=button] as buttons
    for el in soup.find_all("input", type=lambda t: t in ("submit", "button", "reset")):
        btn_id = el.get("id", "")
        btn_type = el.get("type", "submit")
        text = el.get("value", btn_type)

        if btn_id:
            selector = f"#{btn_id}"
        else:
            selector = f"input[type='{btn_type}']"

        buttons.append({"text": text, "type": btn_type, "id": btn_id, "selector": selector})

    links = []
    for el in soup.find_all("a"):
        href = el.get("href", "")
        text = el.get_text(strip=True)
        link_id = el.get("id", "")

        if link_id:
            selector = f"#{link_id}"
        elif href:
            selector = f"a[href='{href}']"
        else:
            selector = "a"

        links.append({"text": text, "href": href, "selector": selector})

    selects = []
    for el in soup.find_all("select"):
        sel_id = el.get("id", "")
        sel_name = el.get("name", "")
        options = [opt.get_text(strip=True) for opt in el.find_all("option")]

        if sel_id:
            selector = f"#{sel_id}"
        elif sel_name:
            selector = f"select[name='{sel_name}']"
        else:
            selector = "select"

        selects.append({"id": sel_id, "name": sel_name, "options": options, "selector": selector})

    forms = []
    for el in soup.find_all("form"):
        action = el.get("action", "")
        method = el.get("method", "get").upper()
        field_count = len(el.find_all(["input", "select", "textarea"]))
        forms.append({"action": action, "method": method, "field_count": field_count})

    return {
        "inputs": inputs,
        "buttons": buttons,
        "links": links,
        "selects": selects,
        "forms": forms,
    }


@mcp.tool()
def parse_pytest_failure(longrepr: str) -> dict[str, Any]:
    """Parse a pytest failure longrepr (traceback text) into structured fields.

    Use this to extract actionable information from a test failure before
    attempting to heal a broken locator or test.

    Args:
        longrepr: The full pytest longrepr/traceback string from a test failure.

    Returns:
        dict with keys:
          - file: source file path where the failure occurred
          - line: line number of the failure (int or None)
          - error_type: e.g. 'NoSuchElementException', 'AssertionError'
          - failed_selector: CSS selector or locator that failed (if detectable)
          - assertion_message: assertion message if it's an assertion failure
          - raw: the full longrepr string
    """
    _record_tool_call()
    result: dict[str, Any] = {
        "file": None,
        "line": None,
        "error_type": None,
        "failed_selector": None,
        "assertion_message": None,
        "raw": longrepr,
    }

    # Extract file and line: patterns like "src/pages/foo.py:42:" or "FAILED tests/...::test - "
    file_line_match = re.search(r"([A-Za-z]:[\\/][\w/\\.\-]+\.py|[\w/\\.\-]+\.py)[:\s]+(\d+)", longrepr)
    if file_line_match:
        result["file"] = file_line_match.group(1).replace("\\", "/")
        result["line"] = int(file_line_match.group(2))

    # Extract error type from the last Exception line
    error_type_match = re.search(
        r"(NoSuchElementException|ElementNotVisibleException|TimeoutException|"
        r"AssertionError|StaleElementReferenceException|WebDriverException|"
        r"ElementClickInterceptedException|NoSuchWindowException|"
        r"InvalidSelectorException|MoveTargetOutOfBoundsException|"
        r"[\w]+Error|[\w]+Exception)",
        longrepr,
    )
    if error_type_match:
        result["error_type"] = error_type_match.group(1)

    # Extract failed selector — look for selector patterns in quotes
    selector_match = re.search(
        r'["\']([#.\[\]:\w\s\-=\'\"^$*]+)["\'].*(?:not found|not visible|timed out|Unable to locate)',
        longrepr,
        re.IGNORECASE,
    )
    if selector_match:
        result["failed_selector"] = selector_match.group(1)
    else:
        # Fallback: look for CSS-like strings after 'selector' keyword
        sel_kw_match = re.search(r'selector[=:\s]+["\']?([^"\'\s,\)]+)', longrepr, re.IGNORECASE)
        if sel_kw_match:
            result["failed_selector"] = sel_kw_match.group(1)

    # Extract assertion message
    assert_match = re.search(r"AssertionError:\s*(.+)", longrepr)
    if assert_match:
        result["assertion_message"] = assert_match.group(1).strip()

    return result


# ===========================================================================
# Group 4: Scaffold Tools  (4 tools: create_test_file, create_page_object_file,
#                            create_locators_file, get_code_template)
# ===========================================================================


def _to_relative(path: str) -> str:
    """Normalize path to repo-relative. Strips REPO_ROOT prefix if absolute."""
    p = Path(path)
    if p.is_absolute():
        try:
            return str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            pass
    return path.replace("\\", "/")


@mcp.tool()
def create_test_file(path: str, content: str) -> dict[str, Any]:
    """Create a new test file in the tests/ directory.

    Validates that the path starts with 'tests/' and ends with '.py'.
    Creates parent directories as needed.

    Args:
        path: Destination path relative to repo root (must start with 'tests/' and end with '.py').
              Absolute paths rooted at the repo root are also accepted.
        content: Full Python source code for the test file.

    Returns:
        dict with keys: success (bool), path (str).

    Raises:
        ValueError: If path does not start with 'tests/' or does not end with '.py'.
    """
    _record_tool_call()
    norm = _to_relative(path)
    if not norm.startswith("tests/"):
        raise ValueError(f"Test file path must start with 'tests/', got: {path}")
    if not norm.endswith(".py"):
        raise ValueError(f"Test file path must end with '.py', got: {path}")

    abs_path = REPO_ROOT / norm
    if abs_path.exists():
        return {
            "success": False,
            "error": f"File already exists at '{norm}'. Delete it first or use write_file() to overwrite intentionally.",
            "path": norm,
        }

    result = write_file(norm, content)
    if not result.get("success"):
        return {"success": False, "path": norm, "error": result.get("error", "Write failed")}
    return {"success": True, "path": norm}


@mcp.tool()
def create_page_object_file(path: str, content: str) -> dict[str, Any]:
    """Create a new page object file in the src/pages/ directory.

    Validates that the path starts with 'src/pages/' and ends with '.py'.
    Creates parent directories as needed.

    Args:
        path: Destination path relative to repo root (must start with 'src/pages/' and end with '.py').
              Absolute paths rooted at the repo root are also accepted.
        content: Full Python source code for the page object.

    Returns:
        dict with keys: success (bool), path (str).

    Raises:
        ValueError: If path validation fails.
    """
    _record_tool_call()
    norm = _to_relative(path)
    if not norm.startswith("src/pages/"):
        raise ValueError(f"Page object path must start with 'src/pages/', got: {path}")
    if not norm.endswith(".py"):
        raise ValueError(f"Page object path must end with '.py', got: {path}")

    abs_path = REPO_ROOT / norm
    if abs_path.exists():
        return {
            "success": False,
            "error": f"File already exists at '{norm}'. Delete it first or use write_file() to overwrite intentionally.",
            "path": norm,
        }

    result = write_file(norm, content)
    if not result.get("success"):
        return {"success": False, "path": norm, "error": result.get("error", "Write failed")}
    return {"success": True, "path": norm}


@mcp.tool()
def create_locators_file(path: str, content: str) -> dict[str, Any]:
    """Create a new locators file in the src/pages/ directory.

    Validates that the path starts with 'src/pages/' and ends with 'locators.py'.
    Creates parent directories as needed.

    Args:
        path: Destination path relative to repo root
              (must start with 'src/pages/' and end with 'locators.py').
              Absolute paths rooted at the repo root are also accepted.
        content: Full Python source code for the locators file.

    Returns:
        dict with keys: success (bool), path (str).

    Raises:
        ValueError: If path validation fails.
    """
    _record_tool_call()
    norm = _to_relative(path)
    if not norm.startswith("src/pages/"):
        raise ValueError(f"Locators file path must start with 'src/pages/', got: {path}")
    if not norm.endswith("locators.py"):
        raise ValueError(f"Locators file path must end with 'locators.py', got: {path}")

    abs_path = REPO_ROOT / norm
    if abs_path.exists():
        return {
            "success": False,
            "error": f"File already exists at '{norm}'. Delete it first or use write_file() to overwrite intentionally.",
            "path": norm,
        }

    result = write_file(norm, content)
    if not result.get("success"):
        return {"success": False, "path": norm, "error": result.get("error", "Write failed")}
    return {"success": True, "path": norm}


@mcp.tool()
def get_code_template(template_type: str, name: str) -> str:
    """Return a starter code template following the repo's exact patterns.

    Use this before create_test_file / create_page_object_file / create_locators_file
    to get a properly structured starting point.

    Args:
        template_type: One of 'test_class', 'page_object', 'locators'.
        name: Feature name, e.g. 'Checkboxes' or 'dropdown_list'.
              PascalCase is used for class names; snake_case for file/method names.

    Returns:
        String containing the template code with placeholders filled in.

    Raises:
        ValueError: If template_type is not one of the three valid types.
    """
    _record_tool_call()
    # Derive naming variants
    # Convert to snake_case for method/file names
    # e.g. "CheckboxPage" -> "checkbox_page", "dropdown_list" -> "dropdown_list"
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower().strip("_")
    snake = re.sub(r"[^a-z0-9_]", "_", snake).strip("_")

    # PascalCase class name
    pascal = "".join(word.capitalize() for word in re.split(r"[_\s]+", name))

    # Human-readable feature name
    feature_name = " ".join(word.capitalize() for word in re.split(r"[_\s]+", name))

    # sub-suite name (same as feature_name)
    sub_suite = feature_name

    # feature directory (snake_case)
    feature_dir = snake

    if template_type == "test_class":
        return f'''import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("{sub_suite}")
class Test{pascal}(UiBaseCase):
    """Tests {feature_name} functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_{snake}(self) -> None:
        self.logger.info("Tests {feature_name}.")
        main_page = MainPage(self)
        page = main_page.click_{snake}_link()

        # TODO: Add test steps
'''

    elif template_type == "page_object":
        return f'''from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.{feature_dir}.locators import {pascal}Locators

if TYPE_CHECKING:
    pass


class {pascal}Page(BasePage):
    """Page object for the {feature_name} page"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load({pascal}Locators.PAGE_LOADED_INDICATOR)

    # TODO: Add page methods
'''

    elif template_type == "locators":
        return f'''"""
Module containing locators for {feature_name} page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class {pascal}Locators:
    PAGE_LOADED_INDICATOR: Locator = {{"selector": ".example h2", "by": By.CSS_SELECTOR}}
    # TODO: Add locators
'''

    else:
        raise ValueError(
            f"Unknown template_type '{template_type}'. Must be one of: 'test_class', 'page_object', 'locators'."
        )


# ===========================================================================
# Group 5: Budget Tools  (2 tools: get_session_stats, reset_session_stats)
# ===========================================================================


@mcp.tool()
def get_session_stats() -> dict[str, Any]:
    """Return current session budget counters and derived efficiency metrics.

    Call this after completing each failure group to check the budget_status
    and decide whether to continue in normal mode, switch to lightweight mode,
    or enter wrap-up mode.

    Returns:
        dict with keys:
          - total_tool_calls (int)
          - total_pytest_runs (int)
          - total_browser_inspections (int)
          - total_fixes_attempted (int)
          - total_fixes_succeeded (int)
          - tests_remaining (int)
          - session_start_time (float | None)
          - elapsed_minutes (float)
          - fix_success_rate (float): succeeded / attempted, or 0.0 if none attempted
          - avg_tool_calls_per_fix (float)
          - budget_status (str): one of "healthy", "caution", "critical"
    """
    _record_tool_call()
    start = _session_state["session_start_time"]
    elapsed_minutes = (time.time() - start) / 60.0 if start else 0.0

    attempted = _session_state["total_fixes_attempted"]
    succeeded = _session_state["total_fixes_succeeded"]

    fix_success_rate = succeeded / attempted if attempted > 0 else 0.0
    avg_tool_calls_per_fix = _session_state["total_tool_calls"] / attempted if attempted > 0 else 0.0

    return {
        "total_tool_calls": _session_state["total_tool_calls"],
        "total_pytest_runs": _session_state["total_pytest_runs"],
        "total_browser_inspections": _session_state["total_browser_inspections"],
        "total_fixes_attempted": attempted,
        "total_fixes_succeeded": succeeded,
        "tests_remaining": _session_state["tests_remaining"],
        "session_start_time": _session_state["session_start_time"],
        "elapsed_minutes": round(elapsed_minutes, 2),
        "fix_success_rate": round(fix_success_rate, 3),
        "avg_tool_calls_per_fix": round(avg_tool_calls_per_fix, 2),
        "budget_status": _compute_budget_status(),
    }


@mcp.tool()
def reset_session_stats() -> dict[str, Any]:
    """Reset all session counters. Call at the start of every agent invocation.

    This clears all accumulated tool call counts, pytest runs, browser
    inspections, and fix tracking so the session budget starts fresh.

    If a prior session was active in this server process (e.g. a previous
    agent run that did not call reset), the returned dict includes a
    "previous_session" key summarising what is being discarded. Agents
    should log this field if present so cross-contamination is visible.

    Returns:
        dict with keys:
          - reset (bool): always True
          - session_start_time (float): epoch timestamp of the new session
          - previous_session (dict | None): summary of the discarded session,
            present only when the server state was non-empty before this reset
    """
    now = time.time()

    # Snapshot previous session before overwriting
    prev_calls = _session_state["total_tool_calls"]
    prev_start = _session_state["session_start_time"]
    previous_session = None
    if prev_calls > 0 and prev_start is not None:
        elapsed = (now - prev_start) / 60.0
        previous_session = {
            "total_tool_calls": prev_calls,
            "total_pytest_runs": _session_state["total_pytest_runs"],
            "total_fixes_attempted": _session_state["total_fixes_attempted"],
            "elapsed_minutes": round(elapsed, 2),
            "warning": "Server state was non-empty — possible cross-session contamination.",
        }

    _session_state.update(
        {
            "total_tool_calls": 1,  # count this reset call itself
            "total_pytest_runs": 0,
            "total_browser_inspections": 0,
            "total_fixes_attempted": 0,
            "total_fixes_succeeded": 0,
            "tests_remaining": 0,
            "session_start_time": now,
            "_pending_verification": False,
            "_call_history": {},
        }
    )
    result: dict[str, Any] = {"reset": True, "session_start_time": now}
    if previous_session:
        result["previous_session"] = previous_session
    return result


# ===========================================================================
# Entry point
# ===========================================================================

if __name__ == "__main__":
    mcp.run()
