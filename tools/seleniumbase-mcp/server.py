"""
SeleniumBase MCP Server

Provides tools for test execution, file I/O, HTML analysis, and code scaffolding
for the seleniumbase-python project. Used by sb-healer, sb-generator, and sb-planner
Claude Code agents.
"""

from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import sys
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
# MCP server instance
# ---------------------------------------------------------------------------

mcp = FastMCP("seleniumbase")

# ===========================================================================
# Group 1: Execution Tools
# ===========================================================================


@mcp.tool()
def run_pytest(
    test_path: str,
    markers: str | None = None,
    browser: str = "chrome",
    headless: bool = True,
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

    Returns:
        dict with keys: exit_code, passed, failed, errors, duration, failures.
        Each item in failures has: nodeid, message, longrepr.
    """
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
            timeout=120,
            cwd=str(REPO_ROOT),
        )
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "duration": 0.0,
            "failures": [{"nodeid": test_path, "message": "Timeout after 120s", "longrepr": ""}],
        }

    # Parse report if it exists
    return _parse_report(result.returncode)


@mcp.tool()
def get_test_results() -> dict[str, Any]:
    """Read and return the structured results from the last run_pytest call.

    Returns the same schema as run_pytest: exit_code, passed, failed, errors,
    duration, failures (each with nodeid, message, longrepr).
    Returns {"error": "No report found"} if no report exists yet.
    """
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
# Group 2: File Tools
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
    abs_path = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)
    if not abs_path.exists():
        raise FileNotFoundError(f"File not found: {abs_path}")
    return abs_path.read_text(encoding="utf-8")


@mcp.tool()
def write_file(path: str, content: str) -> dict[str, Any]:
    """Write content to a file, creating parent directories if needed.

    Args:
        path: Destination path relative to repo root.
        content: Text content to write.

    Returns:
        dict with keys: success (bool), path (str), bytes_written (int).
    """
    abs_path = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    encoded = content.encode("utf-8")
    abs_path.write_bytes(encoded)
    return {"success": True, "path": str(abs_path.relative_to(REPO_ROOT)), "bytes_written": len(encoded)}


@mcp.tool()
def list_files(directory: str = ".", pattern: str = "*.py") -> list[str]:
    """List all files under a directory matching a glob pattern.

    Args:
        directory: Directory path relative to repo root (default '.').
        pattern: Glob pattern to match filenames (e.g. 'test_*.py', '*.py').

    Returns:
        List of relative paths (from repo root) matching the pattern.
    """
    abs_dir = REPO_ROOT / directory if not Path(directory).is_absolute() else Path(directory)
    if not abs_dir.exists():
        return []

    results = []
    for p in abs_dir.rglob("*"):
        if p.is_file() and fnmatch.fnmatch(p.name, pattern):
            results.append(str(p.relative_to(REPO_ROOT)).replace("\\", "/"))
    return sorted(results)


# ===========================================================================
# Group 3: Analysis Tools
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
    result: dict[str, Any] = {
        "file": None,
        "line": None,
        "error_type": None,
        "failed_selector": None,
        "assertion_message": None,
        "raw": longrepr,
    }

    # Extract file and line: patterns like "src/pages/foo.py:42:" or "FAILED tests/...::test - "
    file_line_match = re.search(r'([\w/\\.\-]+\.py)[:\s]+(\d+)', longrepr)
    if file_line_match:
        result["file"] = file_line_match.group(1).replace("\\", "/")
        result["line"] = int(file_line_match.group(2))

    # Extract error type from the last Exception line
    error_type_match = re.search(
        r'(NoSuchElementException|ElementNotVisibleException|TimeoutException|'
        r'AssertionError|StaleElementReferenceException|WebDriverException|'
        r'ElementClickInterceptedException|NoSuchWindowException|'
        r'InvalidSelectorException|MoveTargetOutOfBoundsException|'
        r'[\w]+Error|[\w]+Exception)',
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
    assert_match = re.search(r'AssertionError:\s*(.+)', longrepr)
    if assert_match:
        result["assertion_message"] = assert_match.group(1).strip()

    return result


# ===========================================================================
# Group 4: Scaffold Tools
# ===========================================================================


@mcp.tool()
def create_test_file(path: str, content: str) -> dict[str, Any]:
    """Create a new test file in the tests/ directory.

    Validates that the path starts with 'tests/' and ends with '.py'.
    Creates parent directories as needed.

    Args:
        path: Destination path relative to repo root (must start with 'tests/' and end with '.py').
        content: Full Python source code for the test file.

    Returns:
        dict with keys: success (bool), path (str).

    Raises:
        ValueError: If path does not start with 'tests/' or does not end with '.py'.
    """
    norm = path.replace("\\", "/")
    if not norm.startswith("tests/"):
        raise ValueError(f"Test file path must start with 'tests/', got: {path}")
    if not norm.endswith(".py"):
        raise ValueError(f"Test file path must end with '.py', got: {path}")

    abs_path = REPO_ROOT / path
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(content, encoding="utf-8")
    return {"success": True, "path": norm}


@mcp.tool()
def create_page_object_file(path: str, content: str) -> dict[str, Any]:
    """Create a new page object file in the src/pages/ directory.

    Validates that the path starts with 'src/pages/' and ends with '.py'.
    Creates parent directories as needed.

    Args:
        path: Destination path relative to repo root (must start with 'src/pages/' and end with '.py').
        content: Full Python source code for the page object.

    Returns:
        dict with keys: success (bool), path (str).

    Raises:
        ValueError: If path validation fails.
    """
    norm = path.replace("\\", "/")
    if not norm.startswith("src/pages/"):
        raise ValueError(f"Page object path must start with 'src/pages/', got: {path}")
    if not norm.endswith(".py"):
        raise ValueError(f"Page object path must end with '.py', got: {path}")

    abs_path = REPO_ROOT / path
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(content, encoding="utf-8")
    return {"success": True, "path": norm}


@mcp.tool()
def create_locators_file(path: str, content: str) -> dict[str, Any]:
    """Create a new locators file in the src/pages/ directory.

    Validates that the path starts with 'src/pages/' and ends with 'locators.py'.
    Creates parent directories as needed.

    Args:
        path: Destination path relative to repo root
              (must start with 'src/pages/' and end with 'locators.py').
        content: Full Python source code for the locators file.

    Returns:
        dict with keys: success (bool), path (str).

    Raises:
        ValueError: If path validation fails.
    """
    norm = path.replace("\\", "/")
    if not norm.startswith("src/pages/"):
        raise ValueError(f"Locators file path must start with 'src/pages/', got: {path}")
    if not norm.endswith("locators.py"):
        raise ValueError(f"Locators file path must end with 'locators.py', got: {path}")

    abs_path = REPO_ROOT / path
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(content, encoding="utf-8")
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
    # Derive naming variants
    # Convert to snake_case for method/file names
    # e.g. "CheckboxPage" -> "checkbox_page", "dropdown_list" -> "dropdown_list"
    snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower().strip('_')
    snake = re.sub(r'[^a-z0-9_]', '_', snake).strip('_')

    # PascalCase class name
    pascal = ''.join(word.capitalize() for word in re.split(r'[_\s]+', name))

    # Human-readable feature name
    feature_name = ' '.join(word.capitalize() for word in re.split(r'[_\s]+', name))

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
# Entry point
# ===========================================================================

if __name__ == "__main__":
    mcp.run()
