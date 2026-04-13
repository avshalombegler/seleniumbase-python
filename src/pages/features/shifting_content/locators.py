"""
Module containing locators for Shifting Content page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class ShiftingContentLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    EXAMPLE_1_LINK: Locator = {"selector": "a[href='/shifting_content/menu']", "by": By.CSS_SELECTOR}
    EXAMPLE_2_LINK: Locator = {"selector": "a[href='/shifting_content/image']", "by": By.CSS_SELECTOR}
    EXAMPLE_3_LINK: Locator = {"selector": "a[href='/shifting_content/list']", "by": By.CSS_SELECTOR}
    MENU_CONTAINER: Locator = {"selector": ".example ul", "by": By.CSS_SELECTOR}
    IMAGE_ELEMENT: Locator = {"selector": ".example img", "by": By.CSS_SELECTOR}
    LIST_CONTAINER: Locator = {"selector": ".example .row", "by": By.CSS_SELECTOR}
