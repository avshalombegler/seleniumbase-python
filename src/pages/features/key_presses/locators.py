"""
Module containing locators for Key Presses pages object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class KeyPressesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "h3", "by": By.CSS_SELECTOR}
    TEXT_INPUT: Locator = {"selector": "#target", "by": By.CSS_SELECTOR}
    RESULT: Locator = {"selector": "#result", "by": By.CSS_SELECTOR}
