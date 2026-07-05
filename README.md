# SeleniumBase-Python Test Automation Suite

[![CI Status](https://github.com/avshalombegler/selenium-python/actions/workflows/ci.yml/badge.svg)](https://github.com/avshalombegler/selenium-python/actions/workflows/ci.yml)

A modern, maintainable test automation suite covering two targets: **UI tests** against <https://the-internet.herokuapp.com> (driven by **SeleniumBase**) and **API tests** against the **JSONPlaceholder** REST API (<https://jsonplaceholder.typicode.com>).
Built with a **three-layer Page Object Model**, **AI-powered test generation and healing**, **pytest**, **Allure reporting**, **Docker Compose orchestration**, and **CI/CD** (GitHub Actions & Jenkins).

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables-env)
- [Running Tests](#running-tests)
- [Architecture](#architecture)
- [AI-Powered Testing](#ai-powered-testing)
- [Test Suites](#test-suites)
- [Lint and Format](#lint-and-format)
- [Docker Support](#docker-support)
- [Allure Reports](#allure-reports)
- [CI/CD](#cicd)
- [Project Structure](#project-structure)
- [Adding a New Feature](#adding-a-new-feature)

## Features

- **Three-layer Page Object Model** – Locators, Page Objects, and Tests are strictly separated
- **AI-powered agents** – `sb-planner`, `sb-generator`, and `sb-healer` automate test creation and repair
- **MCP server** – 19 tools across 5 groups expose file I/O, pytest execution, and scaffolding to AI agents
- **Two test suites** – UI tests (40+ features on the-internet) and API tests (JSONPlaceholder, 6 resources)
- **Structured JSON logging** – per-test context with per-worker log files for safe parallel runs
- Multi-browser support (Chrome & Firefox)
- Headless & headed mode
- Parallel test execution via `pytest-xdist`
- Allure reports with history & trends
- Automatic screenshot attachment to Allure for failed tests

### CI/CD Features

#### GitHub Actions

- Runs automatically on every push/PR to main
- Automatic artifact archiving
- Allure reports automatically published to GitHub Pages

#### Jenkins

- Full Jenkins CI/CD environment via Docker Compose (Jenkins, Allure server, UI, and Nginx)
- Parameterized builds for flexible test configuration
- Scheduled job runs every day at night
- Allure report generation and storage on Allure server

## Requirements

### System Requirements

- **Python:** 3.10 or higher
- **Conda:** Anaconda or Miniconda (recommended – the project uses a conda environment)
- **Node.js:** Latest LTS (required for AI agent MCP servers – Playwright MCP and Context7)
- **Git:** Latest version
- **Browsers:**
  - Chrome 120+ / ChromeDriver (auto-managed)
  - Firefox 121+ / GeckoDriver (auto-managed)
- **Docker:** Latest version (for containerized CI/CD)
- **Docker Compose:** Latest version (for orchestrating the full environment)

### Python Dependencies

Key packages (see `pyproject.toml` for full list):

- `seleniumbase==4.44.20`
- `pytest==8.4.2`
- `allure-pytest==2.15.0`
- `pytest-xdist==3.8.0`
- `pytest-json-report==1.5.0`
- `python-dotenv==1.1.1`
- `pytest-sugar==1.1.1`
- `pytest-rerunfailures==16.1`

### Jenkins CI/CD Prerequisites

- Jenkins 2.400+ with Docker support
- Docker installed on Jenkins agent
- Required Jenkins plugins:
  - Docker Pipeline
  - Allure Plugin
  - HTML Publisher Plugin

## Installation

### Local Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/avshalombegler/seleniumbase-python.git
    cd seleniumbase-python
    ```

2. Create and activate the conda environment:

    ```bash
    conda create -n seleniumbase-python python=3.10
    conda activate seleniumbase-python
    ```

3. Install the project and its dependencies:

    ```bash
    python -m pip install -e .
    ```

4. Install `pytest-json-report` (required by the MCP server):

    ```bash
    pip install pytest-json-report
    ```

**Note:** Allure CLI requires separate installation (not available via pip).
See installation guide: <https://docs.qameta.io/allure/#_installing_a_commandline>

### Docker Installation

For a containerized setup, use Docker Compose to run the full CI/CD environment:

1. Ensure Docker and Docker Compose are installed.

2. Clone the repository and navigate to the project directory.

3. Start the services:

    ```bash
    docker-compose up -d
    ```

4. Access Jenkins at `http://localhost:8080` (via Nginx proxy).

5. For external access to Allure reports, run the ngrok script:

    ```powershell
    .\start-ngrok.ps1
    ```

## Environment Variables (.env)

Create a `.env` file in the project root:

```env
# Application
BASE_URL=https://the-internet.herokuapp.com/

# Browser Configuration
BROWSER=chrome             # Options: chrome, firefox
HEADLESS=True              # Run without UI (CI default)
MAXIMIZED=False            # Maximize browser window

# Timeouts (seconds)
SHORT_TIMEOUT=5            # For quick operations
LONG_TIMEOUT=15            # For slow operations
REQUEST_TIMEOUT=5          # For HTTP requests (API tests)

# Test Credentials (for demo site)
TEST_USERNAME=tomsmith
TEST_PASSWORD=SuperSecretPassword!
```

**Note:** Never commit `.env` with real credentials. Use CI secrets for production.

## Running Tests

### Test Markers

The project uses strict markers – only registered markers are valid:

| Marker | Purpose |
| --- | --- |
| `@pytest.mark.ui` | UI tests – auto-navigates to `BASE_URL` in setUp |
| `@pytest.mark.regression` | Full regression suite |
| `@pytest.mark.smoke` | Critical path tests |
| `@pytest.mark.api` | API tests |
| `@pytest.mark.fix` | Test needs human review (healer could not auto-resolve) |

### Locally

Run all UI-marked tests:

```bash
pytest -m ui
```

Run all API tests:

```bash
pytest -m api
```

Run a specific test file:

```bash
pytest tests/the_internet/ui_test_suite/test_ab_testing.py
```

Run a specific test by node ID:

```bash
pytest tests/the_internet/ui_test_suite/test_ab_testing.py::TestABTesting::test_ab_testing_content
```

Run all tests in parallel:

```bash
pytest -m ui -n auto
```

Generate Allure results (add to any pytest command):

```bash
pytest -m ui --alluredir=reports/allure-results
```

View Allure report locally:

```bash
allure serve reports/allure-results
```

Optional – generate a static HTML report:

```bash
allure generate reports/allure-results -o reports/allure-report
```

### Running in GitHub Actions

GitHub Actions automatically runs tests on every push or pull request to the main branch.
For manual runs, go to the Actions tab, select the CI workflow, and click "Run workflow".

- **Browser**: Choose browser (`both`, `chrome`, `firefox`) – default: `both`
- **Marker**: Select test marker (`smoke`, `regression`, `ui`, `api`) – default: `smoke`
- **Workers**: Number of parallel workers (e.g., `auto`, `2`, `4`) – default: `auto`
- **Clean History**: Clean all history and start fresh (boolean) – default: `false`

### Running in Jenkins

1. Create a new Pipeline job in Jenkins
2. Configure SCM to point to your repository
3. Set "Script Path" to `Jenkinsfile`
4. Configure build triggers (e.g., Poll SCM, GitHub webhook)
5. Run the pipeline

#### Pipeline Parameters

- `BROWSER`: Browser choice (`both` / `chrome` / `firefox`)
- `MARKER`: Test marker to run (`regression` / `smoke` / `ui`)
- `WORKERS`: Number of parallel workers (default: `auto`)

## Architecture

### Three-Layer Page Object Model

Every feature follows a strict three-layer pattern:

| Layer | Path | Class |
| --- | --- | --- |
| Locators | `src/pages/features/<feature>/locators.py` | `XxxLocators` |
| Page Object | `src/pages/features/<feature>/<feature>_page.py` | `XxxPage(BasePage)` |
| Test | `tests/the_internet/ui_test_suite/test_<feature>.py` | `TestXxx(UiBaseCase)` |

### Locator Type

```python
Locator = dict[str, str]  # {"selector": "<value>", "by": By.<STRATEGY>}
```

Locators are used by unpacking: `driver.click(**locator)`.
Strategy priority: `By.ID` → `By.CSS_SELECTOR` → `By.XPATH`. Never `By.CLASS_NAME` or `By.TAG_NAME` alone.

### Base Classes

- **`BasePage`** (`src/pages/base/base_page.py`): All page objects inherit this. Wraps SeleniumBase's `BaseCase` as `self.driver`. Provides methods for waiting, clicking, typing, file downloads, element state queries, and navigation.

- **`UiBaseCase`** (`src/pages/base/ui_base_case.py`): All test classes inherit this (extends `BaseCase`). Its `setUp` auto-navigates to `settings.BASE_URL` when the test is marked `@pytest.mark.ui` – no explicit navigation needed in test methods. Handles per-worker download directories for parallel runs and attaches failure screenshots to Allure on teardown.

### Navigation Hub

`MainPage` (`src/pages/common/main_page/`) is the single entry point for all feature pages. Tests always start with `main_page = MainPage(self)` then call the appropriate nav method (e.g., `main_page.click_form_authentication_link()`).

## AI-Powered Testing

Three Claude agents automate the full test authoring and maintenance lifecycle:

### `sb-planner` – Test Design Agent

Inspects a live page with a headless browser and produces a structured spec file.

```text
@sb-planner plan the-internet/<feature>
```

Output: `specs/the_internet/spec_<feature_dir>.md`

### `sb-generator` – Code Generation Agent

Generates the full three-file set (locators, page object, test) plus `MainPage` registration from a spec file.

```text
@sb-generator implement specs/the_internet/spec_<feature_dir>.md
```

The spec is the authoritative source – the generator never invents names or scenarios. Verifies SeleniumBase API via Context7 docs before writing code.

### `sb-healer` – Test Repair Agent

Diagnoses and fixes failing tests. Runs failing tests, parses errors, applies fixes, and marks unresolvable cases with `@pytest.mark.fix`.

```text
@sb-healer fix failing tests in tests/the_internet/ui_test_suite/
```

Repair scope: locator fixes, assertion fixes, timing fixes, code/import errors, incomplete page object completion.

### MCP Servers

Five MCP servers are pre-configured in `.claude/settings.json`:

| Server | Command | Used by |
| --- | --- | --- |
| `seleniumbase` | `python tools/seleniumbase-mcp/server.py` | All agents |
| `playwright` | `npx playwright run-mcp-server` | `sb-planner`, `sb-healer` |
| `context7` | `npx @upstash/context7-mcp` | `sb-generator`, `sb-healer` |
| `fetch` | `npx @modelcontextprotocol/server-fetch` | Main session, `sb-planner` |
| `sequential-thinking` | `npx @modelcontextprotocol/server-sequential-thinking` | Main session, `sb-planner` |

`playwright` provides live browser inspection for page analysis and failure diagnosis. `context7` provides up-to-date SeleniumBase API docs. `fetch` enables direct HTTP requests (useful for API test planning). `sequential-thinking` provides structured multi-step reasoning chains. All four external servers require Node.js.

The custom `seleniumbase` server exposes **19 tools** across 5 groups:

| Group | Tools |
| --- | --- |
| Execution | `run_pytest`, `get_test_results` |
| File I/O | `read_file`, `write_file`, `backup_file`, `cleanup_backups`, `validate_python`, `insert_into_file`, `list_files`, `get_project_structure` |
| Analysis | `get_page_source`, `analyze_page_elements`, `parse_pytest_failure` |
| Scaffold | `create_test_file`, `create_page_object_file`, `create_locators_file`, `get_code_template` |
| Budget | `get_session_stats`, `reset_session_stats` |

`write_file` validates Python syntax before writing – it will refuse to write syntactically invalid code.

## Test Suites

### UI Test Suite – `tests/the_internet/ui_test_suite/`

40+ feature tests against <https://the-internet.herokuapp.com>, covering:

A/B Testing, Add/Remove Elements, Basic Auth, Broken Images, Challenging DOM, Checkboxes, Context Menu, Digest Auth, Drag and Drop, Dropdown List, Dynamic Content, Dynamic Controls, Dynamic Loading, Entry Ad, Exit Intent, File Download, File Upload, Floating Menu, Form Authentication, Frames, Geolocation, Horizontal Slider, Hovers, Infinite Scroll, Inputs, JavaScript Alerts, JavaScript Onload Event Error, JQuery UI Menus, Key Presses, and more.

### API Test Suite – `tests/jsonplaceholder/api_test_suite/`

Full CRUD + model validation + negative tests against the [JSONPlaceholder API](https://jsonplaceholder.typicode.com), covering 6 resources:

`albums`, `comments`, `photos`, `posts`, `todos`, `users`

Each resource has typed Pydantic models in `tests/jsonplaceholder/models/` and shared helpers in `tests/jsonplaceholder/helpers.py`.

## Lint and Format

```bash
task check   # ruff check . (lint only)
task fix     # ruff check . --fix && ruff format . (fix + format)
```

Line length: 120 characters (configured in `pyproject.toml`).

## Docker Support

### Dockerfile.jenkins

The project includes a custom Jenkins agent image with all dependencies:

- Python 3.10
- Chrome & ChromeDriver
- Firefox & GeckoDriver
- Allure CLI
- All Python dependencies

### docker-compose.yml

The project utilizes Docker Compose to orchestrate a complete CI/CD environment, including:

- **Jenkins**: Automated build and test execution server
- **Allure Server**: Backend service for storing and managing Allure test reports
- **Allure UI**: Web interface for viewing and analyzing Allure reports
- **Nginx**: Reverse proxy for routing requests to Allure services

### Ngrok Integration

Ngrok is used to create secure tunnels for external access to Allure reports, enabling remote viewing of test results without exposing internal services directly.

## Allure Reports

### GitHub Actions Allure Reports

Latest reports are published automatically to GitHub Pages:

📊 **GitHub Pages Allure Report** [View Report](https://avshalombegler.github.io/seleniumbase-python/)

### Jenkins Allure Reports

Reports are generated by the Jenkins pipeline, stored in the Allure server, and served via the Allure UI behind an Nginx reverse proxy. A static ngrok tunnel exposes them publicly.

📊 **Local Access:** [View Report](http://localhost:8080) (via Nginx reverse proxy to Allure UI)

📊 **Public Access:** [View Live Report](https://unpleated-braxton-nondynastical.ngrok-free.dev) *(live demo – kept running for review)*

> **Note:** ngrok will display a warning page on first visit – click "Visit Site" to proceed to the dashboard.
> Reports update automatically after each CI run.

## CI/CD

See [Running in GitHub Actions](#running-in-github-actions) and [Running in Jenkins](#running-in-jenkins) above.

## Project Structure

```text
seleniumbase-python/
├── .claude/
│   ├── agents/
│   │   ├── sb-generator.agent.md
│   │   ├── sb-healer.agent.md
│   │   └── sb-planner.agent.md
│   ├── hooks/
│   └── skills/
│       └── sb-test-standards/SKILL.md
├── .github/
│   └── workflows/ci.yml
├── reports/
├── specs/
│   └── the_internet/
├── src/
│   ├── config/
│   │   ├── logging_config.py
│   │   └── project_config.py
│   └── pages/
│       ├── base/
│       │   ├── base_page.py
│       │   └── ui_base_case.py
│       ├── common/
│       │   └── main_page/
│       └── features/          # 40+ feature page objects
├── tests/
│   ├── demo/
│   ├── jsonplaceholder/
│   │   ├── api_test_suite/    # albums, comments, photos, posts, todos, users
│   │   ├── models/
│   │   ├── conftest.py
│   │   └── helpers.py
│   └── the_internet/
│       └── ui_test_suite/     # 40+ UI test files
├── tools/
│   └── seleniumbase-mcp/
│       └── server.py          # MCP server (19 tools)
├── conftest.py
├── docker-compose.yml
├── Dockerfile.jenkins
├── Jenkinsfile
├── pyproject.toml
├── start-ngrok.ps1
└── README.md
```

## Adding a New Feature

### With AI Agents (recommended)

```bash
# Step 1 – Inspect the live page and generate a spec
@sb-planner plan the-internet/<feature>

# Step 2 – Generate locators, page object, test, and MainPage registration
@sb-generator implement specs/the_internet/spec_<feature_dir>.md
```

### Manually

1. Create `src/pages/features/<feature>/locators.py` – `XxxLocators` class with `Locator` attributes, `PAGE_LOADED_INDICATOR` first.
2. Create `src/pages/features/<feature>/<feature>_page.py` – `XxxPage(BasePage)`, `__init__` calls `super().__init__(driver)` then `wait_for_page_to_load(...)`, all methods decorated with `@allure.step`.
3. Add `FEATURE_LINK: Locator` to `MainPageLocators` in `src/pages/common/main_page/locators.py`.
4. Add import and `click_<feature>_link()` method to `src/pages/common/main_page/main_page.py`.
5. Create `tests/the_internet/ui_test_suite/test_<feature>.py` – `TestXxx(UiBaseCase)` with Allure class decorators.
