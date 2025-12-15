"""
Module containing locators for JavaScript Alerts pages object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class JavaScriptAlertsPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "h3", "by": By.CSS_SELECTOR}
    JS_ALERTS_BTN: Locator = {"selector": "button[onclick='jsAlert()'", "by": By.CSS_SELECTOR}
    JS_CONFIRM_BTN: Locator = {"selector": "button[onclick='jsConfirm()'", "by": By.CSS_SELECTOR}
    JS_PROMPT_BTN: Locator = {"selector": "button[onclick='jsPrompt()'", "by": By.CSS_SELECTOR}
    RESULT: Locator = {"selector": "p#result", "by": By.CSS_SELECTOR}
