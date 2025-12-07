"""
Module containing locators for Files Download page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class FilesDownloadPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    FILE_LINK: Locator = {"selector": ".example a", "by": By.CSS_SELECTOR}
    FILE_NAME_LINK: Locator = {"selector": "{file_name}", "by": By.LINK_TEXT}
