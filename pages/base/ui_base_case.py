import logging
import os

import allure
import pytest
from seleniumbase import BaseCase

import config.env_config as env_config


class UiBaseCase(BaseCase):
    @pytest.fixture(autouse=True)
    def _inject_request(self, request) -> None:
        """Inject pytest request object for parametrization support"""
        self.request = request

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
