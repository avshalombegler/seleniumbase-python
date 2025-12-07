"""
Module containing locators for Context Menu page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class ContextMenuPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}
    HOT_SPOT_BOX: Locator = {"selector": "div#hot-spot", "by": By.CSS_SELECTOR}
