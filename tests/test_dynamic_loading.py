import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("Dynamic Loading")
@allure.story("Tests Dynamic Loading functionality")
class TestDynamicLoading(UiBaseCase):
    """Tests Dynamic Loading functionality"""

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_example_1(self) -> None:
        self.logger.info("Tests Dynamic Loading - Example 1.")
        main_page = MainPage(self)
        page = main_page.click_dynamic_loading_link().click_example_1_link()

        self.logger.info("Clicking start button.")
        page.click_start_button()

        self.logger.info("Verifying success message.")
        assert "Hello World!" in page.get_success_message()

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_example_2(self) -> None:
        self.logger.info("Tests Dynamic Loading - Example 2.")
        main_page = MainPage(self)
        page = main_page.click_dynamic_loading_link().click_example_2_link()

        self.logger.info("Clicking start button.")
        page.click_start_button()

        self.logger.info("Verifying success message.")
        assert "Hello World!" in page.get_success_message()
