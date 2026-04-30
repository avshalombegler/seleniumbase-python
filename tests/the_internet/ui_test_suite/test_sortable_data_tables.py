import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage

EXPECTED_HEADING = "Data Tables"
EXPECTED_URL_SUFFIX = "/tables"
EXPECTED_ROW_COUNT = 4
EXPECTED_HEADER_COUNT = 6
TABLE1_FIRST_ROW_LAST_NAME_DEFAULT = "Smith"
TABLE2_FIRST_ROW_LAST_NAME_DEFAULT = "Smith"
TABLE2_FIRST_ROW_DUE_DEFAULT = "$50.00"


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("Sortable Data Tables")
class TestSortableDataTables(UiBaseCase):
    """Tests Sortable Data Tables functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_loads_with_both_tables(self) -> None:
        self.logger.info("Test that page loads with both data tables visible.")
        main_page = MainPage(self)
        page = main_page.click_sortable_data_tables_link()

        heading = page.get_heading_text()
        self.logger.info(f"Retrieved heading: {heading}.")
        table1_rows = page.get_table1_row_count()
        self.logger.info(f"Table1 row count: {table1_rows}.")
        table2_rows = page.get_table2_row_count()
        self.logger.info(f"Table2 row count: {table2_rows}.")
        table1_headers = page.get_table1_header_count()
        self.logger.info(f"Table1 header count: {table1_headers}.")
        table2_headers = page.get_table2_header_count()
        self.logger.info(f"Table2 header count: {table2_headers}.")

        self.assert_equal(heading, EXPECTED_HEADING, f"Expected heading '{EXPECTED_HEADING}', got '{heading}'")
        self.assert_equal(
            table1_rows, EXPECTED_ROW_COUNT, f"Expected {EXPECTED_ROW_COUNT} rows in table1, got {table1_rows}"
        )
        self.assert_equal(
            table2_rows, EXPECTED_ROW_COUNT, f"Expected {EXPECTED_ROW_COUNT} rows in table2, got {table2_rows}"
        )
        self.assert_equal(
            table1_headers,
            EXPECTED_HEADER_COUNT,
            f"Expected {EXPECTED_HEADER_COUNT} headers in table1, got {table1_headers}",
        )
        self.assert_equal(
            table2_headers,
            EXPECTED_HEADER_COUNT,
            f"Expected {EXPECTED_HEADER_COUNT} headers in table2, got {table2_headers}",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table1_displays_correct_data(self) -> None:
        self.logger.info("Test that table1 displays correct initial row data.")
        main_page = MainPage(self)
        page = main_page.click_sortable_data_tables_link()

        first_row_last_name = page.get_table1_first_row_last_name()
        self.logger.info(f"Table1 first row last name: {first_row_last_name}.")

        self.assert_equal(
            first_row_last_name,
            TABLE1_FIRST_ROW_LAST_NAME_DEFAULT,
            f"Expected table1 first row last name to be "
            f"'{TABLE1_FIRST_ROW_LAST_NAME_DEFAULT}', got '{first_row_last_name}'",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table2_displays_correct_data(self) -> None:
        self.logger.info("Test that table2 displays correct initial row data using class-based selectors.")
        main_page = MainPage(self)
        page = main_page.click_sortable_data_tables_link()

        first_row_last_name = page.get_table2_first_row_last_name()
        self.logger.info(f"Table2 first row last name: {first_row_last_name}.")
        first_row_due = page.get_table2_first_row_due()
        self.logger.info(f"Table2 first row due: {first_row_due}.")

        self.assert_equal(
            first_row_last_name,
            TABLE2_FIRST_ROW_LAST_NAME_DEFAULT,
            f"Expected table2 first row last name '{TABLE2_FIRST_ROW_LAST_NAME_DEFAULT}', got '{first_row_last_name}'",
        )
        self.assert_equal(
            first_row_due,
            TABLE2_FIRST_ROW_DUE_DEFAULT,
            f"Expected table2 first row due '{TABLE2_FIRST_ROW_DUE_DEFAULT}', got '{first_row_due}'",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table1_last_name_column_is_sortable(self) -> None:
        self.logger.info("Test that table1 Last Name column is sortable.")
        main_page = MainPage(self)
        page = main_page.click_sortable_data_tables_link()

        page.click_table1_last_name_header()
        self.logger.info("Clicked table1 Last Name header.")
        is_sorted = page.is_table1_last_name_header_sorted()
        self.logger.info(f"Table1 Last Name header sorted: {is_sorted}.")

        self.assert_true(is_sorted, "Expected table1 Last Name header to have a sort direction class after clicking")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_table2_due_column_is_sortable(self) -> None:
        self.logger.info("Test that table2 Due column is sortable using class-based selector.")
        main_page = MainPage(self)
        page = main_page.click_sortable_data_tables_link()

        page.click_table2_due_header()
        self.logger.info("Clicked table2 Due header.")
        is_sorted = page.is_table2_due_header_sorted()
        self.logger.info(f"Table2 Due header sorted: {is_sorted}.")

        self.assert_true(is_sorted, "Expected table2 Due header to have a sort direction class after clicking")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.MINOR)
    def test_tables_page_url(self) -> None:
        self.logger.info("Test that tables page has correct URL after navigation.")
        main_page = MainPage(self)
        main_page.click_sortable_data_tables_link()

        self.assert_true(
            self.get_current_url().endswith(EXPECTED_URL_SUFFIX), f"Expected URL to end with '{EXPECTED_URL_SUFFIX}'"
        )
