import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Dynamic Controls")
@allure.sub_suite("Tests Dynamic Controls functionality")
class TestDynamicControls(UiBaseCase):
    """Tests Dynamic Controls functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    # @pytest.mark.flaky(reruns=2)
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkbox_remove_and_add(self) -> None:
        self.logger.info("Test Remove/add checkbox area.")
        main_page = MainPage(self)
        page = main_page.click_dynamic_controls_link()

        self.logger.info("Checking if checkbox is present.")
        self.assert_true(page.is_checkbox_visible(), "Expected checkbox to be present")

        self.logger.info("Clicking remove button.")
        page.click_remove_button()

        self.logger.info("Checking if checkbox absent.")
        self.assert_false(page.is_checkbox_visible(), "Expected checkbox to be absent")

        self.logger.info("Getting remove message text.")
        message = page.get_remove_add_message()

        self.logger.info("Verifying remove message text.")
        self.assert_in("It's gone!", message, f"Expected '{message}' to contain 'It's gone!'")

        self.logger.info("Clicking add button.")
        page.click_add_button()

        self.logger.info("Checking if checkbox is present.")
        self.assert_true(page.is_checkbox_visible(), "Expected checkbox to be present")

        self.logger.info("Getting add message text.")
        message = page.get_remove_add_message()

        self.logger.info("Verifying add message text.")
        self.assert_in("It's back!", message, f"Expected '{message}' to contain 'It's back!'")

    @pytest.mark.regression
    @pytest.mark.ui
    # @pytest.mark.flaky(reruns=2)
    @allure.severity(allure.severity_level.NORMAL)
    def test_textbox_enable_and_disable(self) -> None:
        self.logger.info("Test Enable/disable textbox area.")
        main_page = MainPage(self)
        page = main_page.click_dynamic_controls_link()

        self.logger.info("Checking if textbox is disabled.")
        self.assert_false(page.is_textbox_enabled(), "Expected textbox to be disabled")

        self.logger.info("Clicking enable button.")
        page.click_enable_button()

        self.logger.info("Checking if textbox is enabled.")
        self.assert_true(page.is_textbox_enabled(), "Expected textbox to be enabled")

        self.logger.info("Getting enable message text.")
        message = page.get_enable_disable_message()

        self.logger.info("Verifying enable message text.")
        self.assert_in("It's enabled!", message, f"Expected '{message}' to contain 'It's enabled!'")

        self.logger.info("Clicking disable button.")
        page.click_disable_button()

        self.logger.info("Checking if textbox is disabled.")
        self.assert_false(page.is_textbox_enabled(), "Expected textbox to be disabled")

        self.logger.info("Getting disable message text.")
        message = page.get_enable_disable_message()

        self.logger.info("Verifying disable message text.")
        self.assert_in("It's disabled!", message, f"Expected '{message}' to contain 'It's disabled!'")
