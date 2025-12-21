"""
Module containing locators for Basic Auth page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class BasicAuthPageLocators:
    AUTHORIZED_INDICATOR: Locator = {"selector": "div#content p", "by": By.CSS_SELECTOR}
