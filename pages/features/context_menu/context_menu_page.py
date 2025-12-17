from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import allure
from selenium.common.exceptions import (
    NoAlertPresentException,
)

from pages.base.base_page import BaseCase, BasePage
from pages.features.context_menu.locators import ContextMenuPageLocators

if TYPE_CHECKING:
    pass


@dataclass
class ClickResult:
    alert_present: bool
    alert_text: str = ""


class ContextMenuPage(BasePage):
    """Page object for the Context Menu page containing methods to interact with and validate page context menu"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(ContextMenuPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Perform right click outside hot spot area")
    def right_click_outside_hot_spot(self) -> ClickResult:
        self.perform_right_click(ContextMenuPageLocators.PAGE_LOADED_INDICATOR)
        return ClickResult(alert_present=False)

    @allure.step("Perform right click on hot spot area")
    def right_click_on_hot_spot(self) -> None:
        self.perform_right_click(ContextMenuPageLocators.HOT_SPOT_BOX)

    @allure.step("Get context menu alert text")
    def get_context_menu_alert_text(self, timeout: int = 5) -> str:
        self.logger.info("Waiting for context menu alert...")
        try:
            alert = self.driver.wait_for_and_switch_to_alert(timeout=timeout)
            text = alert.text
            self.logger.debug(f"Alert text: '{text}'")
            return text
        except Exception:
            self.logger.error("Alert did not appear within timeout")
            raise NoAlertPresentException("Alert not present after right-click")

    @allure.step("Close context menu alert")
    def close_context_menu_alert(self) -> None:
        self.driver.accept_alert()
