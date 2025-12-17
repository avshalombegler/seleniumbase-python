from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.ab_testing.locators import AbTestingPageLocators

if TYPE_CHECKING:
    pass


class ABTestingPage(BasePage):
    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(AbTestingPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get title text")
    def get_title_text(self) -> str:
        return self.get_dynamic_element_text(AbTestingPageLocators.TITLE)

    @allure.step("Get paragraph text")
    def get_paragraph_text(self) -> str:
        return self.get_dynamic_element_text(AbTestingPageLocators.CONTENT_PARAGRAPH)
