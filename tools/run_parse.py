import json
import re


def parse_pytest_failure(longrepr: str) -> dict:
    result = {
        "file": None,
        "line": None,
        "error_type": None,
        "failed_selector": None,
        "assertion_message": None,
    }

    file_line_match = re.search(r"([\w/\\.\-]+\.py)[:\s]+(\d+)", longrepr)
    if file_line_match:
        result["file"] = file_line_match.group(1).replace("\\", "/")
        result["line"] = int(file_line_match.group(2))

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

    selector_match = re.search(
        r'["\']([#.\[\]:\w\s\-=\'"^$*]+)["\'].*(?:not found|not visible|timed out|Unable to locate)',
        longrepr,
        re.IGNORECASE,
    )
    if selector_match:
        result["failed_selector"] = selector_match.group(1)
    else:
        sel_kw_match = re.search(r'selector[=:\s]+["\']?([^"\'\s,\)]+)', longrepr, re.IGNORECASE)
        if sel_kw_match:
            result["failed_selector"] = sel_kw_match.group(1)

    assert_match = re.search(r"AssertionError:\s*(.+)", longrepr)
    if assert_match:
        result["assertion_message"] = assert_match.group(1).strip()

    return result


with open(".pytest_mcp_report.json", encoding="utf-8") as f:
    data = json.load(f)

summary = data.get("summary", {})
print("=" * 60)
print("RUN_PYTEST RESULTS")
print("=" * 60)
print("exit_code : 1  (non-zero, tests failed)")
print(f"passed    : {summary.get('passed', 0)}")
print(f"failed    : {summary.get('failed', 0)}")
print(f"errors    : {summary.get('error', 0)}")
print(f"duration  : {data.get('duration', 0.0):.2f}s")
print()

failures = []
for test in data.get("tests", []):
    if test.get("outcome") in ("failed", "error"):
        call = test.get("call", {})
        longrepr = call.get("longrepr", "") or test.get("longrepr", "")
        crash = call.get("crash", {})
        message = crash.get("message", "") if crash else longrepr[:200]
        parsed = parse_pytest_failure(longrepr)
        failures.append(
            {
                "nodeid": test.get("nodeid", ""),
                "message": message,
                "longrepr": longrepr,
                "parsed": parsed,
            }
        )

for i, f in enumerate(failures, 1):
    p = f["parsed"]
    print(f"{'=' * 60}")
    print(f"FAILURE {i}")
    print(f"{'=' * 60}")
    print(f"nodeid            : {f['nodeid']}")
    print()
    print("longrepr summary  :")
    print(f["longrepr"][:400])
    print()
    print("parse_pytest_failure output:")
    print(f"  file             : {p['file']}")
    print(f"  line             : {p['line']}")
    print(f"  error_type       : {p['error_type']}")
    print(f"  failed_selector  : {p['failed_selector']}")
    print(f"  assertion_message: {p['assertion_message']}")
    print()
