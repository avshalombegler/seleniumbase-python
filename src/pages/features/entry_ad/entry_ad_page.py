from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.entry_ad.locators import EntryAdPageLocators

if TYPE_CHECKING:
    pass


class EntryAdPage(BasePage):
    """Page object for the Entry Ad page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(EntryAdPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click close window")
    def click_close_modal(self) -> None:
        self.click_element(EntryAdPageLocators.CLOSE_BTN)

    @allure.step("Check modal window display")
    def is_modal_displayed(self) -> bool:
        return self.is_element_visible(EntryAdPageLocators.MODAL_LOADED_INDICATOR, timeout=5)

    # click using JS - currently does not work
    # @allure.step("Click re-enable it link")
    # def click_re_enable_link(self) -> None:
    #     def action() -> None:
    #         link = self._safe_wait(EC.element_to_be_clickable, EntryAdPageLocators.RE_ENABLE_LINK)
    #         self.driver.execute_script("arguments[0].click();", link)
    #         self.logger.info("Re-enable link clicked via JS.")

    #     self._retry(action, locator=EntryAdPageLocators.RE_ENABLE_LINK, retry_count=3)
