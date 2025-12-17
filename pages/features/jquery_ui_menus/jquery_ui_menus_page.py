from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.jquery_ui_menus.locators import JQueryUIMenusPageLocators

if TYPE_CHECKING:
    pass


class JQueryUIMenusPage(BasePage):
    """Page object for the JQueryUI - Menu page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(JQueryUIMenusPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Hover over menu item '{item}'")
    def hover_menu_item(self, item: str) -> None:
        locator = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM, item=item)
        self.driver.hover(**locator)
        self.driver.sleep(0.3)  # Allow menu animation to complete

    @allure.step("Click menu item '{item}'")
    def click_menu_item(self, item: str) -> None:
        locator = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM, item=item)
        # self.driver.hover(**locator)
        elem = self.driver.wait_for_element_visible(**locator)
        self.actions.move_to_element(elem).perform()
        self.driver.sleep(0.3)  # Allow menu animation
        self.driver.click(**locator)
