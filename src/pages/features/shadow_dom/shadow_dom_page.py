from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.shadow_dom.locators import ShadowDomLocators

if TYPE_CHECKING:
    pass


class ShadowDomPage(BasePage):
    """Page object for the Shadow DOM page containing methods to interact with and validate Shadow DOM functionality."""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(ShadowDomLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get heading text")
    def get_heading_text(self) -> str:
        return self.get_dynamic_element_text(ShadowDomLocators.HEADING)

    @allure.step("Get shadow slot text")
    def get_shadow_slot_text(self) -> str:
        return self.driver.execute_script(
            "return document.querySelector('my-paragraph')."
            "shadowRoot.querySelector('slot').assignedNodes()[0].textContent.trim();"
        )

    @allure.step("Get shadow default text")
    def get_shadow_default_text(self) -> str:
        return self.driver.execute_script(
            "var nodes = document.querySelector('my-paragraph')."
            "shadowRoot.querySelector('slot').assignedNodes();"
            " if (nodes.length > 0) { return nodes[0].textContent.trim(); }"
            " var p = document.querySelector('my-paragraph > p');"
            " return p ? p.textContent.trim() : '';"
        )
