"""
Module containing locators for JQueryUI - Menu pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class JQueryUIMenusPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "h3", "by": By.CSS_SELECTOR}
    MENU_ITEM: Locator = {"selector": "{item}", "by": By.LINK_TEXT}
