import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("JavaScript Alerts")
@allure.sub_suite("Tests JavaScript Alerts functionality")
class TestJavaScriptAlerts(UiBaseCase):
    """Tests JavaScript Alerts functionality"""

    ALERT_SUCCESS_MSG = "success"
    CONFIRM_OK_MSG = "ok"
    CONFIRM_CANCEL_MSG = "cancel"
    PROMPT_ENTERED_MSG = "testing js prompt alert"
    PROMPT_NULL_MSG = "null"

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_js_alert_functionality(self) -> None:
        self.logger.info("Tests JS Alert.")
        main_page = MainPage(self)
        page = main_page.click_javascript_alerts_link()

        self.logger.info("Clicking JS Alert button.")
        page.click_js_alert_button()

        self.logger.info("Wait for and accept alert.")
        page.driver.wait_for_and_accept_alert()

        self.logger.info("Getting result text.")
        result = page.get_result_text()

        self.logger.info("Verifying result text.")
        self.assert_in(
            self.ALERT_SUCCESS_MSG,
            result.lower(),
            f"Expected '{result}', to contain '{self.ALERT_SUCCESS_MSG}'",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_js_confirm(self) -> None:
        self.logger.info("Tests JS Confirm.")
        main_page = MainPage(self)
        page = main_page.click_javascript_alerts_link()

        self.logger.info("Clicking JS Confirm button.")
        page.click_js_confirm_button()

        self.logger.info("Wait for and accept alert.")
        page.driver.wait_for_and_accept_alert()

        self.logger.info("Getting result text.")
        result = page.get_result_text()

        self.logger.info("Verifying result text.")
        self.assert_in(
            self.CONFIRM_OK_MSG,
            result.lower(),
            f"Expected '{result}', to contain '{self.CONFIRM_OK_MSG}'",
        )

        self.logger.info("Clicking JS Confirm button.")
        page.click_js_confirm_button()

        self.logger.info("Wait for and dismiss alert.")
        page.driver.wait_for_and_dismiss_alert()

        self.logger.info("Getting result text.")
        result = page.get_result_text()

        self.logger.info("Verifying result text.")
        self.assert_in(
            self.CONFIRM_CANCEL_MSG,
            result.lower(),
            f"Expected '{result}', to contain '{self.CONFIRM_CANCEL_MSG}'",
        )

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_js_prompt(self) -> None:
        self.logger.info("Tests JS Prompt.")
        main_page = MainPage(self)
        page = main_page.click_javascript_alerts_link()

        self.logger.info("Clicking JS Prompt button.")
        page.click_js_prompt_button()

        self.logger.info("Entering JS Prompt text.")
        page.enter_prompt_text(self.PROMPT_ENTERED_MSG)

        self.logger.info("Gettingting result text.")
        result = page.get_result_text()

        self.logger.info("Verifying result text.")
        self.assert_in(
            self.PROMPT_ENTERED_MSG,
            result.lower(),
            f"Expected '{result}', to contain '{self.PROMPT_ENTERED_MSG}'",
        )

        self.logger.info("Clicking JS Prompt button.")
        page.click_js_prompt_button()

        self.logger.info("Wait for and dismiss alert.")
        page.driver.wait_for_and_dismiss_alert()

        self.logger.info("Gettingting result text.")
        result = page.get_result_text()

        self.logger.info("Verifying result text.")
        self.assert_in(
            self.PROMPT_NULL_MSG,
            result.lower(),
            f"Expected '{result}', to contain '{self.PROMPT_NULL_MSG}'",
        )
