from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.frames.locators import NestedFramesPageLocators

if TYPE_CHECKING:
    pass


class NestedFramesPage(BasePage):
    """Page object for the Nested Frames page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(NestedFramesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Switch to frame '{value}'")
    def switch_frame(self, value: str) -> None:
        locator = self.format_locator(NestedFramesPageLocators.NESTED_FRAME, value=value)
        self.switch_to_frame(locator)

    @allure.step("Get frame text")
    def get_frame_text(self) -> str:
        return self.get_dynamic_element_text(NestedFramesPageLocators.NESTED_FRAME_BODY)
