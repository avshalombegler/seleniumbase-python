import allure
import pytest
from parameterized import parameterized

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Digest Authentication")
@allure.sub_suite("Verify Digest Authentication scenarios")
class TestDigestAuth(UiBaseCase):
    """Tests for Digest Authentication scenarios"""

    @parameterized.expand(
        [
            ["admin", "admin"],
            ["wrong", "admin"],
            ["admin", "wrong"],
        ],
    )
    @pytest.mark.full
    @allure.severity(allure.severity_level.NORMAL)
    def test_digest_auth_login_scenarios(self, username: str, password: str) -> None:
        self.logger.info("Tests for Digest Authentication scenarios.")
        main_page = MainPage(self)
        page = main_page.get_digest_auth_page(username, password)

        self.logger.info("Check if login succeeded.")
        success = page.is_login_successful()
        self.logger.info("Login " + ("succeeded" if success else "denied"))
