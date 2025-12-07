import allure
import pytest

from pages.base.ui_base_case import UiBaseCase
from pages.common.main_page.main_page import MainPage


@allure.feature("Dynamic Content")
@allure.story("Tests Dynamic Content functionality")
class TestDynamicContent(UiBaseCase):
    """Tests for Dynamic Content functionality"""

    @pytest.mark.full
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_content_changes_after_refresh(self) -> None:
        self.logger.info("Test that content changes after page refresh.")

        main_page = MainPage(self)
        page = main_page.click_dynamic_content_link()
        initial_blocks = page.get_all_content_blocks()

        page.refresh_page()
        refreshed_blocks = page.get_all_content_blocks()

        self.logger.info("Validating initial content blocks structure and count.")
        self._validate_blocks_count(initial_blocks)
        self._validate_blocks_structure(initial_blocks)

        self.logger.info("Validating refreshed content blocks structure and count.")
        self._validate_blocks_count(refreshed_blocks)
        self._validate_blocks_structure(refreshed_blocks)

        self.logger.info("Comparing content changes after refresh.")
        changed_count = self._count_changed_blocks(initial_blocks, refreshed_blocks)
        assert 0 < changed_count <= 3, f"Expected 1-3 blocks to change, got {changed_count}"

    def _validate_blocks_count(self, blocks: list) -> None:
        """Validate that we have exactly 3 content blocks"""
        assert len(blocks) == 3, f"Expected 3 content blocks, got {len(blocks)}"

    def _validate_blocks_structure(self, blocks: list) -> None:
        """Validate structure of each content block"""
        for block in blocks:
            assert block["image"].startswith("http"), "Invalid image URL"
            assert block["text"].strip(), "Empty text in block"

    def _count_changed_blocks(self, initial_blocks: list, refreshed_blocks: list) -> int:
        """Count how many blocks changed between refreshes"""
        return sum(
            1
            for i in range(3)
            if (
                initial_blocks[i]["image"] != refreshed_blocks[i]["image"]
                or initial_blocks[i]["text"] != refreshed_blocks[i]["text"]
            )
        )
