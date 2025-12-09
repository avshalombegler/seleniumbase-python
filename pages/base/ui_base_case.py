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

        # Start video recording after driver is initialized
        if getattr(env_config, "VIDEO_RECORDING", False) and self.driver:
            from conftest import start_recording_safely
            from utils.video_recorder import start_video_recording

            test_name = self.request.node.name.replace(":", "_").replace("/", "_")

            try:
                stop_func, video_path = start_video_recording(self.driver, test_name, self.worker_id)
                start_recording_safely(self.request.node.nodeid, stop_func, video_path)
                self.logger.info(f"Started recording: {video_path}")
            except Exception as e:
                self.logger.error(f"Failed to start recording: {str(e)}")

    def tearDown(self) -> None:
        # Stop video recording before teardown
        if getattr(env_config, "VIDEO_RECORDING", False):
            import time
            from pathlib import Path

            from conftest import stop_recording_safely

            recording_info = stop_recording_safely(self.request.node.nodeid)
            if recording_info:
                stop_func, video_path = recording_info
                try:
                    self.logger.info("Stopping video recording...")
                    stop_func()
                    time.sleep(1.0)

                    video_path_obj = Path(video_path)
                    if video_path_obj.exists() and video_path_obj.stat().st_size > 0:
                        # No lock needed - each worker has separate files
                        allure.attach.file(
                            str(video_path_obj),
                            name="Test Recording",
                            attachment_type=allure.attachment_type.MP4,
                        )
                        self.logger.info(f"Video attached to test body: {video_path_obj}")
                    else:
                        self.logger.warning(f"Video file not found or empty: {video_path_obj}")
                except Exception as e:
                    self.logger.error(f"Failed to stop recording: {str(e)}")

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
