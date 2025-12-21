from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.dynamic_content.locators import DynamicContentPageLocators

if TYPE_CHECKING:
    pass


class DynamicContentPage(BasePage):
    """Page object for the Dynamic Content page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(DynamicContentPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get all content blocks data")
    def get_all_content_blocks(self) -> list:
        blocks = self.get_all_elements(DynamicContentPageLocators.CONTENT_BLOCKS)
        data = []
        for block in blocks:
            try:
                img = block.find_element(
                    DynamicContentPageLocators.IMAGE_IN_BLOCK["by"],
                    DynamicContentPageLocators.IMAGE_IN_BLOCK["selector"],
                ).get_attribute("src")
                text = block.find_element(
                    DynamicContentPageLocators.TEXT_IN_BLOCK["by"], DynamicContentPageLocators.TEXT_IN_BLOCK["selector"]
                ).text.strip()
                data.append({"image": img, "text": text})
            except Exception:
                self.logger.warning("Failed to parse block content")
                continue
        return data
