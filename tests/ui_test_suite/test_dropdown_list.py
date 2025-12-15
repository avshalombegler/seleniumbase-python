import allure
import pytest
from parameterized import parameterized

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Dropdown List")
@allure.sub_suite("Tests Dropdown List functionality")
class TestDropdownList(UiBaseCase):
    """Tests Dropdown List functionality"""

    OPTIONS = [["Option 1"], ["Option 2"]]

    @parameterized.expand(OPTIONS)
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_dropdown_list_functionality(self, option: str) -> None:
        self.logger.info("Tests Dropdown List functionality.")
        main_page = MainPage(self)
        page = main_page.click_dropdown_list_link()

        self.logger.info(f"Selecting option '{option}' from dropdown.")
        page.select_dropdown_option(option)

        self.logger.info(f"Verifying option '{option}' selected.")
        assert page.get_is_option_selected(option), f"Expected '{option}' to be selected, but it's not"
