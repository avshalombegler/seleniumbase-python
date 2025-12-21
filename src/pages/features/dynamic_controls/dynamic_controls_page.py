from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.dynamic_controls.locators import DynamicControlsPageLocators

if TYPE_CHECKING:
    pass


class DynamicControlsPage(BasePage):
    """Page object for the Dynamic Content page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(DynamicControlsPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click remove button")
    def click_remove_button(self, timeout: int = 10) -> None:
        self.click_element(DynamicControlsPageLocators.REMOVE_BTN)
        if not self.wait_for_loader(DynamicControlsPageLocators.WAIT_LOADER, timeout=timeout):
            self.logger.warning("Loader did not complete normally, continuing test...")

    @allure.step("Click add button")
    def click_add_button(self, timeout: int = 10) -> None:
        self.click_element(DynamicControlsPageLocators.ADD_BTN)
        if not self.wait_for_loader(DynamicControlsPageLocators.WAIT_LOADER, timeout=timeout):
            self.logger.warning("Loader did not complete normally, continuing test...")

    @allure.step("Check if checkbox is visible or not visible")
    def is_checkbox_visible(self, timeout: int = 10) -> bool:
        try:
            self.driver.wait_for_element_visible(**DynamicControlsPageLocators.A_CHECKBOX, timeout=timeout)
            return True
        except (ElementNotVisibleException, NoSuchElementException, Exception):
            return False

    @allure.step("Click enable button")
    def click_enable_button(self, timeout: int = 10) -> None:
        self.click_element(DynamicControlsPageLocators.ENABLE_BTN)
        if not self.wait_for_loader(DynamicControlsPageLocators.WAIT_LOADER, timeout=timeout):
            self.logger.warning("Loader did not complete normally, continuing test...")

    @allure.step("Click disable button")
    def click_disable_button(self, timeout: int = 10) -> None:
        self.click_element(DynamicControlsPageLocators.DISABLE_BTN)
        if not self.wait_for_loader(DynamicControlsPageLocators.WAIT_LOADER, timeout=timeout):
            self.logger.warning("Loader did not complete normally, continuing test...")

    @allure.step("Check if textbox is enabled or disabled")
    def is_textbox_enabled(self, timeout: int = 10) -> bool:
        return self.is_element_enabled(DynamicControlsPageLocators.TEXTBOX, timeout=timeout)

    @allure.step("Get Remove/add message text")
    def get_remove_add_message(self) -> str:
        element = self.wait_for_visibility(DynamicControlsPageLocators.REMOVE_ADD_MSG)
        return element.text

    @allure.step("Get Enable/disable message text")
    def get_enable_disable_message(self) -> str:
        element = self.wait_for_visibility(DynamicControlsPageLocators.ENABLE_DISABLE_MSG)
        return element.text
