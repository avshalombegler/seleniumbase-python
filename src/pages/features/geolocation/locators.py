"""
Module containing locators for Geolocation pages object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class GeolocationPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    WHERE_AM_I_BTN: Locator = {"selector": "button[onclick='getLocation()']", "by": By.CSS_SELECTOR}
    LAT_VAL: Locator = {"selector": "lat-value", "by": By.ID}
    LONG_VAL: Locator = {"selector": "long-value", "by": By.ID}
