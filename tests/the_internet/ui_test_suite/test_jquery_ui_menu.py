import allure
import pytest
from parameterized import parameterized

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("JQueryUI - Menus")
class TestJQueryUIMenus(UiBaseCase):
    """Tests JQueryUI - Menus functionality"""

    ENABLED = "Enabled"
    DOWNLOADS = "Downloads"
    FILE_NAME = "menu"
    LINK_MENU_ITEMS = ["PDF", "CSV", "Excel"]
    FILES_EXTENSIONS = ["pdf", "csv", "xls"]

    @parameterized.expand(zip(LINK_MENU_ITEMS, FILES_EXTENSIONS))
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_jquery_ui_menus_functionality(self, link_menu_item: str, file_extension: str) -> None:
        self.logger.info("Tests JQueryUI - Menus.")
        main_page = MainPage(self)
        page = main_page.click_jquery_ui_menus_link()

        expected_file = f"{self.FILE_NAME}.{file_extension}"
        self.delete_downloaded_file_if_present(expected_file)

        self.logger.info(".")
        page.navigate_and_click_menu_item(self.ENABLED, self.DOWNLOADS, link_menu_item)

        page.wait_for_file_to_download(expected_file, timeout=page.long_wait)

        self.logger.info("Verifying downloaded file.")
        self.assert_downloaded_file(expected_file)
