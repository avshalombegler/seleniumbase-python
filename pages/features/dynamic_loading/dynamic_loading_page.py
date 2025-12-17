from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.dynamic_loading.example_1_page import Example1Page
from pages.features.dynamic_loading.example_2_page import Example2Page
from pages.features.dynamic_loading.locators import DynamicLoadingPageLocators

if TYPE_CHECKING:
    pass


class DynamicLoadingPage(BasePage):
    """Page object for the Dynamic Loading page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(DynamicLoadingPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Navigate to {page_name} page")
    def click_example_1_link(self, page_name: str = "Example 1: Element on page that is hidden") -> Example1Page:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(DynamicLoadingPageLocators.EXAMPLE_1_LINK)
        from pages.features.dynamic_loading.example_1_page import Example1Page

        return Example1Page(self.driver)

    @allure.step("Navigate to {page_name} page")
    def click_example_2_link(self, page_name: str = "Example 2: Element rendered after the fact") -> Example2Page:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(DynamicLoadingPageLocators.EXAMPLE_2_LINK)
        from pages.features.dynamic_loading.example_2_page import Example2Page

        return Example2Page(self.driver)
