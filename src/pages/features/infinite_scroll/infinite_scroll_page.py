from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.infinite_scroll.locators import InfiniteScrollPageLocators

if TYPE_CHECKING:
    pass


class InfiniteScrollPage(BasePage):
    """Page object for the Infinite Scroll page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(InfiniteScrollPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get page height")
    def get_page_height(self) -> int:
        return self.driver.execute_script("return document.body.scrollHeight")

    @allure.step("Scroll to bottom of page")
    def scroll_to_bottom_of_page(self) -> None:
        old_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.scroll_down(100)
        self.driver.execute_async_script(
            """
            var callback = arguments[arguments.length - 1];
            var old_height = arguments[0];
            var start = Date.now();
            var interval = setInterval(function() {
                if (document.body.scrollHeight > old_height || Date.now() - start > 10000) {
                    clearInterval(interval);
                    callback();
                }
            }, 200);
            """,
            old_height,
        )
