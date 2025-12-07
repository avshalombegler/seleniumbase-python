from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.frames.locators import IframesPageLocators

if TYPE_CHECKING:
    from logging import Logger


class IframesPage(BasePage):
    """Page object for the iFrame page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        if "read-only" not in self.driver.get_page_source().lower():
            self.wait_for_page_to_load(IframesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Switch to iframe'")
    def switch_to_iframe(self) -> None:
        self.switch_to_frame(IframesPageLocators.IFRAME)

    @allure.step("Send text to rich text area")
    def send_text_to_rich_text_area(self, text: str) -> None:
        self.send_keys_to_element(IframesPageLocators.RICH_TEXT_AREA, text)

    @allure.step("Get iframe text")
    def get_iframe_text(self) -> str:
        return self.get_dynamic_element_text(IframesPageLocators.RICH_TEXT_AREA)
