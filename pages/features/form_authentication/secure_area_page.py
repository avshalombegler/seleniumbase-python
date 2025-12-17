from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.form_authentication.locators import SecureAreaPageLocators

if TYPE_CHECKING:
    from pages.features.form_authentication.form_authentication_page import FormAuthenticationPage


class SecureAreaPage(BasePage):
    """Page object for the Secure Area page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(SecureAreaPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get flash message")
    def get_flash_message(self) -> str:
        return self.get_dynamic_element_text(SecureAreaPageLocators.FLASH_MSG)

    @allure.step("Click logout")
    def click_logout(self) -> FormAuthenticationPage:
        self.click_element(SecureAreaPageLocators.LOGOUT_BTN)
        from pages.features.form_authentication.form_authentication_page import FormAuthenticationPage

        return FormAuthenticationPage(self.driver)
