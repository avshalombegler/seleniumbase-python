"""
Module containing locators for Digest Auth page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class DigestAuthPageLocators:
    AUTHORIZED_INDICATOR: Locator = {"selector": "div#content p", "by": By.CSS_SELECTOR}
