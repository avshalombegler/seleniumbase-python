from __future__ import annotations

from typing import TYPE_CHECKING

import allure
import pytest
from selenium.webdriver.common.keys import Keys

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage

if TYPE_CHECKING:
    pass


@allure.parent_suite("UI Test Suite")
@allure.suite("Key Presses")
@allure.sub_suite("Tests Key Presses functionality")
class TestKeyPresses(UiBaseCase):
    """Tests Key Presses functionality"""

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_key_presses_functionality(self) -> None:
        self.logger.info("Tests Key Presses.")
        main_page = MainPage(self)
        page = main_page.click_key_presses_link()

        test_cases: dict[str, str] = {
            Keys.SPACE: "You entered: SPACE",
            Keys.NUMPAD0: "You entered: NUMPAD0",
            Keys.NUMPAD5: "You entered: NUMPAD5",
            Keys.NUMPAD8: "You entered: NUMPAD8",
            Keys.ESCAPE: "You entered: ESCAPE",
            Keys.BACK_SPACE: "You entered: BACK_SPACE",
            Keys.ARROW_LEFT: "You entered: LEFT",
            Keys.ARROW_UP: "You entered: UP",
        }

        for key, expected_result in test_cases.items():
            self.logger.info("Pressing key '{key}'.")
            page.press_key(key)

            self.logger.info("Getting result.")
            result_text = page.get_result()

            self.logger.info("Verifying result matches key press.")
            self.assert_equal(result_text, expected_result, f"Expected '{result_text}', but got '{expected_result}'")
