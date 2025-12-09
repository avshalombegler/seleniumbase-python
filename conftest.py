"""Main conftest - integrates directory fixtures and hooks."""

import logging
import os
import shutil
import time
from collections.abc import Generator
from pathlib import Path

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.main import Session
from _pytest.nodes import Item
from filelock import FileLock
from seleniumbase.fixtures import constants

import config.env_config as env_config
from utils.logging_helper import configure_root_logger, set_current_test
from utils.video_recorder import start_video_recording

# Constants shared across plugins
DEBUG_PORT_BASE = 9222
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
CACHE_VALID_RANGE = 30

# Configure root logger once for the test session
root_logger = configure_root_logger(log_file="test_logs.log", level=logging.INFO)
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)


def get_worker_id() -> str:
    """Get worker ID for xdist or fallback to local PID."""
    return os.environ.get("PYTEST_XDIST_WORKER") or "local"


def clean_directory(dir_path: Path, lock_suffix: str = "lock") -> None:
    """Helper to clean and recreate a directory with file locking."""
    lock_file = dir_path / f"{lock_suffix}.lock"
    dir_path.mkdir(parents=True, exist_ok=True)
    with FileLock(lock_file):
        if dir_path.exists():
            shutil.rmtree(dir_path, ignore_errors=True)
        dir_path.mkdir(parents=True, exist_ok=True)
        root_logger.info(f"Directory cleaned and recreated at: {dir_path}.")


@pytest.fixture(scope="session", autouse=True)
def clean_directories_at_start(request: FixtureRequest) -> None:
    """Clean downloads directory at session start."""
    worker_id = get_worker_id()

    # Clean videos
    videos_dir = Path("tests_recordings") / worker_id
    clean_directory(videos_dir, worker_id)

    downloads_dir = Path(constants.Files.DOWNLOADS_FOLDER) / worker_id
    clean_directory(downloads_dir, worker_id)


@pytest.fixture(scope="function", autouse=True)
def video_recorder(request: FixtureRequest) -> Generator[None, None, None]:
    """
    Automatically records video of the test session using Chrome DevTools Protocol.
    Recording is enabled only if VIDEO_RECORDING is True in config and driver is Chrome.
    Skips recording for non-Chrome drivers or when disabled.
    """
    if not getattr(env_config, "VIDEO_RECORDING", False):
        yield
        return

    # For class-based tests inheriting from BaseCase, get driver from the test instance
    if hasattr(request.instance, "driver"):
        driver = request.instance.driver
    else:
        # For function-based tests, assume 'sb' fixture is used
        driver = request.getfixturevalue("sb")

    worker_id = get_worker_id()
    test_name = request.node.name.replace(":", "_").replace("/", "_")

    stop_func, video_path = start_video_recording(driver, test_name, worker_id)
    root_logger.info(f"Started recording: {video_path}")

    try:
        yield
    finally:
        try:
            root_logger.info("Stopping video recording...")
            stop_func()

            # Wait briefly to ensure video is fully written
            time.sleep(1.0)

            # Attach video to test body
            video_path_obj = Path(video_path)
            if video_path_obj.exists() and video_path_obj.stat().st_size > 0:
                try:
                    lock_file = video_path_obj.parent / f"{worker_id}.lock"
                    with FileLock(lock_file):
                        allure.attach.file(
                            str(video_path_obj),
                            name="Test Recording",
                            attachment_type=allure.attachment_type.MP4,
                        )
                        root_logger.info(f"Video attached to test body: {video_path_obj}")
                except Exception as e:
                    root_logger.error(f"Failed to attach video: {str(e)}")
            else:
                root_logger.warning(f"Video file not found or empty: {video_path_obj}")
        except Exception as e:
            root_logger.error(f"Failed to stop video recording: {str(e)}")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Add browser info to Allure environment and ensure clean results directory."""
    browser = os.environ.get("BROWSER", env_config.BROWSER).lower()

    # Store for use in fixtures
    config.browser = browser  # type: ignore[attr-defined]

    config.option.browser = browser
    config.option.headless = env_config.HEADLESS

    # if not is_xdist_worker and env_config.VIDEO_RECORDING:
    if env_config.VIDEO_RECORDING:
        config.option.recorder_mode = "video"

    # Get the allure results directory from pytest options
    allure_results_dir = getattr(config.option, "allure_report_dir", None)

    if not allure_results_dir:
        # Fallback to default if not specified
        allure_results_dir = str(Path("reports") / "allure-results")
        config.option.allure_report_dir = allure_results_dir

    allure_results_path = Path(allure_results_dir)

    # Clean allure results ONLY for non-xdist runs and local development
    # Don't clean in CI environments (Jenkins or GitHub Actions) where browsers run in parallel
    is_ci_environment = os.environ.get("JENKINS_HOME") or os.environ.get("GITHUB_ACTIONS")
    is_xdist_worker = os.environ.get("PYTEST_XDIST_WORKER")

    if not is_xdist_worker and not is_ci_environment:
        if allure_results_path.exists():
            root_logger.info(f"Cleaning Allure results directory: {allure_results_path}")
            shutil.rmtree(allure_results_path, ignore_errors=True)

        # Create fresh directory
        allure_results_path.mkdir(parents=True, exist_ok=True)
        root_logger.info(f"Created fresh Allure results directory: {allure_results_path}")
    else:
        # In CI or xdist, just ensure directory exists
        allure_results_path.mkdir(parents=True, exist_ok=True)
        if is_ci_environment:
            root_logger.info(f"Running in CI environment - preserving existing results in: {allure_results_path}")

    env_properties_path = allure_results_path / "environment.properties"
    with open(env_properties_path, "w") as f:
        f.write(f"Browser={browser.capitalize()}\n")
        f.write(f"Headless={env_config.HEADLESS}\n")
        f.write(f"Maximized={env_config.MAXIMIZED}\n")
        f.write(f"Base.URL={env_config.BASE_URL}\n")
        f.write(f"Window.Size={WINDOW_WIDTH}x{WINDOW_HEIGHT}\n")
        if os.environ.get("GITHUB_ACTIONS"):
            f.write(f"Run.ID={os.environ.get('GITHUB_RUN_ID', 'N/A')}\n")
            f.write(f"Workflow={os.environ.get('GITHUB_WORKFLOW', 'N/A')}\n")
        elif os.environ.get("JENKINS_HOME"):
            f.write(f"Build.Number={os.environ.get('BUILD_NUMBER', 'N/A')}\n")
            f.write(f"Job.Name={os.environ.get('JOB_NAME', 'N/A')}\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item) -> Generator[None, None, None]:
    """
    Pytest hook to handle:
        - Test duration logging.
        - Screenshot taking on test failure (Locally and to Allure Report).
    """
    outcome = yield
    report = outcome.get_result()  # type: ignore[attr-defined]

    if report.when == "setup":
        # Set the test name for logging context
        set_current_test(item.name)

    if report.when == "call":
        test_name = item.name
        duration = report.duration if hasattr(report, "duration") else 0

        # Log outcome explicitly
        outcome_str = "PASSED" if report.passed else "FAILED" if report.failed else "SKIPPED"
        root_logger.info(f"Test {outcome_str}: {test_name} (Duration: {duration:.2f}s).")

        # Take screenshot only on failure (handled by SeleniumBase)
        if report.failed:
            root_logger.info("Test failed - screenshot captured by SeleniumBase BaseCase")

    elif report.when == "teardown":
        set_current_test(None)
        # Log teardown failures explicitly
        if report.failed:
            root_logger.error(f"Test teardown failed for: {item.name}")
            root_logger.info("Teardown failure logged - SeleniumBase handles screenshots")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """
    Log final test session results.
    """
    passed = session.testscollected - session.testsfailed
    root_logger.info(
        f"Test session finished. Total: {session.testscollected}, "
        f"Passed: {passed}, Failed: {session.testsfailed}, "
        f"Exit status: {exitstatus}"
    )


@pytest.fixture
def logger(request) -> logging.Logger:
    from utils.logging_helper import get_logger

    # Use the test class name if available, else the test function name
    test_class = getattr(request.instance, "__class__", None)
    name = test_class.__name__ if test_class else request.node.name
    return get_logger(name)
