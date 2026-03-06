from __future__ import annotations

import os
from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.jquery_ui_menus.locators import JQueryUIMenusPageLocators

if TYPE_CHECKING:
    pass


class JQueryUIMenusPage(BasePage):
    """Page object for the JQueryUI - Menu page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(JQueryUIMenusPageLocators.PAGE_LOADED_INDICATOR)
        downloads_dir = self.driver.get_downloads_folder()
        for f in os.listdir(downloads_dir):
            file_path = os.path.join(downloads_dir, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

    @allure.step("Hover over menu item '{item}'")
    def hover_menu_item(self, item: str) -> None:
        locator = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM, item=item)
        self.driver.hover(**locator)

    @allure.step("Click menu item '{item}'")
    def hover_and_click_menu_item(self, item: str) -> None:
        click_locator = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM_LINK_XPATH, item=item)
        self.driver.js_click(click_locator["selector"], by=click_locator["by"])
