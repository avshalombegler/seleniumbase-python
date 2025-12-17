from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.by import By

from pages.base.base_page import BaseCase, BasePage
from pages.features.checkboxes.locators import CheckboxesPageLocators

if TYPE_CHECKING:
    pass


class CheckboxesPage(BasePage):
    """Page object for the Checkboxes page containing methods to interact with and validate checkboxes."""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(CheckboxesPageLocators.PAGE_LOADED_INDICATOR)

    def _get_checkbox_locator(self, index: int) -> dict[str, str]:
        """
        Returns a locator for the checkbox at the given index (0-based).
        Example: index=0 → first checkbox, index=1 → second checkbox
        """
        # Base locator for all checkboxes
        base_locator = CheckboxesPageLocators.CHECKBOXES

        # Convert to CSS selector string
        value = base_locator["selector"]
        by = base_locator["by"]
        if by != By.CSS_SELECTOR:
            raise ValueError("Expected CSS selector for checkboxes")

        # Add :nth-of-type(index + 1) because CSS is 1-based
        dynamic_selector = f"{value}:nth-of-type({index + 1})"
        locator = {"selector": dynamic_selector, "by": By.CSS_SELECTOR}

        return locator

    @allure.step("Click checkbox {index}")
    def _click_checkbox(self, index: int) -> None:
        locator = self._get_checkbox_locator(index)
        self.click_element(locator)

    @allure.step("Check if checkbox {index} is checked")
    def is_checkbox_checked(self, index: int) -> bool:
        locator = self._get_checkbox_locator(index)
        return self.is_element_selected(locator)

    @allure.step("Set checkbox '{index}' to '{should_be_checked}'")
    def set_checkbox(self, index: int, should_be_checked: bool) -> None:
        self.logger.info(f"Set checkbox '{index}' to '{should_be_checked}'.")
        if self.is_checkbox_checked(index) != should_be_checked:
            self._click_checkbox(index)
