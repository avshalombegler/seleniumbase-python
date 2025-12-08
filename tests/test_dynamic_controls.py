import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("Dynamic Controls")
@allure.story("Tests Dynamic Controls functionality")
class TestDynamicControls(UiBaseCase):
    """Tests Dynamic Controls functionality"""

    # @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.ui
    # @pytest.mark.flaky(reruns=2)
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkbox_remove_and_add(self) -> None:
        self.logger.info("Test Remove/add checkbox area.")
        main_page = MainPage(self)
        page = main_page.click_dynamic_controls_link()

        self.logger.info("Checking if checkbox is present.")
        assert page.is_checkbox_present(), "Expected checkbox to be present"

        self.logger.info("Clicking remove button.")
        page.click_remove_button()

        self.logger.info("Checking if checkbox absent.")
        assert not page.is_checkbox_present(), "Expected checkbox to be absent"

        self.logger.info("Getting remove message text.")
        message = page.get_remove_add_message()

        self.logger.info("Verifying remove message text.")
        assert "It's gone!" in message, f"Expected '{message}' to contain 'It's gone!'"

        self.logger.info("Clicking add button.")
        page.click_add_button()

        self.logger.info("Checking if checkbox is present.")
        assert page.is_checkbox_present(), "Expected checkbox to be present"

        self.logger.info("Getting add message text.")
        message = page.get_remove_add_message()

        self.logger.info("Verifying add message text.")
        assert "It's back!" in message, f"Expected '{message}' to contain 'It's back!'"

    # @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.ui
    # @pytest.mark.flaky(reruns=2)
    @allure.severity(allure.severity_level.NORMAL)
    def test_textbox_enable_and_disable(self) -> None:
        self.logger.info("Test Enable/disable textbox area.")
        main_page = MainPage(self)
        page = main_page.click_dynamic_controls_link()

        self.logger.info("Checking if textbox is disabled.")
        assert not page.is_textbox_enabled(), "Expected textbox to be disabled"

        self.logger.info("Clicking enable button.")
        page.click_enable_button()

        self.logger.info("Checking if textbox is enabled.")
        assert page.is_textbox_enabled(), "Expected textbox to be enabled"

        self.logger.info("Getting enable message text.")
        message = page.get_enable_disable_message()

        self.logger.info("Verifying enable message text.")
        assert "It's enabled!" in message, f"Expected '{message}' to contain 'It's enabled!'"

        self.logger.info("Clicking disable button.")
        page.click_disable_button()

        self.logger.info("Checking if textbox is disabled.")
        assert not page.is_textbox_enabled(), "Expected textbox to be disabled"

        self.logger.info("Getting disable message text.")
        message = page.get_enable_disable_message()

        self.logger.info("Verifying disable message text.")
        assert "It's disabled!" in message, f"Expected '{message}' to contain 'It's disabled!'"
