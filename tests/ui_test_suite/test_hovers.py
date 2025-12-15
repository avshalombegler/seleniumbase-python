import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Hovers")
@allure.sub_suite("Tests Hovers functionality")
class TestHovers(UiBaseCase):
    """Tests Hovers functionality"""

    USER: str = "user"
    USERS: str = "users/"
    FIRST_USER: int = 1
    NUM_OF_USERS: int = 3

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_hovers_functionality(self) -> None:
        self.logger.info("Tests Hovers.")
        main_page = MainPage(self)
        page = main_page.click_hovers_link()

        for user_index in range(self.FIRST_USER, self.NUM_OF_USERS + 1):
            self.logger.info("Hovering mouse over profile image.")
            page.hover_mouse_over_profile_image(user_index)

            self.logger.info("Getting user name text.")
            username_text = page.get_user_name_text(user_index)

            self.logger.info("Verifying user name text.")
            assert self.USER + str(user_index) in username_text, (
                f"Expected '{username_text}' to contain '{self.USER + str(user_index)}'"
            )

            self.logger.info("Clicking view profile link.")
            user_page = page.click_view_profile_link(user_index)

            self.logger.info("Getting current browser url.")
            current_url = self.get_current_url()

            self.logger.info("Verifying user name in current url.")
            assert self.USERS + str(user_index) in current_url, (
                f"Expected '{current_url}' to contain '{self.USERS + str(user_index)}'"
            )

            self.logger.info("Navigating back page.")
            user_page.navigate_back_page()
