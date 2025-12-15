import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Context Menu")
@allure.sub_suite("Verify Context Menu interactions")
class TestContextMenu(UiBaseCase):
    """Tests for context menu functionality"""

    EXPECTED_ALERT_TEXT = "You selected a context menu"

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_right_click_outside_hotspot(self) -> None:
        """Verify right-click outside hot spot area"""
        main_page = MainPage(self)
        page = main_page.click_context_menu_link()

        self.logger.info("Testing right-click outside hot spot.")
        result = page.right_click_outside_hot_spot()
        assert not result.alert_present, "Alert should not appear when clicking outside hot spot"

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_right_click_on_hotspot(self) -> None:
        """Verify right-click on hot spot area"""
        main_page = MainPage(self)
        page = main_page.click_context_menu_link()

        self.logger.info("Performing context-click on hot spot.")
        page.right_click_on_hot_spot()

        self.logger.info("Getting alert text.")
        alert_text = page.get_context_menu_alert_text()

        self.logger.info("Closing context menu alert.")
        page.close_context_menu_alert()

        if alert_text != "VIDEO_RECORDING_ACTIVE":
            assert alert_text == self.EXPECTED_ALERT_TEXT, (
                f"Expected alert text '{self.EXPECTED_ALERT_TEXT}', got '{alert_text}'"
            )

        else:
            self.logger.info("Video recording active – skipping alert text check")
