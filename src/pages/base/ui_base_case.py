from __future__ import annotations

import os
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

        Performs the following:
        1. Calls parent class's tearDown method for standard cleanup
        2. Attaches accumulated test logs to Allure report (formatted, without ANSI codes)
        3. On test failure, attaches screenshot from 'latest_logs' directory to Allure report

        The logs are accumulated in memory during test execution and attached as a single
        text block. The buffer is cleared after attachment to prevent duplication in
        subsequent tests.
        """
        super().tearDown()

        # Attach accumulated test logs to Allure
        try:
            from src.config.logging_config import get_allure_handler

            handler = get_allure_handler()
            if handler:
                logs_content = handler.get_logs()
                if logs_content.strip():
                    allure.attach(
                        logs_content,
                        name="Test Logs",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    handler.clear()
        except Exception as e:
            self.logger.error(f"Failed to attach test logs to Allure: {e}")

        # Attach screenshot to Allure Report on failure
        if hasattr(self, "request") and hasattr(self, "_outcome") and self._outcome.errors:
            try:
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name=f"Failed Screenshot - {self.request.node.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
                self.logger.info(f"Test failed - screenshot attached for: {self.request.node.name}")
            except Exception as e:
                self.logger.error(f"Failed to attach screenshot: {e}")
