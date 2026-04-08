import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage

EXPECTED_ROW_COUNT = 50
EXPECTED_COL_COUNT = 50
EXPECTED_HEADER_COUNT = 50


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("Large and Deep DOM")
class TestLargeAndDeepDom(UiBaseCase):
    """Tests for the Large and Deep DOM page."""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    def test_large_dom_table_is_present(self) -> None:
        self.logger.info("Test that the large DOM table is present on the page.")
        main_page = MainPage(self)
        main_page.click_large_and_deep_dom_link()

        self.assert_true(self.get_current_url().endswith("/large"), "URL should end with /large")
        self.assert_element_visible("#large-table")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table_has_50_rows(self) -> None:
        self.logger.info("Test that the large DOM table has 50 rows.")
        main_page = MainPage(self)
        page = main_page.click_large_and_deep_dom_link()

        self.assert_equal(page.get_table_row_count(), EXPECTED_ROW_COUNT, "Table should have 50 rows")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table_has_50_columns(self) -> None:
        self.logger.info("Test that the large DOM table has 50 columns.")
        main_page = MainPage(self)
        page = main_page.click_large_and_deep_dom_link()

        self.assert_equal(page.get_table_col_count(), EXPECTED_COL_COUNT, "Table should have 50 columns")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_last_cell_is_present(self) -> None:
        self.logger.info("Test that the last data cell is present — deep DOM rendered fully.")
        main_page = MainPage(self)
        page = main_page.click_large_and_deep_dom_link()

        self.assert_true(page.is_last_cell_present(), "Last data cell should be present — deep DOM rendered fully")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_cells_are_present(self) -> None:
        self.logger.info("Test that header cells header-1 through header-50 are present.")
        main_page = MainPage(self)
        page = main_page.click_large_and_deep_dom_link()

        self.assert_equal(
            page.get_header_cell_count(),
            EXPECTED_HEADER_COUNT,
            "Table should have 50 header cells",
        )
        self.assert_true(page.is_first_header_present(), "First header cell (header-1) should be visible")
        self.assert_true(page.is_last_header_present(), "Last header cell (header-50) should be present")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.MINOR)
    def test_first_row_and_cell_accessible(self) -> None:
        self.logger.info("Test that the first data row and first cell are accessible.")
        main_page = MainPage(self)
        main_page.click_large_and_deep_dom_link()

        self.assert_element_visible("table#large-table tbody tr:first-child")
        self.assert_element_visible("table#large-table tbody tr:first-child td:first-child")
