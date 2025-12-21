"""
Module containing locators for Hovers pages object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class HoversPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    FIGURE: Locator = {"selector": "div.figure:nth-of-type({index})", "by": By.CSS_SELECTOR}
    NAME: Locator = {"selector": "div.figure:nth-of-type({index}) > .figcaption > h5", "by": By.CSS_SELECTOR}
    VIEW_PROFILE_BTN: Locator = {"selector": "div.figure:nth-of-type({index}) > .figcaption > a", "by": By.CSS_SELECTOR}


class HoversUserPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "h1", "by": By.CSS_SELECTOR}
