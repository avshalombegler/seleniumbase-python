import allure
import pytest
from parameterized import parameterized
from seleniumbase import BaseCase

from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Basic Auth")
@allure.sub_suite("Tests Basic Autorization login scenatios")
class TestBasicAuth(BaseCase):
    """Tests basic autorization login scenatios"""

    @parameterized.expand(
        [
            ["admin", "admin", 200, "Congratulations! You must have the proper credentials."],
            ["wrong", "wrong", 401, "Not authorized\n"],
            ["", "", 401, "Not authorized\n"],
        ]
    )
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_basic_auth(
        self,
        username: str,
        password: str,
        expected_status_code: int,
        expected_message: str,
    ) -> None:
        """Tests basic autorization login scenatios"""
        import logging

        logger = logging.getLogger(__name__)

        logger.info("Tests basic autorization login scenatios.")
        main_page = MainPage(self)
        page = main_page.get_basic_auth_page()

        logger.info("Initialize URL based on username and password.")
        url = page.init_url(username, password)

        logger.info("Get status code and authorization message.")
        status_code, message = page.get_status_code_and_auth_message(url)

        logger.info("Validate status code and authorization message.")
        self.assert_equal(
            expected_status_code, status_code, f"Expected '{expected_status_code}', but got '{status_code}'"
        )
        self.assert_in(expected_message, message, f"Expected '{message}' to contain '{expected_message}'")
