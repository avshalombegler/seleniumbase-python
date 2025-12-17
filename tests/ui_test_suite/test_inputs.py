import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Inputs")
@allure.sub_suite("Tests Inputs functionality")
class TestInputs(UiBaseCase):
    """Tests Inputs functionality"""

    NUMBER: int = 1337
    INCREASE_VALUE: int = 5
    DECREASE_VALUE: int = 2
    EXPECTED_VALUE: int = NUMBER + INCREASE_VALUE - DECREASE_VALUE

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_inputs_functionality(self) -> None:
        self.logger.info("Tests Inputs.")
        main_page = MainPage(self)
        page = main_page.click_inputs_link()

        self.logger.info("Entering input number.")
        page.enter_input_number(self.NUMBER)

        self.logger.info("Getting input number value.")
        input_number = page.get_input_number_value()

        self.logger.info("Verifying input number value.")
        self.assert_equal(
            self.NUMBER,
            input_number,
            f"Expected '{self.NUMBER}', but got '{input_number}'",
        )

        self.logger.info("Increasing number value using keyboard arrow.")
        page.increase_number_value(self.INCREASE_VALUE)

        self.logger.info("Getting input increased number value.")
        increased_number = page.get_input_number_value()

        self.logger.info("Verifying input number value.")
        self.assert_equal(
            self.NUMBER + self.INCREASE_VALUE,
            increased_number,
            f"Expected '{self.NUMBER + self.INCREASE_VALUE}', but got '{increased_number}'",
        )

        self.logger.info("Decreasing number value using keyboard arrow.")
        page.decrease_number_value(self.DECREASE_VALUE)

        self.logger.info("Getting decreased input number value.")
        decreased_number = page.get_input_number_value()

        self.logger.info("Verifying input number value.")
        self.assert_equal(
            self.EXPECTED_VALUE,
            decreased_number,
            f"Expected '{self.EXPECTED_VALUE}', but got '{decreased_number}'",
        )
