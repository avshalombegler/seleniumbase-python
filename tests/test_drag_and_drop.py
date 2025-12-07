import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("Drag and Drop")
@allure.story("Tests Drag and Drop functionality")
class TestDragAndDrop(UiBaseCase):
    """Tests Drag and Drop functionality"""

    BOX_A = "A"
    BOX_B = "B"

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_drag_and_drop_functionality(self) -> None:
        self.logger.info("Tests Drag and Drop functionality.")
        main_page = MainPage(self)
        page = main_page.click_drag_and_drop_link()

        self.logger.info("Performing drag and drop on box element.")
        page.drag_and_drop_box()

        self.logger.info("Verifying drag and drop action succeeded.")
        assert page.get_box_header(self.BOX_A.lower()) == self.BOX_B
        assert page.get_box_header(self.BOX_B.lower()) == self.BOX_A
