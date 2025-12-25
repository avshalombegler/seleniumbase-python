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
from src.config.logging_config import configure_logging

# Configure root logging once for the test session
configure_logging()
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)
logging.getLogger("undetected_chromedriver").setLevel(logging.WARNING)


def clean_directory(dir_path: Path, lock_suffix: str = "lock") -> None:
    """Helper to clean and recreate a directory with file locking."""
    lock_file = dir_path / f"{lock_suffix}.lock"
    dir_path.mkdir(parents=True, exist_ok=True)

    # Add timeout to prevent deadlocks
    with FileLock(lock_file, timeout=30):
        if dir_path.exists():
            shutil.rmtree(dir_path, ignore_errors=True)
        dir_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory cleaned and recreated at: {dir_path}.")


@pytest.fixture(scope="session", autouse=True)
def clean_directories_at_start() -> None:
    """Clean downloads directory at session start."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER") or "local"

    # Clean downloads
    downloads_dir = Path(constants.Files.DOWNLOADS_FOLDER) / worker_id
    clean_directory(downloads_dir, worker_id)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """
    Configure pytest settings for browser testing with Allure reporting.
    This function sets up the browser configuration based on environment variables or default settings,
    ensures the Allure results directory is properly managed (cleaned for local runs, preserved in CI/xdist),
    and generates an environment.properties file with relevant test metadata.
    Key actions:
    - Retrieves and sets the browser type (defaulting to settings.BROWSER).
    - Configures headless mode from settings.
    - For Chrome, sets up a user data directory and adds necessary Chromium arguments.
    - Manages the Allure results directory: cleans it for non-CI, non-xdist runs; ensures existence otherwise.
    - Writes environment properties including browser, headless mode, base URL, and CI-specific details.
    Args:
        config (pytest.Config): The pytest configuration object to modify.
    """
    is_ci_environment = os.environ.get("JENKINS_HOME") or os.environ.get("GITHUB_ACTIONS")
    is_xdist_worker = os.environ.get("PYTEST_XDIST_WORKER")
    browser = os.environ.get("BROWSER", settings.BROWSER).lower()

    # Store for use in fixtures
    config.browser = browser  # type: ignore[attr-defined]

    config.option.browser = browser
    config.option.headless = settings.HEADLESS

    # Add Chrome arguments for user profile
    if browser == "chrome" and not is_ci_environment:
        user_data_dir = os.path.abspath("chrome_user_data")
        os.makedirs(user_data_dir, exist_ok=True)

        # Add chromium arguments
        if not hasattr(config.option, "chromium_arg") or not config.option.chromium_arg:
            config.option.chromium_arg = []

        config.option.chromium_arg.extend(
            [
                f"--user-data-dir={user_data_dir}",
                "--profile-directory=Default",
            ]
        )

    # Get the allure results directory from pytest options
    allure_results_dir = getattr(config.option, "allure_report_dir", None)

    if not allure_results_dir:
        # Fallback to default if not specified
        allure_results_dir = str(Path("reports") / "allure-results")
        config.option.allure_report_dir = allure_results_dir

    allure_results_path = Path(allure_results_dir)

    # Clean allure results ONLY for non-xdist runs and local development
    # Don't clean in CI environments (Jenkins or GitHub Actions) where browsers run in parallel

    if not is_xdist_worker and not is_ci_environment:
        if allure_results_path.exists():
            logging.info(f"Cleaning Allure results directory: {allure_results_path}")
            shutil.rmtree(allure_results_path, ignore_errors=True)

        # Create fresh directory
        allure_results_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created fresh Allure results directory: {allure_results_path}")
    else:
        # In CI or xdist, just ensure directory exists
        allure_results_path.mkdir(parents=True, exist_ok=True)
        if is_ci_environment:
            logging.info(f"Running in CI environment - preserving existing results in: {allure_results_path}")

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


@pytest.fixture(autouse=True)
def bind_test_context(request: pytest.FixtureRequest) -> None:
    """Binds test context variables for structured logging.

    This function sets up context variables for structlog, including the test name
    from the pytest request and the browser setting. It is typically used as a pytest
    fixture to provide logging context during test execution.

    Args:
        request (pytest.FixtureRequest): The pytest fixture request object, which
            contains information about the current test node.
    """
    structlog.contextvars.bind_contextvars(test_name=request.node.name, browser=settings.BROWSER)
