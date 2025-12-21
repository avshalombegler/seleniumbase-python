from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    UnexpectedAlertPresentException,
)

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.digest_auth.locators import DigestAuthPageLocators

if TYPE_CHECKING:
    pass


class DigestAuthPage(BasePage):
    """Page object for the Digest Authentication page containing methods to test digest authentication scenarios"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)

    @allure.step("Check if login succeeded")
    def is_login_successful(self) -> bool:
        try:
            self.get_dynamic_element_text(DigestAuthPageLocators.AUTHORIZED_INDICATOR)
            return True
        except (TimeoutException, UnexpectedAlertPresentException, NoSuchElementException, Exception):
            return False
