"""
Module containing locators for Frames pages object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class FramesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    NESTED_FRAMES_LINK: Locator = {"selector": "Nested Frames", "by": By.LINK_TEXT}
    IFRAME_LINK: Locator = {"selector": "iFrame", "by": By.LINK_TEXT}


class NestedFramesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "frameset", "by": By.CSS_SELECTOR}
    NESTED_FRAME: Locator = {"selector": "frame[name='frame-{value}']", "by": By.CSS_SELECTOR}
    NESTED_FRAME_BODY: Locator = {"selector": "body", "by": By.TAG_NAME}


class IframesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
    IFRAME: Locator = {"selector": ".tox-edit-area__iframe", "by": By.CSS_SELECTOR}
    RICH_TEXT_AREA: Locator = {"selector": "#tinymce > p", "by": By.CSS_SELECTOR}
