import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage

LAT_VAL = 32.0853
LONG_VAL = 34.7818


@allure.parent_suite("UI Test Suite")
@allure.suite("Geolocation")
@allure.sub_suite("Tests Geolocation functionality")
class TestGeolocation(UiBaseCase):
    """Tests Geolocation functionality"""

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_geolocation_functionality(self) -> None:
        self.logger.info("Tests Geolocation.")
        main_page = MainPage(self)
        page = main_page.click_geolocation_link()

        self.logger.info("Clicking 'Where am I' button.")
        page.click_where_am_i_button()

        self.logger.info("Verifying geolocation latitude value.")
        lat = page.get_latitude_value()
        assert LAT_VAL == lat, f"expected '{LAT_VAL}', but got '{lat}'"

        self.logger.info("Verifying geolocation longitude value.")
        long = page.get_longitude_value()
        assert LONG_VAL == long, f"expected '{LONG_VAL}', but got '{long}'"
