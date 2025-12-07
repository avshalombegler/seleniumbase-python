"""
Module containing locators for Dynamic Controls page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class DynamicControlsPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h4", "by": By.CSS_SELECTOR}
    WAIT_LOADER: Locator = {"selector": "#loading", "by": By.CSS_SELECTOR}

    A_CHECKBOX: Locator = {"selector": "input[type=checkbox]", "by": By.CSS_SELECTOR}
    REMOVE_BTN: Locator = {"selector": "//button[text()='Remove']", "by": By.XPATH}
    ADD_BTN: Locator = {"selector": "//button[text()='Add']", "by": By.XPATH}
    REMOVE_ADD_MSG: Locator = {"selector": "#checkbox-example #message", "by": By.CSS_SELECTOR}

    TEXTBOX: Locator = {"selector": "input[type=text]", "by": By.CSS_SELECTOR}
    ENABLE_BTN: Locator = {"selector": "//button[text()='Enable']", "by": By.XPATH}
    DISABLE_BTN: Locator = {"selector": "//button[text()='Disable']", "by": By.XPATH}
    ENABLE_DISABLE_MSG: Locator = {"selector": "#input-example #message", "by": By.CSS_SELECTOR}
