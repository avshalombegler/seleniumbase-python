import allure
import pytest
from parameterized import parameterized

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("Floating Menu")
@allure.story("Tests Floating Menu functionality")
class TestFloatingMenu(UiBaseCase):
    """Tests Floating Menu functionality"""

    FLOATING_MENU_ITEM = [
        ["Home"],
        ["News"],
        ["Contact"],
        ["About"],
    ]

    @parameterized.expand(FLOATING_MENU_ITEM)
    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_floating_menu_functionality(self, item: str) -> None:
        self.logger.info("Tests Files Download.")
        main_page = MainPage(self)
        page = main_page.click_floating_menu_link()

        self.logger.info("Scrolling down.")
        page.scroll_down()

        self.logger.info(f"Clicking floating menu item '{item}'.")
        page.click_floating_menu_item(item)

        self.logger.info("Getting current URL.")
        current_url = self.get_current_url()

        self.logger.info("Verifying url updated after click on menu item.")
        assert item.lower() in current_url, f"Expected '{current_url}' to contain '{item.lower()}'"
