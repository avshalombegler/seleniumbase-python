"""
Module containing locators for Infinite Scroll pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class InfiniteScrollPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
