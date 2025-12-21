from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.key_presses.locators import KeyPressesPageLocators

if TYPE_CHECKING:
    pass


class KeyPressesPage(BasePage):
    """Page object for the Key Presses page containing methods to interact with and validate
    page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(KeyPressesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Press key")
    def press_key(self, key: str) -> None:
        elem = self.wait_for_visibility(KeyPressesPageLocators.TEXT_INPUT)
        elem.send_keys(key)

    @allure.step("Get result")
    def get_result(self) -> str:
        return self.get_dynamic_element_text(KeyPressesPageLocators.RESULT)
