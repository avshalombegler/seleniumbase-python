"""
Module containing locators for Dynamic Content page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class DynamicContentPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}
    CONTENT_BLOCKS: Locator = {"selector": "#content > .row", "by": By.CSS_SELECTOR}
    IMAGE_IN_BLOCK: Locator = {"selector": "div#content div.large-2 img", "by": By.CSS_SELECTOR}
    TEXT_IN_BLOCK: Locator = {"selector": "div#content div.large-2 + div.large-10", "by": By.CSS_SELECTOR}
