"""
Module containing locators for Form Authentication page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class FormAuthenticationPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h2", "by": By.CSS_SELECTOR}
    USERNAME_TEXTBOX: Locator = {"selector": "username", "by": By.ID}
    PASSWORD_TEXTBOX: Locator = {"selector": "password", "by": By.ID}
    LOGIN_BTN: Locator = {"selector": "button[type=submit]", "by": By.CSS_SELECTOR}
    FLASH_MSG: Locator = {"selector": "flash", "by": By.ID}


class SecureAreaPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h2", "by": By.CSS_SELECTOR}
    LOGOUT_BTN: Locator = {"selector": "a[href='/logout']", "by": By.CSS_SELECTOR}
    FLASH_MSG: Locator = {"selector": "flash", "by": By.ID}
