"""
Module containing locators for Shadow DOM page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class ShadowDomLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "my-paragraph", "by": By.CSS_SELECTOR}
    HEADING: Locator = {"selector": "#content h1", "by": By.CSS_SELECTOR}
