from __future__ import annotations

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

    @allure.step("Hover over menu item '{item}'")
    def hover_menu_item(self, item: str) -> None:
        locator = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM, item=item)
        self.driver.hover(**locator)

    # @allure.step("Click menu item '{item}'")
    # def hover_and_click_menu_item(self, item: str) -> None:
    #     xpath = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM_XPATH, item=item)
    #     menu_item_elem = self.wait_for_visibility(xpath)
    #     element_size = menu_item_elem.size
    #     width = 2
    #     height = element_size["height"] / 2

    #     self.actions.move_to_element_with_offset(menu_item_elem, width, height).click().perform()

    # @allure.step("Click menu item '{item}'")
    # def hover_and_click_menu_item(self, downloads: str, item: str) -> None:
    #     downloads_locator = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM, item=downloads)
    #     menu_item_locator = self.format_locator(JQueryUIMenusPageLocators.MENU_ITEM, item=item)

    #     self.driver.hover_and_click(
    #         hover_selector=downloads_locator["selector"],
    #         click_selector=menu_item_locator["selector"],
    #         hover_by=downloads_locator["by"],
    #         click_by=menu_item_locator["by"],
    #     )

    # def js_open_menu_and_click(self, item_text: str) -> None:
    #     """ """
    #     script = f"""
    #     var item = $("ul#menu a:contains('{item_text}')").filter(function() {{
    #         return $(this).text().trim() === '{item_text}';
    #     }});

    #     if (item.length === 0) {{
    #         throw new Error("Menu item '{item_text}' not found");
    #     }}

    #     item.parents('li').trigger('mouseenter');

    #     item.trigger('focus').trigger('mouseenter');

    #     setTimeout(function() {{
    #         item.trigger('click');
    #     }}, 300);
    #     """
    #     self.driver.execute_script(script)
