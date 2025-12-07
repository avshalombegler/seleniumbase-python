"""
Module containing locators for Broken Images page object.
"""

from selenium.webdriver.common.by import By

from pages.base.base_page import Locator


class BrokenImagesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}
    IMAGES: Locator = {"selector": "div.example img", "by": By.CSS_SELECTOR}
    IMAGE: Locator = {"selector": "{tag}[src$='{image_name}']", "by": By.CSS_SELECTOR}
