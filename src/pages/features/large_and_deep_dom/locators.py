"""
Module containing locators for Large and Deep DOM page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class LargeAndDeepDomLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "large-table", "by": By.ID}
    TABLE: Locator = {"selector": "large-table", "by": By.ID}
    FIRST_HEADER: Locator = {"selector": "header-1", "by": By.ID}
    LAST_HEADER: Locator = {"selector": "header-50", "by": By.ID}
    FIRST_DATA_ROW: Locator = {"selector": "#large-table tbody tr:first-child", "by": By.CSS_SELECTOR}
    FIRST_DATA_CELL: Locator = {
        "selector": "#large-table tbody tr:first-child td:first-child",
        "by": By.CSS_SELECTOR,
    }
    LAST_DATA_CELL: Locator = {
        "selector": "#large-table tbody tr:last-child td:last-child",
        "by": By.CSS_SELECTOR,
    }
