import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage

EXPECTED_HEADING = "Shifting Content"


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("Shifting Content")
class TestShiftingContent(UiBaseCase):
    """Tests Shifting Content functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    def test_shifting_content_index_page_loads(self) -> None:
        self.logger.info("Test Shifting Content index page loads with correct heading.")
        main_page = MainPage(self)
        page = main_page.click_shifting_content_link()

        heading = page.get_heading_text()
        self.assert_equal(heading, EXPECTED_HEADING, f"Expected heading '{EXPECTED_HEADING}', got '{heading}'")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_menu_example_link_navigates_correctly(self) -> None:
        self.logger.info("Test clicking Example 1 navigates to the menu sub-page.")
        main_page = MainPage(self)
        page = main_page.click_shifting_content_link()

        page.click_menu_example_link()
        self.assert_true(
            self.get_current_url().endswith("/shifting_content/menu"),
            "Expected URL to end with /shifting_content/menu",
        )
        self.assert_true(
            page.is_menu_container_visible(),
            "Expected the menu container to be visible on the menu sub-page",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_image_example_link_navigates_correctly(self) -> None:
        self.logger.info("Test clicking Example 2 navigates to the image sub-page.")
        main_page = MainPage(self)
        page = main_page.click_shifting_content_link()

        page.click_image_example_link()
        self.assert_true(
            self.get_current_url().endswith("/shifting_content/image"),
            "Expected URL to end with /shifting_content/image",
        )
        self.assert_true(
            page.is_image_visible(),
            "Expected an image element to be visible on the image sub-page",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_list_example_link_navigates_correctly(self) -> None:
        self.logger.info("Test clicking Example 3 navigates to the list sub-page.")
        main_page = MainPage(self)
        page = main_page.click_shifting_content_link()

        page.click_list_example_link()
        self.assert_true(
            self.get_current_url().endswith("/shifting_content/list"),
            "Expected URL to end with /shifting_content/list",
        )
        self.assert_true(
            page.is_list_visible(),
            "Expected the list container to be visible on the list sub-page",
        )
