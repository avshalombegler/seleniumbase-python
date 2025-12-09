from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.files_download.locators import FilesDownloadPageLocators

if TYPE_CHECKING:
    from logging import Logger


class FilesDownloadPage(BasePage):
    """Page object for the Files Download page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        self.wait_for_page_to_load(FilesDownloadPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get list of files links")
    def get_list_of_files_links(self) -> list[str]:
        elements = self.get_all_elements(FilesDownloadPageLocators.FILE_LINK)
        return [elem.get_attribute("href") for elem in elements]

    @allure.step("Get list of files links")
    def download_files(self, files_links, dest_folder) -> None:
        for link in files_links:
            self.driver.download_file(link, dest_folder)
