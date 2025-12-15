from __future__ import annotations

from typing import TYPE_CHECKING

from pages.base.base_page import BaseCase, BasePage
from pages.features.javascript_onload_event_error.locators import JavaScriptOnloadRventErrorPageLocators

if TYPE_CHECKING:
    from logging import Logger


class JavaScriptOnloadRventErrorPage(BasePage):
    """Page object for the JavaScript onload event error page containing methods to interact with and validate
    page functionality"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(JavaScriptOnloadRventErrorPageLocators.PAGE_LOADED_INDICATOR)
