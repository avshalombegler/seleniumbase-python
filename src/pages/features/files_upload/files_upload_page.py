from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.files_upload.file_uploaded_page import FileUploadedPage
from src.pages.features.files_upload.locators import FilesUploadPageLocators

if TYPE_CHECKING:
    pass


class FileUploadPage(BasePage):
    """Page object for the Files Upload page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(FilesUploadPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Select file '{file_path}' to upload")
    def select_file_to_upload(self, file_path: str) -> None:
        self.send_keys_to_element(FilesUploadPageLocators.FILE_UPLOAD, file_path)

    @allure.step("Click Upload button - return File Uploaded Page object")
    def click_upload_file(self) -> FileUploadedPage:
        self.click_element(FilesUploadPageLocators.UPLOAD_BTN)
        return FileUploadedPage(self.driver)
