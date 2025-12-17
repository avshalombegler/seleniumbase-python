from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.keys import Keys

from pages.base.base_page import BaseCase, BasePage
from pages.features.horizontal_slider.locators import HorizontalSliderPageLocators

if TYPE_CHECKING:
    pass


class HorizontalSliderPage(BasePage):
    """Page object for the Horizontal Slider page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(HorizontalSliderPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Set horizontal slider value using mouse")
    def set_horizontal_slider_value_using_mouse(self, r: int) -> None:
        slider_elem = self.wait_for_visibility(HorizontalSliderPageLocators.SLIDER)

        self.actions.move_to_element(slider_elem).pause(0.3).perform()
        self.actions.reset_actions()
        self.actions.click_and_hold(slider_elem).pause(0.2).move_by_offset(r, 0).pause(0.2).release().perform()

    @allure.step("Set horizontal slider value using keys")
    def set_horizontal_slider_value_using_keys(self, r: int) -> None:
        slider_elem = self.wait_for_visibility(HorizontalSliderPageLocators.SLIDER)

        self.actions.click(slider_elem).perform()
        self.actions.reset_actions()

        for _ in range(r):
            self.actions.send_keys(Keys.ARROW_LEFT).perform()
            sleep(0.5)

    @allure.step("Get horizontal slider value")
    def get_horizontal_slider_value(self) -> float:
        return float(self.get_dynamic_element_text(HorizontalSliderPageLocators.SLIDER_VALUE).strip())
