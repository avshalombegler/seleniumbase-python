import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage
from src.pages.features.shadow_dom.locators import ShadowDomLocators

EXPECTED_HEADING = "Simple template"
EXPECTED_SLOT_TEXT = "Let's have some different text!"


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("Shadow DOM")
class TestShadowDom(UiBaseCase):
    """Tests Shadow DOM functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    def test_shadow_dom_page_loads(self) -> None:
        self.logger.info("Test Shadow DOM page loads with correct heading.")
        main_page = MainPage(self)
        page = main_page.click_shadow_dom_link()

        heading = page.get_heading_text()
        self.assert_equal(heading, EXPECTED_HEADING, f"Expected heading '{EXPECTED_HEADING}', got '{heading}'")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_shadow_dom_slot_text(self) -> None:
        self.logger.info("Test Shadow DOM slotted text content.")
        main_page = MainPage(self)
        page = main_page.click_shadow_dom_link()

        slot_text = page.get_shadow_slot_text()
        self.assert_equal(
            slot_text, EXPECTED_SLOT_TEXT, f"Expected slot text '{EXPECTED_SLOT_TEXT}', got '{slot_text}'"
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.MINOR)
    def test_shadow_dom_host_element_visible(self) -> None:
        self.logger.info("Test Shadow DOM host element is visible.")
        main_page = MainPage(self)
        page = main_page.click_shadow_dom_link()

        self.assert_true(
            page.is_element_visible(ShadowDomLocators.SHADOW_HOST),
            "Expected shadow host element (my-paragraph) to be visible",
        )
