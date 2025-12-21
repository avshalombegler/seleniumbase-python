from pathlib import Path

import allure
import pytest
from parameterized import parameterized

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Files Upload")
@allure.sub_suite("Tests Files Upload functionality")
class TestFilesUpload(UiBaseCase):
    """Tests Files Upload functionality"""

    TEST_FILES_DIR = Path(__file__).parent / "files"

    FILES_NAMES = [
        "audio-first.mp3",
        "CATE-CHAPTER_1-QUALITY.ppt",
        "Company_Portal_Installer.exe",
        "Screenshot_2025-11-16_at_9.23.28_PM.png",
        "test1.json",
        "TestingFile.pdf",
    ]

    @parameterized.expand(FILES_NAMES)
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_files_upload_functionality(self, filename: str) -> None:
        self.logger.info("Tests Files Upload.")
        main_page = MainPage(self)
        page = main_page.click_file_upload_link()

        file_path = str(self.TEST_FILES_DIR / filename)

        self.logger.info("Upload file using the Upload button.")
        page.select_file_to_upload(file_path)
        file_uploaded_page = page.click_upload_file()

        self.logger.info("Fetting uploaded filename.")
        uploaded_filename = file_uploaded_page.get_uploaded_file_name()

        self.logger.info("Verifying file uploaded sucessfully.")
        self.assert_equal(
            filename,
            uploaded_filename,
            f"Expected filename '{filename}', but got '{uploaded_filename}'",
        )
