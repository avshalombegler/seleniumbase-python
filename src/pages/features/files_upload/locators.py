"""
Module containing locators for Files Upload page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class FilesUploadPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    FILE_UPLOAD: Locator = {"selector": "file-upload", "by": By.ID}
    UPLOAD_BTN: Locator = {"selector": "file-submit", "by": By.ID}
    UPLOAD_BOX: Locator = {"selector": "div[id=drag-drop-upload]", "by": By.CSS_SELECTOR}


class FileUploadedPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    UPLOADED_FILE: Locator = {"selector": "uploaded-files", "by": By.ID}
