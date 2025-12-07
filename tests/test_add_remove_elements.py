import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("Add/Remove Elements")
@allure.story("Verify adding and removing elements on the page")
class TestAddRemoveElements(UiBaseCase):
    """Tests for add/remove elements page functionality"""

    # @pytest.mark.full
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_elements(self) -> None:
        self.logger.info("Tests for add elements.")
        main_page = MainPage(self)
        page = main_page.click_add_remove_elements_link()

        self.logger.info("Add two elements.")
        page.add_elements(2)
        count = page.count_delete_buttons()
        self.logger.info(f"Found {count} delete buttons.")
        assert count == 2, f"Expected 2 delete buttons, got {count}"

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_elements(self) -> None:
        self.logger.info("Tests for remove elements.")
        main_page = MainPage(self)
        page = main_page.click_add_remove_elements_link()

        self.logger.info("Ensure there are elements to remove")
        page.add_elements(2)

        self.logger.info("Remove all elements")
        page.remove_all_elements()
        count = page.count_delete_buttons()
        self.logger.info(f"Found {count} delete buttons.")
        assert count == 0, f"Expected 0 delete buttons, got {count}"
