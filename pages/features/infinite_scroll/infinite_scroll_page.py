from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.infinite_scroll.locators import InfiniteScrollPageLocators

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
        self.driver.scroll_down(100)
        sleep(1)
