"""
Module containing locators for AB Testing page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class AbTestingPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}
    TITLE: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}
    CONTENT_PARAGRAPH: Locator = {"selector": "div#content p", "by": By.CSS_SELECTOR}
