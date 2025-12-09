import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("iframe")
@allure.story("Tests iframe functionality")
class TestIframe(UiBaseCase):
    """Tests iframe functionality"""

    TEXT = "Testing switch to iframe functionality"

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_iframe_functionality(self) -> None:
        self.logger.info("Tests iframe.")
        main_page = MainPage(self)
        page = main_page.click_frames_link()

        self.logger.info("Clicking iframe link.")
        iframe_page = page.click_iframe_link()

        self.logger.info("Checking if herokuapp blocked – TinyMCE read-only mode.")
        if "read-only" in self.get_page_source():
            self.logger.info("Skipping test: herokuapp blocked – TinyMCE read-only mode.")
            pytest.skip("herokuapp blocked – TinyMCE read-only mode")

        self.logger.info("Switching to iframe.")
        iframe_page.switch_to_iframe()

        self.logger.info("Sending text to iframe's rich text area.")
        iframe_page.send_text_to_rich_text_area(self.TEXT)

        # TODO: Test rich text area buttons - TinyMCE always blocked.

        self.logger.info("Getting text from iframe's rich text area.")
        frame_text = iframe_page.get_iframe_text()

        self.logger.info("Verifying text in iframe's rich text area.")
        assert self.TEXT == frame_text, (
            f"Expected frame text '{self.TEXT}',\
              got '{frame_text}'"
        )
