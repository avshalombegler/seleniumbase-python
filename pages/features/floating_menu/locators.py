"""
Module containing locators for Floating Menu page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class FloatingMenuPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    MENU_ITEM: Locator = {"selector": "{item}", "by": By.LINK_TEXT}
