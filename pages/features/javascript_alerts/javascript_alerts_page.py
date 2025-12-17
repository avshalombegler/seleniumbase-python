from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.javascript_alerts.locators import JavaScriptAlertsPageLocators

if TYPE_CHECKING:
    pass


class JavaScriptAlertsPage(BasePage):
    """Page object for the JavaScript Alerts page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(JavaScriptAlertsPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click JS Alert button")
    def click_js_alert_button(self) -> None:
        button = self.wait_for_visibility(JavaScriptAlertsPageLocators.JS_ALERTS_BTN)
        button.click()

    @allure.step("Click JS Confirm button")
    def click_js_confirm_button(self) -> None:
        button = self.wait_for_visibility(JavaScriptAlertsPageLocators.JS_CONFIRM_BTN)
        button.click()

    @allure.step("Click JS Prompt button")
    def click_js_prompt_button(self) -> None:
        button = self.wait_for_visibility(JavaScriptAlertsPageLocators.JS_PROMPT_BTN)
        button.click()

    @allure.step("Enter text in prompt and accept")
    def enter_prompt_text(self, text: str) -> None:
        alert = self.driver.wait_for_and_switch_to_alert()
        alert.send_keys(text)
        alert.accept()

    @allure.step("Get result text")
    def get_result_text(self) -> str:
        return self.get_dynamic_element_text(JavaScriptAlertsPageLocators.RESULT)
