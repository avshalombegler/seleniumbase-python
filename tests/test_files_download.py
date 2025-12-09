import os

import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("Files Download")
@allure.story("Tests Files Download functionality")
class TestFilesDownload(UiBaseCase):
    """Tests Files Download functionality"""

    # @pytest.mark.xfail(reason="One file link is broken")
    # @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skipif(
        os.getenv("BROWSER") == "firefox",
        reason="Skipping file download test for Firefox due to slow downloading process",
    )
    def test_files_download_functionality(self) -> None:
        self.logger.info("Tests Files Download.")

        main_page = MainPage(self)
        page = main_page.click_file_download_link()

        self.logger.info("Getting list of downloadable files.")
        files_links = page.get_list_of_files_links()

        self.logger.info("Downloading all files in page.")
        page.download_files(files_links, self.get_downloads_folder())

        downloaded_files = self.get_downloaded_files()

        self.logger.info("Verifying downloaded files count equals to files in page.")
        files_links_count = len(files_links)
        downloaded_files_count = len(downloaded_files)
        self.logger.info(f"Expected count: {files_links_count}")
        self.logger.info(f"Downloaded count: {downloaded_files_count}")

        assert files_links_count == downloaded_files_count, (
            f"Expected files count '{files_links_count}', but got '{downloaded_files_count}' files. "
            f"Missing files: {[set(f.split('/')[-1] for f in files_links) - set(downloaded_files)]}"
        )
