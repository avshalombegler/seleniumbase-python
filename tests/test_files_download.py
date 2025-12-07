import os

import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("Files Download")
@allure.story("Tests Files Download functionality")
class TestFilesDownload(UiBaseCase):
    """Tests Files Download functionality"""

    @pytest.mark.xfail(reason="One file link is broken")
    @pytest.mark.full
    @pytest.mark.ui
    @pytest.mark.clean_downloads
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skipif(
        os.getenv("BROWSER") == "firefox",
        reason="Skipping file download test for Firefox due to slow downloading process",
    )
    def test_files_download_functionality(self, downloads_directory) -> None:
        self.logger.info("Tests Files Download.")
        main_page = MainPage(self)
        page = main_page.click_file_download_link()

        self.logger.info("Getting list of downloadable files.")
        file_names = page.get_list_of_downloadable_files()

        self.logger.info("Downloading all files in page.")
        for file_name in file_names:
            page.download_file_by_filename(file_name)

        self.logger.info("Verifying downloaded files count equals to files in page.")
        assert len(file_names) == len(page.get_number_of_downloaded_files(downloads_directory))
