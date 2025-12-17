import logging
import os
from pathlib import Path

import allure
import pytest
from seleniumbase import BaseCase
from seleniumbase.fixtures import constants

from config import settings


class UiBaseCase(BaseCase):
    @pytest.fixture(autouse=True)
    def _inject_request(self, request) -> None:
        """Inject pytest request object for parametrization support"""
        self.request = request

    def get_new_driver(self, *args, **kwargs):
        """Override to set download directory before driver creation."""
        worker_id = os.environ.get("PYTEST_XDIST_WORKER") or "local"
        downloads_dir = os.path.abspath(os.path.join(constants.Files.DOWNLOADS_FOLDER, worker_id))
        os.makedirs(downloads_dir, exist_ok=True)

        self.downloads_folder = downloads_dir
        driver = super().get_new_driver(*args, **kwargs)

        if self.browser == "chrome":
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": downloads_dir})
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.info(f"Chrome download directory set to: {downloads_dir}")

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
        super().setUp()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.worker_id = os.environ.get("PYTEST_XDIST_WORKER") or "local"

        # Navigate to base URL if @pytest.mark.ui
        if hasattr(self, "request") and self.request.node.get_closest_marker("ui"):
            with allure.step(f"Navigate to base URL: {settings.BASE_URL}"):
                self.open(settings.BASE_URL)

    def tearDown(self) -> None:
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
