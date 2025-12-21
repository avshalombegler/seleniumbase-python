# SeleniumBase-Python Test Automation Suite

[![CI Status](https://github.com/avshalombegler/selenium-python/actions/workflows/ci.yml/badge.svg)](https://github.com/avshalombegler/selenium-python/actions/workflows/ci.yml)

A modern, maintainable test automation suite using **SeleniumBase** for <https://the-internet.herokuapp.com>.  
Built with **Page Object Model**, **pytest**, **Allure reporting**, **Docker Compose orchestration**, and **CI/CD** (GitHub Actions & Jenkins).

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables-env)
- [Running tests](#running-tests)
- [Docker Support](#docker-support)
- [Allure Reports](#allure-reports)
- [Project structure](#project-structure)

## Features

- Clean POM architecture
- Multi-browser support (Chrome & Firefox)
- Headless & headed mode
- Parallel test execution via `pytest-xdist`
- Allure reports generation with history & trends
- Automatic screenshot attachment to Allure Report for failed tests

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

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    python -m pip install -e .
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

Create a .env file in the project root:

```env
# Application
BASE_URL=https://the-internet.herokuapp.com/

# Browser Configuration
BROWSER=chrome             # Options: chrome, firefox
HEADLESS=True              # Run without UI (CI default)
MAXIMIZED=False            # Maximize browser window

# Timeouts (seconds)
SHORT_TIMEOUT=3            # For quick operations
LONG_TIMEOUT=10            # For slow operations

# Test Credentials (for demo site)
USERNAME=tomsmith
PASSWORD=SuperSecretPassword!
```

**⚠️ Note:** Never commit `.env` with real credentials. Use CI secrets for production.

## Running tests

### Locally

- Run all tests (sequential):

    ```bash
    pytest
    ```

- Run all tests in parallel:

    ```bash
    pytest -n auto
    ```

- Run a specific test file:

    ```bash
    pytest .\tests\test_test_name.py
    ```

- Generate Allure results (add this flag to the pytest run command):

    ```bash
    --alluredir=reports/allure-results
    ```

- View Allure Report Locally:

    ```bash
    allure serve reports/allure-results
    ```

- Optional: generate a static HTML report (requires Allure CLI):

    ```bash
    allure generate reports/allure-results -o reports/allure-report
    ```

### Running in GitHub Actions

- GitHub Actions automatically runs tests on every push or pull request to the main branch.
- For manual runs, go to the Actions tab, select the CI workflow, and click "Run workflow" (if configured with workflow_dispatch).

### Running in Jenkins

1. Create a new Pipeline job in Jenkins
2. Configure SCM to point to your repository
3. Set "Script Path" to `Jenkinsfile`
4. Configure build triggers (e.g., Poll SCM, GitHub webhook)
5. Run the pipeline

#### Pipeline Parameters

The Jenkinsfile supports the following parameters:

- `BROWSER`: Browser choice (both/chrome/firefox)
- `MARKER`: Test marker to run (regression/smoke/ui)
- `WORKERS`: Number of parallel workers (default: auto)

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

### 📊 GitHub Actions Allure Reports

Latest reports are published automatically to GitHub Pages:

|  | Latest Run | With History |
|-----------|-----------|-----------|
| **Chrome** | [View Report](https://avshalombegler.github.io/seleniumbase-python/chrome/latest-only/build-chrome-20407234199/) | [View Report](https://avshalombegler.github.io/seleniumbase-python/chrome/latest-with-history/build-chrome-20407234199/) |
| **Firefox** | [View Report](https://avshalombegler.github.io/seleniumbase-python/firefox/latest-only/build-firefox-20407234199/) | [View Report](https://avshalombegler.github.io/seleniumbase-python/firefox/latest-with-history/build-firefox-20407234199/) |

### 📊 Jenkins Allure Reports

Reports generated from Jenkins pipeline runs are hosted locally and can be accessed publicly via ngrok tunneling. These reports are populated through the Allure server backend, served via the Allure UI, and exposed externally using ngrok for secure remote access.

**Local Access:** [View Report](http://localhost:8080) (via Nginx reverse proxy to Allure UI)

**Public Access:** [View Report](https://url-place-holder.ngrok-free.dev) (dynamic tunnel URL provided by ngrok)

> Reports update automatically after each CI run.

## Project structure

```text
seleniumbase-python/
├── .github/
│    └── workflows/ci.yml                           # GitHub Actions workflow
├── reports/                                        # Allure results and artifacts
├── src/                                            # 
│   ├── config/ 
│   │    └── logging_config.py                      # 
│   │    └── nginx.conf                             # Nginx configuration for reverse proxy
│   │    └── project_config.py                      # 
│   └── pages/                                      # Page Object Model classes
│        ├── base/                                  # BasePage, UiBaseCase
│        ├── common/                                # MainPage
│        └── features/                              # Page objects per feature
├── tests/                                          # Test cases
├── .env                                            # Environment variables (gitignored)
├── conftest.py                                     # Main conftest - registers plugins
├── docker-compose.yml                              # Docker Compose configuration for CI/CD environment
├── Dockerfile.jenkins                              # Custom Jenkins agent Docker image
├── environment.yml                                 # 
├── Jenkinsfile                                     # Jenkins pipeline definition
├── pyproject.toml                                  # Project configuration
├── requirements.txt    
├── start-ngrok.ps1                                 # PowerShell script to start ngrok tunnel
└── README.md
```

## How to Add New Tests

1. Create page object in `src/pages/features/your_feature/your_page.py`
2. Add test in `tests/x_test_suite/test_your_feature.py`
3. (Optional) Add `@pytest.mark.regression` or other markers

## Contributing

We welcome contributions! Please follow these steps:

- Fork the repository and create a feature branch.
- Write tests for new features and ensure all tests pass.
- Follow PEP 8 style guidelines.
- Submit a pull request with a clear description.

For issues or questions, open a GitHub issue.
