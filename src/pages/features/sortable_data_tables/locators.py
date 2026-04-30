"""
Module containing locators for Sortable Data Tables page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class SortableDataTablesLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}
    TABLE1: Locator = {"selector": "table1", "by": By.ID}
    TABLE2: Locator = {"selector": "table2", "by": By.ID}
    TABLE1_HEADERS: Locator = {"selector": "#table1 thead th", "by": By.CSS_SELECTOR}
    TABLE2_HEADERS: Locator = {"selector": "#table2 thead th", "by": By.CSS_SELECTOR}
    TABLE1_ROWS: Locator = {"selector": "#table1 tbody tr", "by": By.CSS_SELECTOR}
    TABLE2_ROWS: Locator = {"selector": "#table2 tbody tr", "by": By.CSS_SELECTOR}
    TABLE1_HEADER_LAST_NAME: Locator = {
        "selector": "//table[@id='table1']//th[normalize-space()='Last Name']",
        "by": By.XPATH,
    }
    TABLE1_HEADER_DUE: Locator = {"selector": "//table[@id='table1']//th[normalize-space()='Due']", "by": By.XPATH}
    TABLE2_HEADER_LAST_NAME: Locator = {
        "selector": "//table[@id='table2']//th[normalize-space()='Last Name']",
        "by": By.XPATH,
    }
    TABLE2_HEADER_DUE: Locator = {"selector": "//table[@id='table2']//th[normalize-space()='Due']", "by": By.XPATH}
    TABLE1_FIRST_ROW_LAST_NAME: Locator = {
        "selector": "#table1 tbody tr:first-child td:first-child",
        "by": By.CSS_SELECTOR,
    }
    TABLE2_FIRST_ROW_LAST_NAME: Locator = {
        "selector": "#table2 tbody tr:first-child td.last-name",
        "by": By.CSS_SELECTOR,
    }
    TABLE2_FIRST_ROW_DUE: Locator = {"selector": "#table2 tbody tr:first-child td.dues", "by": By.CSS_SELECTOR}
    TABLE1_SORT_INDICATOR_LAST_NAME: Locator = {
        "selector": "#table1 thead th:nth-child(1).headerSortDown, #table1 thead th:nth-child(1).headerSortUp",
        "by": By.CSS_SELECTOR,
    }
    TABLE2_SORT_INDICATOR_DUE: Locator = {
        "selector": "#table2 thead th:nth-child(4).headerSortDown, #table2 thead th:nth-child(4).headerSortUp",
        "by": By.CSS_SELECTOR,
    }
