"""
Module containing locators for Notification Messages page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class NotificationMessagesLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    CLICK_HERE_LINK: Locator = {"selector": "a[href='/notification_message']", "by": By.CSS_SELECTOR}
    FLASH_MESSAGE: Locator = {"selector": "flash", "by": By.ID}
    FLASH_CLOSE_BUTTON: Locator = {"selector": "#flash a.close", "by": By.CSS_SELECTOR}
