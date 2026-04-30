"""
Module containing locators for Drag And Drop page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class DragAndDropPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    BOX_A: Locator = {"selector": "#column-a", "by": By.CSS_SELECTOR}
    BOX_B: Locator = {"selector": "#column-b", "by": By.CSS_SELECTOR}
    BOX_HEADER: Locator = {"selector": "#column-{box} header", "by": By.CSS_SELECTOR}
