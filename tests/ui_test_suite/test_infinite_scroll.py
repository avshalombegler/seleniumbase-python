import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Infinite Scroll")
@allure.sub_suite("Tests Infinite Scroll functionality")
class TestInfiniteScroll(UiBaseCase):
    """Tests Infinite Scroll functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_infinite_scroll_functionality(self) -> None:
        self.logger.info("Tests Infinite Scroll.")
        main_page = MainPage(self)
        page = main_page.click_infinite_scroll_link()

        for _ in range(5):
            self.logger.info("Getting old page height.")
            old_height = page.get_page_height()

            self.logger.info("Scrolling to bottom of page.")
            page.scroll_to_bottom_of_page()

            self.logger.info("Getting new page height.")
            new_height = page.get_page_height()

            self.logger.info("Verifying new page height is bigger than old page height.")
            assert old_height < new_height, (
                f"Expected 'old height < new height', but got 'old height: {old_height}, new height: {new_height}'"
            )
