from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.config import settings
from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.geolocation.locators import GeolocationPageLocators

if TYPE_CHECKING:
    pass


class GeolocationPage(BasePage):
    """Page object for the Geolocation page containing methods to interact with and validate page functionality"""

    def __init__(
        self,
        driver: BaseCase,
        wait_for_load: bool = True,
    ) -> None:
        super().__init__(driver)
        if wait_for_load:
            self.wait_for_page_to_load(GeolocationPageLocators.PAGE_LOADED_INDICATOR)

        # Inject geolocation mock for Chrome after page loads
        if self.driver.browser == "chrome":
            self._inject_chrome_geolocation_mock()

        # Inject geolocation mock for Firefox after page loads
        if self.driver.browser == "firefox":
            self._inject_firefox_geolocation_mock()

    def _inject_chrome_geolocation_mock(self) -> None:
        """Inject geolocation mock for Chrome browser."""

        self.driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {"origin": "https://the-internet.herokuapp.com", "permissions": ["geolocation"]},
        )
        self.driver.execute_cdp_cmd(
            "Emulation.setGeolocationOverride",
            {
                "latitude": settings.GEOLOCATION_LAT,
                "longitude": settings.GEOLOCATION_LON,
                "accuracy": 100,
            },
        )

    def _inject_firefox_geolocation_mock(self) -> None:
        """Inject geolocation mock for Firefox browser."""

        script = f"""
        Object.defineProperty(navigator.geolocation, 'getCurrentPosition', {{
            value: function(success, error) {{
                success({{
                    coords: {{
                        latitude: {settings.GEOLOCATION_LAT},
                        longitude: {settings.GEOLOCATION_LON},
                        accuracy: 100,
                        altitude: null,
                        altitudeAccuracy: null,
                        heading: null,
                        speed: null
                    }},
                    timestamp: Date.now()
                }});
            }},
            writable: false,
            configurable: false
        }});
        """
        self.driver.execute_script(script)

    @allure.step("Click 'Where am I?' button")
    def click_where_am_i_button(self) -> None:
        self.click_element(GeolocationPageLocators.WHERE_AM_I_BTN)

    @allure.step("Get latitude value")
    def get_latitude_value(self) -> float:
        return float(self.get_dynamic_element_text(GeolocationPageLocators.LAT_VAL))

    @allure.step("Click longitude value")
    def get_longitude_value(self) -> float:
        return float(self.get_dynamic_element_text(GeolocationPageLocators.LONG_VAL))
