from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.shifting_content.locators import ShiftingContentLocators

if TYPE_CHECKING:
    pass


class ShiftingContentPage(BasePage):
    """Page object for the Shifting Content page containing methods to interact with and validate page functionality."""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(ShiftingContentLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get heading text")
    def get_heading_text(self) -> str:
        return self.get_dynamic_element_text(ShiftingContentLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click menu example link")
    def click_menu_example_link(self) -> None:
        self.click_element(ShiftingContentLocators.EXAMPLE_1_LINK)

    @allure.step("Click image example link")
    def click_image_example_link(self) -> None:
        self.click_element(ShiftingContentLocators.EXAMPLE_2_LINK)

    @allure.step("Click list example link")
    def click_list_example_link(self) -> None:
        self.click_element(ShiftingContentLocators.EXAMPLE_3_LINK)

    @allure.step("Check if menu container is visible")
    def is_menu_container_visible(self) -> bool:
        return self.is_element_visible(ShiftingContentLocators.MENU_CONTAINER)

    @allure.step("Check if image is visible")
    def is_image_visible(self) -> bool:
        return self.is_element_visible(ShiftingContentLocators.IMAGE_ELEMENT)

    @allure.step("Check if list is visible")
    def is_list_visible(self) -> bool:
        return self.is_element_visible(ShiftingContentLocators.LIST_CONTAINER)
