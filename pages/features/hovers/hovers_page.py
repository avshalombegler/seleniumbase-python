from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.hovers.hovers_user_page import HoversUserPage
from pages.features.hovers.locators import HoversPageLocators

if TYPE_CHECKING:
    from logging import Logger


class HoversPage(BasePage):
    """Page object for the Hovers page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(HoversPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Hover mouse over profile image")
    def hover_mouse_over_profile_image(self, index: int) -> None:
        locator = self.format_locator(HoversPageLocators.FIGURE, index=index)
        self.driver.hover(**locator)

    @allure.step("Get user name text")
    def get_user_name_text(self, index: int) -> str:
        locator = self.format_locator(HoversPageLocators.NAME, index=index)
        return self.get_dynamic_element_text(locator)

    @allure.step("Click view profile link")
    def click_view_profile_link(self, index: int) -> HoversUserPage:
        locator = self.format_locator(HoversPageLocators.VIEW_PROFILE_BTN, index=index)
        self.click_element(locator)
        return HoversUserPage(self.driver, self.logger)
