"""
Module containing locators for Multiple Windows page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class MultipleWindowsLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "a[href='/windows/new']", "by": By.CSS_SELECTOR}
    OPEN_NEW_WINDOW_LINK: Locator = {"selector": "a[href='/windows/new']", "by": By.CSS_SELECTOR}
    PAGE_HEADING: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
