"""
Module containing locators for Inputs pages object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class InputsPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "h3", "by": By.CSS_SELECTOR}
    INPUT_NUMBER: Locator = {"selector": "input[type=number]", "by": By.CSS_SELECTOR}
