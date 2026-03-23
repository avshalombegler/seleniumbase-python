"""Pytest configuration and shared fixtures for Selenium-based UI tests.

Sets up logging, cleans result/download directories, and defines pytest hooks and fixtures.
"""

import logging
import os
import shutil
from pathlib import Path

import pytest
import structlog
from filelock import FileLock
from seleniumbase.fixtures import constants

from src.config import settings

logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)
logging.getLogger("undetected_chromedriver").setLevel(logging.WARNING)


# ---------------------------------------------------------------------------
# Pytest hooks
# ---------------------------------------------------------------------------


def _setup_logging(config: pytest.Config) -> None:
    show_logs = os.environ.get("SHOW_LOGS", "false").lower() == "true"
    os.environ["SHOW_LOGS"] = "true" if show_logs else "false"

    # Deferred import: depends on SHOW_LOGS env var being set above
    from src.config.logging_config import configure_logging

    configure_logging()

    if show_logs:
        config.option.capture = "no"


def _configure_browser(config: pytest.Config) -> None:
    is_ci_environment = os.environ.get("JENKINS_HOME") or os.environ.get("GITHUB_ACTIONS")
    is_xdist_worker = os.environ.get("PYTEST_XDIST_WORKER")
    browser = os.environ.get("BROWSER", settings.BROWSER).lower()

    # Store for use in fixtures and downstream helpers
    config.browser = browser  # type: ignore[attr-defined]
    config.option.browser = browser
    config.option.headless = settings.HEADLESS

    if browser == "chrome" and not is_ci_environment:
        # Use per-worker subdirectory when running in parallel to avoid Chrome profile lock conflicts
        if is_xdist_worker:
            user_data_dir = os.path.abspath(os.path.join("chrome_user_data", is_xdist_worker))
        else:
            user_data_dir = os.path.abspath("chrome_user_data")
        os.makedirs(user_data_dir, exist_ok=True)

        if not hasattr(config.option, "chromium_arg") or not config.option.chromium_arg:
            config.option.chromium_arg = []

        config.option.chromium_arg.extend(
            [
                f"--user-data-dir={user_data_dir}",
                "--profile-directory=Default",
            ]
        )


def _setup_allure_directory(config: pytest.Config) -> None:
    is_ci_environment = os.environ.get("JENKINS_HOME") or os.environ.get("GITHUB_ACTIONS")
    is_xdist_worker = os.environ.get("PYTEST_XDIST_WORKER")

    allure_results_dir = getattr(config.option, "allure_report_dir", None)
    if not allure_results_dir:
        allure_results_dir = str(Path("reports") / "allure-results")
        config.option.allure_report_dir = allure_results_dir

    allure_results_path = Path(allure_results_dir)

    # Clean allure results ONLY for non-xdist runs and local development
    # Don't clean in CI environments (Jenkins or GitHub Actions) where browsers run in parallel
    if not is_xdist_worker and not is_ci_environment:
        if allure_results_path.exists():
            logging.info(f"Cleaning Allure results directory: {allure_results_path}")
            shutil.rmtree(allure_results_path, ignore_errors=True)
        allure_results_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created fresh Allure results directory: {allure_results_path}")
    else:
        allure_results_path.mkdir(parents=True, exist_ok=True)
        if is_ci_environment:
            logging.info(f"Running in CI environment - preserving existing results in: {allure_results_path}")

    # Store resolved path for _write_allure_env_properties
    config.allure_results_path = allure_results_path  # type: ignore[attr-defined]


def _write_allure_env_properties(config: pytest.Config) -> None:
    is_xdist_worker = os.environ.get("PYTEST_XDIST_WORKER")
    if is_xdist_worker:
        return

    allure_results_path: Path = config.allure_results_path  # type: ignore[attr-defined]
    browser: str = config.browser  # type: ignore[attr-defined]

    env_properties_path = allure_results_path / "environment.properties"
    with open(env_properties_path, "w") as f:
        f.write(f"Browser={browser.capitalize()}\n")
        f.write(f"Headless={settings.HEADLESS}\n")
        f.write(f"Base_URL={settings.BASE_URL}\n")
        if os.environ.get("GITHUB_ACTIONS"):
            f.write(f"GitHub_Actions_Workflow={os.environ.get('GITHUB_WORKFLOW', 'N/A')}\n")
            f.write(f"GitHub_Actions_Run_ID={os.environ.get('GITHUB_RUN_ID', 'N/A')}\n")
        elif os.environ.get("JENKINS_HOME"):
            f.write(f"Jenkins_Job_Name={os.environ.get('JOB_NAME', 'N/A')}\n")
            f.write(f"Jenkins_Build_Number={os.environ.get('BUILD_NUMBER', 'N/A')}\n")


def _setup_logs_directory() -> None:
    is_ci_environment = os.environ.get("JENKINS_HOME") or os.environ.get("GITHUB_ACTIONS")
    is_xdist_worker = os.environ.get("PYTEST_XDIST_WORKER")

    logs_path = Path("logs")

    if not is_xdist_worker and not is_ci_environment:
        if logs_path.exists():
            logging.info(f"Cleaning logs directory: {logs_path}")
            shutil.rmtree(logs_path, ignore_errors=True)
        logs_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created fresh logs directory: {logs_path}")
    else:
        logs_path.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """
    Configure pytest settings for browser testing with Allure reporting.
    Sets up logging, browser options, Allure results directory, and environment metadata.
    """
    _setup_logs_directory()
    _setup_logging(config)
    _configure_browser(config)
    _setup_allure_directory(config)
    _write_allure_env_properties(config)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def clean_directory(dir_path: Path, lock_suffix: str = "lock") -> None:
    """Helper to clean and recreate a directory with file locking."""
    lock_file = dir_path.parent / f"{lock_suffix}.lock"
    dir_path.mkdir(parents=True, exist_ok=True)

    # Add timeout to prevent deadlocks
    with FileLock(lock_file, timeout=30):
        if dir_path.exists():
            shutil.rmtree(dir_path, ignore_errors=True)
        dir_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory cleaned and recreated at: {dir_path}.")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def clean_directories_at_start() -> None:
    """Clean downloads directory at session start."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER") or "local"

    downloads_dir = Path(constants.Files.DOWNLOADS_FOLDER) / worker_id
    clean_directory(downloads_dir, worker_id)



@pytest.fixture(autouse=True)
def bind_test_context(request: pytest.FixtureRequest) -> None:
    """Bind per-test context for structured JSON logging (test_name, browser)."""
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(test_name=request.node.name, browser=settings.BROWSER)
