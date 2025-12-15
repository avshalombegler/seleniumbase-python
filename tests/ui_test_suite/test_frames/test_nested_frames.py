import allure
import pytest
from parameterized import parameterized

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Frames")
@allure.sub_suite("Tests Nested Frames functionality")
class TestNestedFrames(UiBaseCase):
    """Tests Nested Frames functionality"""

    TOP_FRAME = "top"
    BOTTOM_FRAME = "bottom"
    NESTED_FRAMES = [["left"], ["middle"], ["right"]]

    @parameterized.expand(NESTED_FRAMES)
    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_top_nested_frames_functionality(self, frame: str) -> None:
        self.logger.info("Tests Nested Frames.")
        main_page = MainPage(self)
        page = main_page.click_frames_link()

        self.logger.info("Clicking Nested Frames link.")
        nested_frames_page = page.click_nested_frames_link()

        self.logger.info(f"Switching to frame '{self.TOP_FRAME}'.")
        nested_frames_page.switch_frame(self.TOP_FRAME)

        self.logger.info(f"Switching to nested frame '{frame}'.")
        nested_frames_page.switch_frame(frame)

        self.logger.info("Getting frame text.")
        frame_text = nested_frames_page.get_frame_text()

        self.logger.info("Verifying frame text.")
        assert frame.upper() == frame_text, (
            f"Expected frame text '{frame.upper()}',\
              got '{frame_text}'"
        )

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_bottom_nested_frames_functionality(self) -> None:
        self.logger.info("Tests Nested Frames.")
        main_page = MainPage(self)
        page = main_page.click_frames_link()

        self.logger.info("Clicking Nested Frames link.")
        nested_frames_page = page.click_nested_frames_link()

        self.logger.info(f"Switching to frame '{self.BOTTOM_FRAME}'.")
        nested_frames_page.switch_frame(self.BOTTOM_FRAME)

        self.logger.info("Getting frame text.")
        frame_text = nested_frames_page.get_frame_text()

        self.logger.info("Verifying frame text.")
        assert self.BOTTOM_FRAME.upper() == frame_text, (
            f"Expected frame text '{self.BOTTOM_FRAME.upper()}',\
              got '{frame_text}'"
        )
