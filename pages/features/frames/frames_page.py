from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.frames.iframe_page import IframesPage
from pages.features.frames.locators import FramesPageLocators
from pages.features.frames.nested_frames_page import NestedFramesPage

if TYPE_CHECKING:
    pass


class FramesPage(BasePage):
    """Page object for the Frames page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(FramesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click Nested Frames link")
    def click_nested_frames_link(self) -> NestedFramesPage:
        self.click_element(FramesPageLocators.NESTED_FRAMES_LINK)
        return NestedFramesPage(self.driver)

    @allure.step("Click iFrame link")
    def click_iframe_link(self) -> IframesPage:
        self.click_element(FramesPageLocators.IFRAME_LINK)
        return IframesPage(self.driver)
