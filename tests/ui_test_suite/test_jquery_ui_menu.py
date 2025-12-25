import allure
import pytest
from parameterized import parameterized

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("JQueryUI - Menus")
@allure.sub_suite("Tests JQueryUI - Menus functionality")
class TestJQueryUIMenus(UiBaseCase):
    """Tests JQueryUI - Menus functionality"""

    ENABLED = "Enabled"
    DOWNLOADS = "Downloads"
    FILE_NAME = "menu"
    LINK_MENU_ITEMS = ["PDF", "CSV", "Excel"]
    FILES_EXTENSIONS = ["pdf", "csv", "xls"]
    EXPECTED_DOWNLOADED_FILES_COUNT = 1

    @parameterized.expand(zip(LINK_MENU_ITEMS, FILES_EXTENSIONS))
    @pytest.mark.skip(reason="Test is not yet complete")
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_jquery_ui_menus_functionality(self, link_menu_item: str, file_extension: str) -> None:
        self.logger.info("Tests JQueryUI - Menus.")
        main_page = MainPage(self)
        page = main_page.click_jquery_ui_menus_link()

        self.logger.info(".")
        page.hover_menu_item(self.ENABLED)
        self.sleep(1)
        page.hover_menu_item(self.DOWNLOADS)
        self.sleep(1)
        page.hover_menu_item(link_menu_item)
        self.sleep(1)
        page.hover_and_click_menu_item(link_menu_item)
        # page.js_open_menu_and_click(link_menu_item)
        page.wait_for_file_to_download(f"{self.FILE_NAME}.{file_extension}")

        actual_downloaded_files_count = len(page.driver.get_downloaded_files())

        self.logger.info("Verifying input number value.")
        self.assert_equal(
            self.EXPECTED_DOWNLOADED_FILES_COUNT,
            actual_downloaded_files_count,
            f"Expected '{self.EXPECTED_DOWNLOADED_FILES_COUNT}', but got '{actual_downloaded_files_count}'",
        )
