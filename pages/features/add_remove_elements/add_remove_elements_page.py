from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.add_remove_elements.locators import AddRemoveElementsPageLocators

if TYPE_CHECKING:
    from logging import Logger


class AddRemoveElementsPage(BasePage):
    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(AddRemoveElementsPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click Add Element button")
    def click_add_element(self) -> None:
        self.logger.info("Clicking Add Element button.")
        self.click_element(AddRemoveElementsPageLocators.ADD_ELEMENT_BTN)

    @allure.step("Click Delete Element button")
    def click_delete(self) -> None:
        self.logger.info("Clicking Delete Element button.")
        self.click_element(AddRemoveElementsPageLocators.DELETE_BTN)

    def count_delete_buttons(self) -> int:
        self.logger.info("Counting Delete Element button(s).")
        return self.get_number_of_elements(AddRemoveElementsPageLocators.DELETE_BTNS)

    @allure.step("Add {count} elements")
    def add_elements(self, count: int = 1) -> None:
        for _ in range(count):
            self.click_add_element()

    @allure.step("Remove all elements")
    def remove_all_elements(self) -> None:
        while self.count_delete_buttons() > 0:
            self.click_delete()
