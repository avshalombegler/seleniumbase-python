from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import allure
import pytest
import structlog
from seleniumbase import BaseCase
from seleniumbase.fixtures import constants

from src.config import settings

if TYPE_CHECKING:
    from typing import Any


class UiBaseCase(BaseCase):
    @pytest.fixture(autouse=True)
    def _inject_request(self, request: pytest.FixtureRequest) -> None:
        """Inject pytest request object for parametrization support"""
        self.request = request

    def get_new_driver(self, *args: Any, **kwargs: Any) -> Any:
        """Override to set download directory before driver creation."""
        worker_id: str = os.environ.get("PYTEST_XDIST_WORKER") or "local"
        downloads_dir: str = os.path.abspath(os.path.join(constants.Files.DOWNLOADS_FOLDER, worker_id))
        os.makedirs(downloads_dir, exist_ok=True)

        self.downloads_folder = downloads_dir
        driver = super().get_new_driver(*args, **kwargs)

        if self.browser == "chrome":
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": downloads_dir})
            self.logger = structlog.get_logger(self.__class__.__name__)
            self.logger.info("Chrome download directory set to", download_path=downloads_dir)

        return driver

    def get_downloads_folder(self) -> str:
        """Override to return the per-worker download directory."""
        worker_id = os.environ.get("PYTEST_XDIST_WORKER") or "local"
        downloads_dir = os.path.abspath(os.path.join(constants.Files.DOWNLOADS_FOLDER, worker_id))
        return downloads_dir

    def get_browser_downloads_folder(self) -> str:
        """Override to return the per-worker download directory for browser downloads."""
        return self.get_downloads_folder()

    def setUp(self) -> None:
        """
        Set up the test environment for UI-based tests.
        This method initializes the logger using structlog with the class name,
        retrieves the worker ID from the PYTEST_XDIST_WORKER environment variable
        (or defaults to 'local' if not set), and navigates to the base URL if the
        test is marked with @pytest.mark.ui. The navigation is logged as an Allure step.
        """
        super().setUp()
        self.logger = structlog.get_logger(self.__class__.__name__)
        self.worker_id = os.environ.get("PYTEST_XDIST_WORKER") or "local"

        # Navigate to base URL if @pytest.mark.ui
        if hasattr(self, "request") and self.request.node.get_closest_marker("ui"):
            with allure.step(f"Navigate to base URL: {settings.BASE_URL}"):
                self.open(settings.BASE_URL)

    def tearDown(self) -> None:
        """
        Clean up after each test method.
        Calls the parent class's tearDown method to perform standard cleanup.
        If the test failed (indicated by errors in _outcome), attempts to attach
        a screenshot from the 'latest_logs' directory to the Allure report.
        The screenshot path is derived from the test node ID, and if it exists,
        it is attached as a PNG file with a descriptive name. Logs success or
        failure of the attachment process.
        """
        super().tearDown()

        # Attach screenshot to Allure Report on failure
        if hasattr(self, "request") and hasattr(self, "_outcome") and self._outcome.errors:
            try:
                nodeid = self.request.node.nodeid
                test_path = nodeid.replace(".py::", ".").replace("::", ".").replace("/", ".").replace("\\", ".")

                screenshot_dir = Path("latest_logs") / test_path
                screenshot_filename = "screenshot.png"
                screenshot_path = screenshot_dir / screenshot_filename

                if os.path.exists(screenshot_path):
                    allure.attach.file(
                        screenshot_path,
                        name=f"Failed Screenshot - {self.request.node.name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
                    self.logger.info(f"Test failed - screenshot attached from: {screenshot_path}")
            except Exception as e:
                self.logger.error(f"Failed to attach screenshot: {e}")
