from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.windows.locators import MultipleWindowsLocators

if TYPE_CHECKING:
    pass


class MultipleWindowsPage(BasePage):
    """Page object for the Multiple Windows page containing methods to interact with and validate window functionality."""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(MultipleWindowsLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click open new window link")
    def click_open_new_window(self) -> None:
        self.click_element(MultipleWindowsLocators.OPEN_NEW_WINDOW_LINK)

    @allure.step("Get all window handles")
    def get_window_handles(self) -> list[str]:
        return self.driver.driver.window_handles

    @allure.step("Switch to window '{handle}'")
    def switch_to_window(self, handle: str) -> None:
        self.driver.driver.switch_to.window(handle)

    @allure.step("Get page heading")
    def get_page_heading(self) -> str:
        return self.get_dynamic_element_text(MultipleWindowsLocators.PAGE_HEADING)
