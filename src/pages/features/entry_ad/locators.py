"""
Module containing locators for Entry Ad page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class EntryAdPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    MODAL_LOADED_INDICATOR: Locator = {"selector": ".modal-title h3", "by": By.CSS_SELECTOR}
    CLOSE_BTN: Locator = {"selector": "div.modal-footer p", "by": By.CSS_SELECTOR}
    RE_ENABLE_LINK: Locator = {"selector": "click here", "by": By.LINK_TEXT}
