import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Exit Intent")
@allure.sub_suite("Tests Exit Intent functionality")
class TestExitIntent(UiBaseCase):
    """Tests Exit Intent functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_window_functionality(self) -> None:
        self.logger.info("Tests Exit Intent.")
        main_page = MainPage(self)
        page = main_page.click_exit_intent_link()

        self.logger.info("Maximize broser window for better stability.")
        self.maximize_window()
        self.sleep(1)

        self.logger.info("Moving mouse out of the viewport pane.")
        page.trigger_exit_intent_js()

        self.logger.info("Verifying modal display.")
        self.assert_true(page.is_modal_displayed())

        self.logger.info("Clicking close button.")
        page.click_close_modal()

        self.logger.info("Verifying modal close.")
        self.assert_false(page.is_modal_displayed())
