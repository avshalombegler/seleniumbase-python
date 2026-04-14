from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.sortable_data_tables.locators import SortableDataTablesLocators

if TYPE_CHECKING:
    pass


class SortableDataTablesPage(BasePage):
    """
    Page object for the Sortable Data Tables page containing methods to interact with and validate table functionality.
    """

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(SortableDataTablesLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get heading text")
    def get_heading_text(self) -> str:
        return self.get_dynamic_element_text(SortableDataTablesLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get table1 row count")
    def get_table1_row_count(self) -> int:
        return self.get_number_of_elements(SortableDataTablesLocators.TABLE1_ROWS)

    @allure.step("Get table2 row count")
    def get_table2_row_count(self) -> int:
        return self.get_number_of_elements(SortableDataTablesLocators.TABLE2_ROWS)

    @allure.step("Get table1 header count")
    def get_table1_header_count(self) -> int:
        return self.get_number_of_elements(SortableDataTablesLocators.TABLE1_HEADERS)

    @allure.step("Get table2 header count")
    def get_table2_header_count(self) -> int:
        return self.get_number_of_elements(SortableDataTablesLocators.TABLE2_HEADERS)

    @allure.step("Get table1 first row last name")
    def get_table1_first_row_last_name(self) -> str:
        return self.get_dynamic_element_text(SortableDataTablesLocators.TABLE1_FIRST_ROW_LAST_NAME)

    @allure.step("Get table2 first row last name")
    def get_table2_first_row_last_name(self) -> str:
        return self.get_dynamic_element_text(SortableDataTablesLocators.TABLE2_FIRST_ROW_LAST_NAME)

    @allure.step("Get table2 first row due")
    def get_table2_first_row_due(self) -> str:
        return self.get_dynamic_element_text(SortableDataTablesLocators.TABLE2_FIRST_ROW_DUE)

    @allure.step("Click table1 Last Name header")
    def click_table1_last_name_header(self) -> None:
        self.click_element(SortableDataTablesLocators.TABLE1_HEADER_LAST_NAME)

    @allure.step("Click table1 Due header")
    def click_table1_due_header(self) -> None:
        self.click_element(SortableDataTablesLocators.TABLE1_HEADER_DUE)

    @allure.step("Click table2 Last Name header")
    def click_table2_last_name_header(self) -> None:
        self.click_element(SortableDataTablesLocators.TABLE2_HEADER_LAST_NAME)

    @allure.step("Click table2 Due header")
    def click_table2_due_header(self) -> None:
        self.click_element(SortableDataTablesLocators.TABLE2_HEADER_DUE)

    @allure.step("Check if table1 Last Name header is sorted")
    def is_table1_last_name_header_sorted(self) -> bool:
        classes = self.get_element_attr(SortableDataTablesLocators.TABLE1_HEADER_LAST_NAME, "class") or ""
        return "headerSortDown" in classes or "headerSortUp" in classes

    @allure.step("Check if table2 Due header is sorted")
    def is_table2_due_header_sorted(self) -> bool:
        classes = self.get_element_attr(SortableDataTablesLocators.TABLE2_HEADER_DUE, "class") or ""
        return "headerSortDown" in classes or "headerSortUp" in classes

    @allure.step("Get all table1 Last Name values")
    def get_all_table1_last_name_values(self) -> list[str]:
        rows = self.get_all_elements(SortableDataTablesLocators.TABLE1_ROWS)
        return [row.text for row in rows]

    @allure.step("Get all table2 Due values")
    def get_all_table2_due_values(self) -> list[str]:
        rows = self.get_all_elements(SortableDataTablesLocators.TABLE2_ROWS)
        return [row.text for row in rows]
