from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.files_upload.locators import FileUploadedPageLocators

if TYPE_CHECKING:
    from logging import Logger


class FileUploadedPage(BasePage):
    """Page object for the File Uploaded page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(FileUploadedPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get uploaded file name")
    def get_uploaded_file_name(self) -> str:
        return self.get_dynamic_element_text(FileUploadedPageLocators.UPLOADED_FILE)
