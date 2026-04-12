"""
Module containing locators for Redirect Link page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class RedirectLinkLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    REDIRECT_HERE_LINK: Locator = {"selector": "redirect", "by": By.ID}
