import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Checkboxes")
@allure.sub_suite("Verify Checkboxes interactions")
class TestCheckboxes(UiBaseCase):
    """Test for verifying checkbox functionality"""

    CHECKBOX_INDEX_0 = 0
    CHECKBOX_INDEX_1 = 1

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkboxes_functionality(self) -> None:
        self.logger.info("Test for verifying checkbox functionality.")
        main_page = MainPage(self)
        page = main_page.click_checkboxes_link()

        self.logger.info("Check checkboxes initial state.")
        assert not page.is_checkbox_checked(self.CHECKBOX_INDEX_0), (
            f"Expected checkbox {self.CHECKBOX_INDEX_0} to be unchecked"
        )
        assert page.is_checkbox_checked(self.CHECKBOX_INDEX_1), (
            f"Expected checkbox {self.CHECKBOX_INDEX_1} to be checked"
        )

        self.logger.info("Set checkboxes new state.")
        page.set_checkbox(self.CHECKBOX_INDEX_0, True)
        page.set_checkbox(self.CHECKBOX_INDEX_1, False)

        self.logger.info("Check checkboxes new state.")
        assert page.is_checkbox_checked(self.CHECKBOX_INDEX_0), (
            f"Expected checkbox {self.CHECKBOX_INDEX_0} to be checked"
        )
        assert not page.is_checkbox_checked(self.CHECKBOX_INDEX_1), (
            f"Expected checkbox {self.CHECKBOX_INDEX_1} to be unchecked"
        )
