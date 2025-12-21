from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.exit_intent.locators import ExitIntentPageLocators

if TYPE_CHECKING:
    pass


class ExitIntentPage(BasePage):
    """Page object for the Exit Intent page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(ExitIntentPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Trigger exit intent via JavaScript (headless fallback)")
    def trigger_exit_intent_js(self) -> None:
        self.driver.execute_script(
            """
            var event = new Event('mouseleave');
            document.dispatchEvent(event);
        """
        )

    @allure.step("Click close window")
    def click_close_modal(self) -> None:
        self.click_element(ExitIntentPageLocators.CLOSE_BTN)

    @allure.step("Check modal window display")
    def is_modal_displayed(self) -> bool:
        return self.is_element_visible(ExitIntentPageLocators.MODAL_LOADED_INDICATOR, timeout=5)
