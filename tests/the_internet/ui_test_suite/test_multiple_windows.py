import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage

NEW_WINDOW_HEADING = "New Window"
ORIGINAL_WINDOW_HEADING = "Opening a new window"
NEW_WINDOW_URL_SEGMENT = "/windows/new"
WINDOWS_URL_SEGMENT = "/windows"


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("Multiple Windows")
class TestMultipleWindows(UiBaseCase):
    """Tests Multiple Windows functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    def test_new_window_opens_with_expected_content(self) -> None:
        self.logger.info("Test that a new window opens and contains expected content.")
        main_page = MainPage(self)
        page = main_page.click_windows_link()

        original_handle = self.driver.current_window_handle
        page.click_open_new_window()

        handles = page.get_window_handles()
        self.assert_equal(len(handles), 2, "Exactly two window handles should be open after clicking the link")
        new_handle = [h for h in handles if h != original_handle][0]
        page.switch_to_window(new_handle)
        self.assert_true(self.get_current_url().endswith("/windows/new"), "New window URL should end with /windows/new")
        self.assert_equal(page.get_page_heading(), NEW_WINDOW_HEADING, "New window heading should read 'New Window'")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_original_window_remains_after_new_window_opens(self) -> None:
        self.logger.info("Test that the original window remains intact after a new window opens.")
        main_page = MainPage(self)
        page = main_page.click_windows_link()

        original_handle = self.driver.current_window_handle
        page.click_open_new_window()

        handles = page.get_window_handles()
        self.assert_equal(len(handles), 2, "Two window handles should be open")
        page.switch_to_window(original_handle)
        self.assert_true(
            self.get_current_url().endswith("/windows"), "Original window URL should still end with /windows"
        )
        self.assert_equal(
            page.get_page_heading(),
            ORIGINAL_WINDOW_HEADING,
            "Original window heading should still read 'Opening a new window'",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_switch_between_windows(self) -> None:
        self.logger.info("Test switching back and forth between two window handles.")
        main_page = MainPage(self)
        page = main_page.click_windows_link()

        original_handle = self.driver.current_window_handle
        page.click_open_new_window()

        handles = page.get_window_handles()
        new_handle = [h for h in handles if h != original_handle][0]

        # In new window
        page.switch_to_window(new_handle)
        self.assert_equal(page.get_page_heading(), NEW_WINDOW_HEADING, "New window heading should be 'New Window'")
        # Back in original window
        page.switch_to_window(original_handle)
        self.assert_equal(
            page.get_page_heading(), ORIGINAL_WINDOW_HEADING, "Original window heading should be 'Opening a new window'"
        )
