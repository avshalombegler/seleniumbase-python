"""
Module containing locators for Horizontal Slider pages object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class HorizontalSliderPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    SLIDER: Locator = {"selector": "input[type=range]", "by": By.CSS_SELECTOR}
    SLIDER_VALUE: Locator = {"selector": "range", "by": By.ID}
