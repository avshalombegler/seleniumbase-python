"""
Module containing locators for Checkboxes page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class CheckboxesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    CHECKBOXES: Locator = {"selector": "#checkboxes input[type=checkbox]", "by": By.CSS_SELECTOR}
