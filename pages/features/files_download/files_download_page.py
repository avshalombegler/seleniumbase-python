from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.files_download.locators import FilesDownloadPageLocators

if TYPE_CHECKING:
    from logging import Logger
    from pathlib import Path


class FilesDownloadPage(BasePage):
    """Page object for the Files Download page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(FilesDownloadPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get list of downloadable files'")
    def get_list_of_downloadable_files(self) -> list[str]:
        elements = self.get_all_elements(FilesDownloadPageLocators.FILE_LINK)
        downloadable_files = []
        for elem in elements:
            href = elem.get_attribute("href")
            text = elem.text
            if href and "download" in href and text:
                downloadable_files.append(text)
        return downloadable_files

    @allure.step("Download file '{file_name}'")
    def download_file_by_filename(self, file_name: str, timeout: int = 10) -> None:
        self.download_file(FilesDownloadPageLocators.FILE_NAME_LINK, file_name, timeout=timeout)

    @allure.step("Get number of downloaded files")
    def get_number_of_downloaded_files(self, download_directory: Path) -> list:
        return self.get_files_in_directory(download_directory)
