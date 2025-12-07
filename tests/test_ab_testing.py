import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("A/B Testing")
@allure.story("Verify content on A/B Testing page")
class TestABTesting(UiBaseCase):
    """Tests for verifying title and paragraph content of page"""

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_ab_testing_content(self) -> None:
        self.logger.info("Tests for verifying title and paragraph content of page")
        main_page = MainPage(self)
        page = main_page.click_ab_testing_link()

        title = page.get_title_text()
        self.logger.info(f"Retrieved title: {title}.")
        expected_titles = ["A/B Test Control", "A/B Test Variation 1"]
        assert title in expected_titles, f"Expected title in {expected_titles}, got '{title}'"

        paragraph = page.get_paragraph_text()
        self.logger.info(f"Retrieved paragraph: {paragraph}.")
        expected_text = "Also known as split testing"
        assert expected_text in paragraph, f"Expected '{expected_text}' in paragraph, got '{paragraph}'"
