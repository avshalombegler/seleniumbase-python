import allure
import pytest
from parameterized import parameterized

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Form Authentication")
@allure.sub_suite("Tests Form Authentication functionality")
class TestFormAuthentication(UiBaseCase):
    """Tests Form Authentication functionality"""

    SUCCESSFULL_LOGIN = "You logged into"
    SUCCESSFULL_LOGOUT = "You logged out of"

    @parameterized.expand(
        [
            ["tomsmith", "SuperSecretPassword!", "You logged into"],
            ["tomsmith", "wrong!", "Your password is invalid!"],
            ["wrong", "SuperSecretPassword!", "Your username is invalid!"],
        ],
    )
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_authentication_functionality(
        self,
        username: str,
        password: str,
        expected_message: str,
    ) -> None:
        self.logger.info("Tests Form Authentication.")
        main_page = MainPage(self)
        page = main_page.click_form_authentication_link()

        self.logger.info(f"Entering username '{username}'.")
        page.enter_username(username)

        self.logger.info(f"Entering password '{password}'.")
        page.enter_password(password)

        if self.SUCCESSFULL_LOGIN in expected_message:
            self.logger.info("Clicking login button.")
            secure_area_page = page.click_login_correct()

            self.logger.info("Getting flash message.")
            flash_message = secure_area_page.get_flash_message()

            self.logger.info("Verifying flash message after successfull login.")
            self.assert_in(
                expected_message,
                flash_message,
                f"Expected '{flash_message}'to contain '{expected_message}'",
            )

            self.logger.info("Clicking logout button.")
            page = secure_area_page.click_logout()

            self.logger.info("Getting flash message.")
            flash_message = page.get_flash_message()

            self.logger.info("Verifying flash message after successfull login.")
            self.assert_in(
                self.SUCCESSFULL_LOGOUT,
                flash_message,
                f"Expected '{flash_message}'to contain '{self.SUCCESSFULL_LOGOUT}'",
            )

        else:
            self.logger.info("Clicking login button.")
            page.click_login_invalid()

            self.logger.info("Getting flash message.")
            flash_message = page.get_flash_message()

            self.logger.info("Verifying flash message after unsuccessfull login.")
            self.assert_in(
                expected_message,
                flash_message,
                f"Expected '{flash_message}'to contain '{expected_message}'",
            )
