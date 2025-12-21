"""
Module containing locators for Exit Intent page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class ExitIntentPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    PAGE_BODY: Locator = {"selector": "body", "by": By.TAG_NAME}
    MODAL_LOADED_INDICATOR: Locator = {"selector": ".modal-title h3", "by": By.CSS_SELECTOR}
    CLOSE_BTN: Locator = {"selector": "div.modal-footer p", "by": By.CSS_SELECTOR}
