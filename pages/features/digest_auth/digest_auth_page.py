from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    UnexpectedAlertPresentException,
)

from pages.base.base_page import BaseCase, BasePage
from pages.features.digest_auth.locators import DigestAuthPageLocators

if TYPE_CHECKING:
    from logging import Logger


class DigestAuthPage(BasePage):
    """Page object for the Digest Authentication page containing methods to test digest authentication scenarios"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)

    @allure.step("Check if login succeeded")
    def is_login_successful(self) -> bool:
        try:
            self.get_dynamic_element_text(DigestAuthPageLocators.AUTHORIZED_INDICATOR)
            return True
        except (TimeoutException, UnexpectedAlertPresentException, NoSuchElementException):
            return False

    @allure.step("Get page source for debug")
    def get_page_source_snippet(self) -> str:
        source = self.driver.page_source
        return source[:500]
