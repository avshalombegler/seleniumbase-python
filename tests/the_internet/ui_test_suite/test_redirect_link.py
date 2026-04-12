import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage

EXPECTED_HEADING = "Redirection"


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("Redirect Link")
class TestRedirectLink(UiBaseCase):
    """Tests Redirect Link functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    def test_redirect_link_navigates_to_status_codes(self) -> None:
        self.logger.info("Tests that clicking the redirect link navigates to the status codes page.")
        main_page = MainPage(self)
        page = main_page.click_redirect_link_link()

        page.click_redirect_here()

        self.assert_true(
            self.get_current_url().endswith("/status_codes"),
            "Expected URL to end with /status_codes after clicking the redirect link",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_redirect_link_page_heading(self) -> None:
        self.logger.info("Tests that the redirect link page loads with the correct heading.")
        main_page = MainPage(self)
        page = main_page.click_redirect_link_link()

        heading = page.get_heading_text()
        self.assert_equal(heading, EXPECTED_HEADING, f"Expected heading '{EXPECTED_HEADING}', got '{heading}'")
