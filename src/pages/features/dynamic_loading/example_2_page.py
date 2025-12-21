from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.dynamic_loading.locators import Example2PageLocators

if TYPE_CHECKING:
    pass


class Example2Page(BasePage):
    """Page object for the Dynamic Content page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(Example2PageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click start button")
    def click_start_button(self, timeout: int = 10) -> None:
        self.click_element(Example2PageLocators.START_BTN)
        self.wait_for_loader(Example2PageLocators.WAIT_LOADER, timeout=timeout)

    @allure.step("Get success message")
    def get_success_message(self) -> str:
        return self.get_dynamic_element_text(Example2PageLocators.SUCCESS_MSG)
