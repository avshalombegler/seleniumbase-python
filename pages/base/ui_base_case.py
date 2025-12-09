import logging
import os

import allure
import pytest
from seleniumbase import BaseCase
from seleniumbase.fixtures import constants

import config.env_config as env_config


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

        # Set the downloads folder attribute
        self.downloads_folder = downloads_dir

        # Get the driver from parent class
        driver = super().get_new_driver(*args, **kwargs)

        # For Chrome, update download preferences after driver creation
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

        # Check if test has @pytest.mark.ui decorator
        if hasattr(self, "request") and self.request.node.get_closest_marker("ui"):
            with allure.step(f"Navigate to base URL: {env_config.BASE_URL}"):
                self.open(env_config.BASE_URL)

    def tearDown(self) -> None:
        # Attach screenshot to Allure on failure
        if hasattr(self, "request") and hasattr(self, "_outcome") and self._outcome.errors:
            try:
                screenshot_path = f"screenshots/{self.worker_id}/{self.request.node.name}_fail.png"
                if os.path.exists(screenshot_path):
                    allure.attach.file(
                        screenshot_path,
                        name=f"Failed_Screenshot_{self.request.node.name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
                    self.logger.info("Test failed - screenshot attached to Allure Report")
            except Exception as e:
                self.logger.error(f"Failed to attach screenshot: {e}")

        super().tearDown()
