"""
Module containing locators for Key Presses pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class KeyPressesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "h3", "by": By.CSS_SELECTOR}
    TEXT_INPUT: Locator = {"selector": "input#target", "by": By.CSS_SELECTOR}
    RESULT: Locator = {"selector": "p#result", "by": By.CSS_SELECTOR}
