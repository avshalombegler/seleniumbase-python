from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.by import By

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.large_and_deep_dom.locators import LargeAndDeepDomLocators

if TYPE_CHECKING:
    pass


class LargeAndDeepDomPage(BasePage):
    """Page object for the Large and Deep DOM page."""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(LargeAndDeepDomLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get table row count")
    def get_table_row_count(self) -> int:
        return self.get_number_of_elements({"selector": "table#large-table tbody tr", "by": By.CSS_SELECTOR})

    @allure.step("Get table column count")
    def get_table_col_count(self) -> int:
        return self.get_number_of_elements(
            {"selector": "table#large-table tbody tr:first-child td", "by": By.CSS_SELECTOR}
        )

    @allure.step("Check if last data cell is present")
    def is_last_cell_present(self) -> bool:
        return self.is_element_visible(LargeAndDeepDomLocators.LAST_DATA_CELL)

    @allure.step("Get header cell count")
    def get_header_cell_count(self) -> int:
        return self.get_number_of_elements({"selector": "table#large-table thead th", "by": By.CSS_SELECTOR})

    @allure.step("Check if first header cell is present")
    def is_first_header_present(self) -> bool:
        return self.is_element_visible(LargeAndDeepDomLocators.FIRST_HEADER)

    @allure.step("Check if last header cell is present")
    def is_last_header_present(self) -> bool:
        return self.is_element_visible(LargeAndDeepDomLocators.LAST_HEADER)
