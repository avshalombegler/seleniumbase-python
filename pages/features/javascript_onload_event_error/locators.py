"""
Module containing locators for JavaScript onload event error pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class JavaScriptOnloadRventErrorPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "p", "by": By.CSS_SELECTOR}
