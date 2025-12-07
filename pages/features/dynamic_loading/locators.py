"""
Module containing locators for Dynamic Loading page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class DynamicLoadingPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    EXAMPLE_1_LINK: Locator = {"selector": "Example 1: Element on page that is hidden", "by": By.LINK_TEXT}
    EXAMPLE_2_LINK: Locator = {"selector": "Example 2: Element rendered after the fact", "by": By.LINK_TEXT}


class Example1PageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h4", "by": By.CSS_SELECTOR}
    START_BTN: Locator = {"selector": "div#start > button", "by": By.CSS_SELECTOR}
    WAIT_LOADER: Locator = {"selector": "div#loading", "by": By.CSS_SELECTOR}
    SUCCESS_MSG: Locator = {"selector": "div#finish > h4", "by": By.CSS_SELECTOR}


class Example2PageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h4", "by": By.CSS_SELECTOR}
    START_BTN: Locator = {"selector": "div#start > button", "by": By.CSS_SELECTOR}
    WAIT_LOADER: Locator = {"selector": "div#loading", "by": By.CSS_SELECTOR}
    SUCCESS_MSG: Locator = {"selector": "div#finish > h4", "by": By.CSS_SELECTOR}
