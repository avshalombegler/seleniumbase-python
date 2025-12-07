"""
Module containing locators for Add Remove Elements page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class AddRemoveElementsPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div#content h3", "by": By.CSS_SELECTOR}
    ADD_ELEMENT_BTN: Locator = {"selector": ".example > button", "by": By.CSS_SELECTOR}
    DELETE_BTN: Locator = {"selector": "#elements > button:first-child", "by": By.CSS_SELECTOR}
    DELETE_BTNS: Locator = {"selector": "#elements > button", "by": By.CSS_SELECTOR}
