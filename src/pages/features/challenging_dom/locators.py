"""
Module containing locators for Challenging DOM page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class ChallengingDomPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    BLUE_BTN: Locator = {"selector": "a.button:not(.alert):not(.success)", "by": By.CSS_SELECTOR}
    RED_BTN: Locator = {"selector": "a.button.alert", "by": By.CSS_SELECTOR}
    GREEN_BTN: Locator = {"selector": "a.button.success", "by": By.CSS_SELECTOR}
    EDIT_BTN: Locator = {"selector": "//tbody//tr[{row_num}]//a[text()='edit']", "by": By.XPATH}
    DEL_BTN: Locator = {"selector": "//tbody//tr[{row_num}]//a[text()='delete']", "by": By.XPATH}
    TABLE_HEADERS_TEXT: Locator = {"selector": ".example thead th", "by": By.CSS_SELECTOR}
    TABLE_HEAD_TEXT: Locator = {"selector": "//th[text()='{column_name}']", "by": By.XPATH}
    TABLE_CELL_TEXT: Locator = {
        "selector": "//th[text()='{column_name}']/ancestor::thead/following::tr//td[text()='{cell_value}']",
        "by": By.XPATH,
    }
    TD: Locator = {
        "selector": "//table//td[{index}][normalize-space()='{cell}']",
        "by": By.XPATH,
    }
