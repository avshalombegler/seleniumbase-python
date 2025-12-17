import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Entry Ad")
@allure.sub_suite("Tests Entry Ad functionality")
class TestEntryAd(UiBaseCase):
    """Tests Entry Ad functionality"""

    @pytest.mark.skip(reason="Test is not yet complete")
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_window_functionality(self) -> None:
        self.logger.info("Tests Entry Ad.")
        main_page = MainPage(self)
        page = main_page.click_entry_ad_link()

        self.logger.info("Verifying ad window display.")
        self.assert_true(page.is_modal_displayed())

        self.logger.info("Clicking close button.")
        page.click_close_modal()

        self.logger.info("Verifying ad window close.")
        self.assert_false(page.is_modal_displayed())

        page.refresh_page()
        self.logger.info("Verifying ad window close.")
        self.assert_false(page.is_modal_displayed())

        self.logger.info("Clicking re-enable button.")
        # page.click_re_enable_link()

        self.logger.info("Verifying ad window display.")
        self.assert_true(page.is_modal_displayed())

        self.logger.info("Clicking close button.")
        page.click_close_modal()

        self.logger.info("Verifying ad window close.")
        self.assert_false(page.is_modal_displayed())
