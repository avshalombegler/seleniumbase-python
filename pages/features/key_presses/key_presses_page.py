from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.key_presses.locators import KeyPressesPageLocators

if TYPE_CHECKING:
    from logging import Logger

    from selenium.webdriver.common.keys import Keys


class KeyPressesPage(BasePage):
    """Page object for the Key Presses page containing methods to interact with and validate
    page functionality"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(KeyPressesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Press key")
    def press_key(self, key: Keys) -> None:
        elem = self.wait_for_visibility(KeyPressesPageLocators.TEXT_INPUT)
        self.actions.send_keys_to_element(elem, key).perform()

    @allure.step("Get result")
    def get_result(self) -> str:
        return self.get_dynamic_element_text(KeyPressesPageLocators.RESULT)
