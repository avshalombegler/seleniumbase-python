from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.redirect_link.locators import RedirectLinkLocators

if TYPE_CHECKING:
    pass


class RedirectLinkPage(BasePage):
    """
    Page object for the Redirect Link page containing methods to interact with and validate redirect functionality.
    """

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(RedirectLinkLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get heading text")
    def get_heading_text(self) -> str:
        return self.get_dynamic_element_text(RedirectLinkLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click redirect here link")
    def click_redirect_here(self) -> None:
        self.click_element(RedirectLinkLocators.REDIRECT_HERE_LINK)
