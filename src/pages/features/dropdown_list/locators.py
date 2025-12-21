"""
Module containing locators for Dropdown List page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class DropdownListPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}
    DROPDOWN: Locator = {"selector": "select#dropdown", "by": By.CSS_SELECTOR}
