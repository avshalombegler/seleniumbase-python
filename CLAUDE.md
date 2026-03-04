# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run tests (UI marker is the default in `pyproject.toml`):**

```bash
# Run all ui-marked tests
pytest

# Run a specific test file
pytest tests/the_internet/ui_test_suite/test_ab_testing.py

# Run a specific test by node ID
pytest tests/the_internet/ui_test_suite/test_ab_testing.py::TestABTesting::test_ab_testing_content

# Override marker (e.g. run all regression tests)
pytest -m regression

# Run in parallel
pytest -n auto

# Run with Allure reporting
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

**Lint and format (via taskipy):**

```bash
task check   # ruff check .
task fix     # ruff check . --fix && ruff format .
```

**Python environment:** Always use the conda env at `C:/Users/Avshalom/anaconda3/envs/seleniumbase-python/python.exe`. The project is installed with `python -m pip install -e .`.

**MCP server (for AI agents):**

```bash
C:/Users/Avshalom/anaconda3/envs/seleniumbase-python/python.exe tools/seleniumbase-mcp/server.py
```

## Architecture

### Three-Layer Page Object Model

Every feature follows this strict three-layer pattern:

| Layer | Path | Class |
| --- | --- | --- |
| Locators | `src/pages/features/<feature>/locators.py` | `XxxLocators` |
| Page Object | `src/pages/features/<feature>/<feature>_page.py` | `XxxPage(BasePage)` |
| Test | `tests/the_internet/ui_test_suite/test_<feature>.py` | `TestXxx(UiBaseCase)` |

**Navigation hub:** `MainPage` (`src/pages/common/main_page/`) acts as the single entry point for all feature pages. Every feature has a `click_<feature>_link()` method in `MainPage` that clicks the homepage link and returns the feature's page object. Tests always start with `main_page = MainPage(self)` then call the nav method.

### Locator Type

```python
Locator = dict[str, str]  # {"selector": "<value>", "by": By.<STRATEGY>}
```

Defined in `src/pages/base/base_page.py` (TYPE_CHECKING only). Used by unpacking: `driver.click(**locator)`. Locator strategy priority: `By.ID` → `By.CSS_SELECTOR` → `By.XPATH`. Never `By.CLASS_NAME` or `By.TAG_NAME` alone.

### Base Classes

- **`BasePage`** (`src/pages/base/base_page.py`): All page objects inherit this. Wraps SeleniumBase's `BaseCase` as `self.driver`. Key methods: `wait_for_page_to_load`, `wait_for_visibility`, `wait_for_invisibility`, `click_element`, `send_keys_to_element`, `is_element_visible`, `get_dynamic_element_text`, `format_locator`, `get_all_elements`.

- **`UiBaseCase`** (`src/pages/base/ui_base_case.py`): All test classes inherit this (which extends `BaseCase`). Its `setUp` automatically navigates to `settings.BASE_URL` when the test is marked `@pytest.mark.ui` — **do not add explicit navigation in test methods for ui-marked tests**. Attaches failure screenshots to Allure on teardown. Handles per-worker download directories for parallel runs.

### Configuration

`src/config/project_config.py` — pydantic-settings `Settings` class loaded from `.env`. Import as:

```python
from src.config import settings
```

Key fields: `BASE_URL`, `BROWSER`, `HEADLESS`, `SHORT_TIMEOUT`, `LONG_TIMEOUT`, `TEST_USERNAME`, `TEST_PASSWORD`.

### Test Markers

Defined in `pyproject.toml`. `--strict-markers` is enforced — only use registered markers:

- `@pytest.mark.ui` — triggers auto-navigation to `BASE_URL` in `setUp`
- `@pytest.mark.regression` — full regression suite
- `@pytest.mark.smoke` — critical path tests
- `@pytest.mark.api` — API tests
- `@pytest.mark.fix` — test needs human review (healer could not auto-resolve)

### Test Suites

- `tests/the_internet/ui_test_suite/` — UI tests against `https://the-internet.herokuapp.com`
- `tests/jsonplaceholder/` — API tests against the JSONPlaceholder API (has its own `conftest.py` and `models/`)
- `tests/demo/` — Demo/scratch tests

### Allure Reporting

Every test class uses three Allure decorators:

```python
@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("<Feature Name>")
```

Every page object method is decorated with `@allure.step(...)`.

## AI Agents

Three Claude agents are defined in `.claude/agents/` and invoked via `@<agent-name>`:

**`sb-planner`** — Inspects a live page with a headless browser and produces a structured
spec file that `sb-generator` can consume. Usage:

```text
@sb-planner plan the-internet/<feature>
```

Writes `specs/the_internet/spec_<feature_dir>.md`. Does not write test code.

**`sb-generator`** — Generates the full four-file set (locators, page object, test file, `__init__.py`) plus `MainPage` registration from a spec file. Usage:

```text
@sb-generator implement specs/the_internet/spec_<feature_dir>.md
```

Specs live in `specs/the_internet/` as Markdown files. The spec is the authoritative source — the generator never invents names or scenarios. Uses the MCP server tools and Context7 for SeleniumBase API verification.

**`sb-healer`** — Diagnoses and fixes failing tests. Runs failing tests, parses errors, applies fixes using `write_file`/`insert_into_file`, and marks unresolvable tests with `@pytest.mark.fix`.

**Shared standards:** All three agents reference `.claude/skills/sb-test-standards/SKILL.md` for the project's coding conventions. This file is the single source of truth for what correct locator, page object, and test file code looks like. When a convention changes (new base method, updated import pattern, etc.), update this file — the agents will reflect the change on their next invocation.

All agents use the MCP server (`tools/seleniumbase-mcp/server.py`) which exposes 19 tools for file I/O with syntax validation, pytest execution, test result parsing, and code scaffolding.

**Hook maintenance:** `.claude/settings.json` registers a `PostToolUse` ruff-formatting hook for every MCP write tool by exact name (`mcp__seleniumbase__write_file`, `create_test_file`, etc.). **When a new write tool is added to `server.py`, a corresponding matcher entry must be added to `.claude/settings.json`** and a new entry added to `.claude/hooks/ruff_fix_mcp_file.py`'s docstring. The hook script itself requires no changes — only the matcher registration.

## Adding a New Feature

1. Run `@sb-planner plan the-internet/<feature>` to generate `specs/the_internet/spec_<feature_dir>.md`.
2. Invoke `@sb-generator implement specs/the_internet/spec_<feature_dir>.md`.

Or manually:

1. Create `src/pages/features/<feature>/locators.py` — `XxxLocators` class with `Locator` attributes, `PAGE_LOADED_INDICATOR` first.
2. Create `src/pages/features/<feature>/<feature>_page.py` — `XxxPage(BasePage)`, `__init__` calls `super().__init__(driver)` then `wait_for_page_to_load(...)`, all methods decorated with `@allure.step`.
3. Create `src/pages/features/<feature>/__init__.py` (empty).
4. Add `FEATURE_LINK: Locator` to `MainPageLocators` in `src/pages/common/main_page/locators.py`.
5. Add import and `click_<feature>_link()` method to `src/pages/common/main_page/main_page.py`.
6. Create `tests/the_internet/ui_test_suite/test_<feature>.py` — `TestXxx(UiBaseCase)` with Allure class decorators.
