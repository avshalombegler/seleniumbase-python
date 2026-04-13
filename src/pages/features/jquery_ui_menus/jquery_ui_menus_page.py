from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.action_chains import ActionChains

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.jquery_ui_menus.locators import JQueryUIMenusPageLocators

if TYPE_CHECKING:
    pass


class JQueryUIMenusPage(BasePage):
    """Page object for the JQueryUI - Menu page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(JQueryUIMenusPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Navigate menu path and click final item")
    def navigate_and_click_menu_item(self, *items: str) -> None:
        """Navigate through menu hierarchy and click the final item.

        Each level waits for the next item to become visible before hovering,
        so no fixed sleeps are needed and hover state is never left to decay.
        """
        for i, item in enumerate(items):
            locator = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM, item=item)
            element = self.wait_for_visibility(locator)
            if i < len(items) - 1:
                ActionChains(self.driver.driver).move_to_element(element).perform()
            else:
                href = element.get_attribute("href")
                ActionChains(self.driver.driver).move_to_element(element).perform()
                self.driver.execute_script(
                    "var a=document.createElement('a');a.href=arguments[0];a.download='';"
                    "document.body.appendChild(a);a.click();document.body.removeChild(a);",
                    href,
                )
