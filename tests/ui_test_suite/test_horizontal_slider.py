import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Horizontal Slider")
@allure.sub_suite("Tests Horizontal Slider functionality")
class TestHorizontalSlider(UiBaseCase):
    """Tests Horizontal Slider functionality"""

    EXPECTED_MIN_RANGE: float = 0.0
    EXPECTED_MAX_RANGE: float = 5.0
    EXPECTED_KEYS_RANGE: float = 0.5
    MIN_RANGE: int = -80
    MAX_RANGE: int = 80
    KEYS_RANGE: int = 4

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_horizontal_slider_functionality_using_mouse(self) -> None:
        self.logger.info("Tests Horizontal Slider.")
        main_page = MainPage(self)
        page = main_page.click_horizontal_slider_link()

        self.logger.info("Setting horizontal slider value using mouse.")
        page.set_horizontal_slider_value_using_mouse(self.MAX_RANGE)

        self.logger.info("Verifying horizontal slider new value.")
        slider_value = page.get_horizontal_slider_value()
        self.assert_equal(
            self.EXPECTED_MAX_RANGE,
            slider_value,
            f"Expected slider value '{self.EXPECTED_MAX_RANGE}', got '{slider_value}'",
        )

        self.logger.info("Setting horizontal slider value using drag and drop.")
        page.set_horizontal_slider_value_using_mouse(self.MIN_RANGE)

        self.logger.info("Verifying horizontal slider new value.")
        slider_value = page.get_horizontal_slider_value()
        self.assert_equal(
            self.EXPECTED_MIN_RANGE,
            slider_value,
            f"Expected slider value '{self.EXPECTED_MIN_RANGE}', got '{slider_value}'",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_horizontal_slider_functionality_using_keys(self) -> None:
        self.logger.info("Tests Horizontal Slider.")
        main_page = MainPage(self)
        page = main_page.click_horizontal_slider_link()

        self.logger.info("Setting horizontal slider value using arrow key.")
        page.set_horizontal_slider_value_using_keys(self.KEYS_RANGE)

        self.logger.info("Verifying horizontal slider new value.")
        slider_value = page.get_horizontal_slider_value()
        self.assert_equal(
            self.EXPECTED_KEYS_RANGE,
            slider_value,
            f"Expected slider value '{self.EXPECTED_KEYS_RANGE}', got '{slider_value}'",
        )
