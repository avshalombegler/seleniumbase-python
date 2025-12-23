import allure
import pytest
from parameterized import parameterized

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Challenging DOM")
@allure.sub_suite("Verify Challenging DOM buttons interactions and table content")
class TestChallengingDom(UiBaseCase):
    """Tests for verifying Challenging DOM buttons interactions and table content"""

    BUTTONS = [["blue"], ["red"], ["green"]]
    COLUMNS = ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Diceret"]
    CELL_VALUES = ["Iuvaret", "Apeirian", "Adipisci", "Definiebas", "Consequuntur", "Phaedrum"]
    EDIT_SUFFIX = "challenging_dom#edit"
    DEL_SUFFIX = "challenging_dom#delete"

    @parameterized.expand(BUTTONS)
    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_each_button_clicks(self, button: str) -> None:
        self.logger.info("Verify each button in page is clickable.")
        main_page = MainPage(self)
        page = main_page.click_challenging_dom_link()

        self.logger.info(f"Clicking {button} button.")
        page.click_colored_button(button)

    @parameterized.expand(COLUMNS)
    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table_header_per_column(self, col: str) -> None:
        self.logger.info("Verify table head text per column.")
        main_page = MainPage(self)
        page = main_page.click_challenging_dom_link()

        self.logger.info(f"Getting table head text of column '{col}'.")
        header = page.get_table_head_text(col)
        self.assert_equal(header, col, f"Table head value '{col}' not found (got '{header}')")

    @parameterized.expand(zip(COLUMNS, CELL_VALUES))
    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_cells_content_per_column(self, col: str, cell: str) -> None:
        self.logger.info("Verify cell content per column.")
        main_page = MainPage(self)
        page = main_page.click_challenging_dom_link()

        for i in range(3):  # reduced repetition for faster tests; expand as needed
            expected = f"{cell}{i}"
            self.logger.info(f"Getting table cell '{cell}' text under column '{col}'.")
            val = page.get_table_cell_text(col, expected)
            self.assert_equal(val, expected, f"Cell value '{expected}' under '{col}' not found (got '{val}')")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table_edit_and_delete_buttons_per_row(self) -> None:
        self.logger.info("Verify edit and delete buttons per row are clickable.")
        main_page = MainPage(self)
        page = main_page.click_challenging_dom_link()

        for i in range(3):  # reduced repetition for faster tests; expand as needed
            self.logger.info(f"Clicking edit button in row {i}.")
            page.click_edit_button(i)

            current_url = self.get_current_url()
            self.assert_in(
                self.EDIT_SUFFIX,
                current_url,
                f"Expected URL '{self.EDIT_SUFFIX} in URL', got URL: '{current_url}'",
            )

            self.logger.info(f"Click delete button in row {i}.")
            page.click_delete_button(i)

            current_url = self.get_current_url()
            self.assert_in(
                self.DEL_SUFFIX,
                current_url,
                f"Expected URL '{self.DEL_SUFFIX} in URL', got URL: '{current_url}'",
            )
