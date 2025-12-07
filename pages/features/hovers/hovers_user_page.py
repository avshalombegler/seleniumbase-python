from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.hovers.locators import HoversUserPageLocators

if TYPE_CHECKING:
    from logging import Logger


class HoversUserPage(BasePage):
    """Page object for the Hovers page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(HoversUserPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get current browser url")
    def get_current_browser_url(self) -> str:
        return self.get_current_url()

    @allure.step("Navigate back")
    def navigate_back_page(self) -> None:
        self.navigate_back()
