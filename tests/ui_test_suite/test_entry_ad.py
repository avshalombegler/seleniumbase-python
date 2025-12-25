import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@pytest.mark.skip(reason="Test is not yet complete")
@allure.parent_suite("UI Test Suite")
@allure.suite("Entry Ad")
@allure.sub_suite("Tests Entry Ad functionality")
class TestEntryAd(UiBaseCase):
    """Tests Entry Ad functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_appears_on_first_visit(self) -> None:
        """Test that modal appears on initial page load"""
        self.logger.info("Testing modal appearance on first visit.")
        main_page = MainPage(self)
        page = main_page.click_entry_ad_link()

        self.sleep(1)
        self.assert_true(page.is_modal_displayed())

        page.click_close_modal()
        self.assert_false(page.is_modal_displayed())

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_does_not_reappear_on_refresh(self) -> None:
        """Test that modal does not reappear after being closed and page refreshed"""
        self.logger.info("Testing modal does not reappear on refresh.")
        main_page = MainPage(self)
        page = main_page.click_entry_ad_link()

        self.sleep(1)
        if page.is_modal_displayed():
            page.click_close_modal()

        page.refresh_page()
        self.sleep(1)
        self.assert_false(page.is_modal_displayed())

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_reappears_with_re_enable_link(self) -> None:
        """Test that clicking re-enable link shows modal again"""
        self.logger.info("Testing modal reappearance via re-enable link.")
        main_page = MainPage(self)
        page = main_page.click_entry_ad_link()

        self.sleep(1)
        if page.is_modal_displayed():
            page.click_close_modal()

        self.sleep(0.5)
        page.click_re_enable_link()
        self.sleep(1)

        self.assert_true(page.is_modal_displayed())
        page.click_close_modal()

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    def test_modal_close_button_functionality(self) -> None:
        """Test that close button properly closes the modal"""
        self.logger.info("Testing modal close button.")
        main_page = MainPage(self)
        page = main_page.click_entry_ad_link()

        self.sleep(1)
        self.assert_true(page.is_modal_displayed())

        page.click_close_modal()
        self.sleep(0.5)
        self.assert_false(page.is_modal_displayed())

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_state_persists_across_navigation(self) -> None:
        """Test that modal state persists when navigating away and back"""
        self.logger.info("Testing modal state persistence.")
        main_page = MainPage(self)
        page = main_page.click_entry_ad_link()

        self.sleep(1)
        if page.is_modal_displayed():
            page.click_close_modal()

        self.open(self.get_current_url().replace("/entry_ad", ""))
        self.sleep(0.5)

        page = main_page.click_entry_ad_link()
        self.sleep(1)
        self.assert_false(page.is_modal_displayed())

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_does_not_reappear_in_new_session(self) -> None:
        """Test that modal appears in a completely new browser session"""
        self.logger.info("Testing modal in new session.")
        main_page = MainPage(self)
        page = main_page.click_entry_ad_link()

        self.sleep(1)
        if page.is_modal_displayed():
            page.click_close_modal()

        url = self.get_current_url().replace("/entry_ad", "")
        self.open_new_window()
        self.switch_to_newest_window()

        self.open(url)
        self.sleep(0.5)
        page_new = main_page.click_entry_ad_link()

        self.sleep(1)
        self.assert_false(page_new.is_modal_displayed())
