from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.floating_menu.locators import FloatingMenuPageLocators

if TYPE_CHECKING:
    pass


class FloatingMenuPage(BasePage):
    """Page object for the Floating Menu page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(FloatingMenuPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Scroll down")
    def scroll_down(self) -> None:
        self.driver.execute_script("window.scrollBy(0, 500);")

    @allure.step("Click floating menu item '{item}'")
    def click_floating_menu_item(self, item: str) -> None:
        locator = self.format_locator(FloatingMenuPageLocators.MENU_ITEM, item=item)
        self.click_element(locator)
