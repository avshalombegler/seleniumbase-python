from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.form_authentication.locators import FormAuthenticationPageLocators
from pages.features.form_authentication.secure_area_page import SecureAreaPage

if TYPE_CHECKING:
    pass


class FormAuthenticationPage(BasePage):
    """Page object for the Form Auth page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(FormAuthenticationPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Enter username '{username}'")
    def enter_username(self, username: str) -> None:
        self.send_keys_to_element(FormAuthenticationPageLocators.USERNAME_TEXTBOX, username)

    @allure.step("Enter password '{password}'")
    def enter_password(self, password: str) -> None:
        self.send_keys_to_element(FormAuthenticationPageLocators.PASSWORD_TEXTBOX, password)

    @allure.step("Click login - correct")
    def click_login_correct(self) -> SecureAreaPage:
        self.click_element(FormAuthenticationPageLocators.LOGIN_BTN)
        return SecureAreaPage(self.driver)

    @allure.step("Click login - invalid")
    def click_login_invalid(self) -> None:
        self.click_element(FormAuthenticationPageLocators.LOGIN_BTN)

    @allure.step("Get flash message")
    def get_flash_message(self) -> str:
        return self.get_dynamic_element_text(FormAuthenticationPageLocators.FLASH_MSG)
