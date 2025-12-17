from __future__ import annotations

import time
from typing import TYPE_CHECKING

import allure

from pages.base.base_page import BaseCase, BasePage
from pages.features.drag_and_drop.locators import DragAndDropPageLocators

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class DragAndDropPage(BasePage):
    """Page object for the Drag and Drop page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(DragAndDropPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Perform drag and drop on box")
    def drag_and_drop_box(self) -> None:
        # Check if the driver is Firefox; if so, skip SeleniumBase drag_and_drop and use JS directly
        browser = self.driver.browser

        if browser != "firefox":
            try:
                # Try SeleniumBase drag_and_drop first for Chrome/other browsers
                self.driver.drag_and_drop(
                    drag_selector=DragAndDropPageLocators.BOX_A["selector"],
                    drop_selector=DragAndDropPageLocators.BOX_B["by"],
                    drag_by=DragAndDropPageLocators.BOX_A["selector"],
                    drop_by=DragAndDropPageLocators.BOX_B["by"],
                )
                self.logger.info("Drag and drop completed using SeleniumBase.")
                time.sleep(0.4)  # Allow DOM update
                return
            except Exception as e:
                self.logger.warning(f"SeleniumBase drag_and_drop failed: {e}. Falling back to JS.")

        # Fallback to improved JS simulation for Firefox or if SeleniumBase failed
        source = self.wait_for_visibility(DragAndDropPageLocators.BOX_A)
        target = self.wait_for_visibility(DragAndDropPageLocators.BOX_B)
        self._js_drag_and_drop(source, target)

    def _js_drag_and_drop(self, source: WebElement, target: WebElement) -> None:
        """Improved JS-based drag and drop simulation using HTML5 events."""
        js = """
        function simulateHTML5DragDrop(source, target) {
            // Create a DataTransfer object if supported, else a simple mock
            var dataTransfer = null;
            try {
                dataTransfer = new DataTransfer();
            } catch (e) {
                dataTransfer = {
                    data: {},
                    setData: function(key, val) { this.data[key] = val; },
                    getData: function(key) { return this.data[key]; },
                    effectAllowed: 'move',
                    dropEffect: 'move'
                };
            }
            // Dispatch dragstart on source
            var dragStartEvent = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            source.dispatchEvent(dragStartEvent);
            // Dispatch dragenter and dragover on target to prepare for drop
            var dragEnterEvent = new DragEvent('dragenter', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            target.dispatchEvent(dragEnterEvent);
            var dragOverEvent = new DragEvent('dragover', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            target.dispatchEvent(dragOverEvent);
            // Dispatch drop on target
            var dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            target.dispatchEvent(dropEvent);
            // Dispatch dragend on source
            var dragEndEvent = new DragEvent('dragend', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            source.dispatchEvent(dragEndEvent);
        }
        simulateHTML5DragDrop(arguments[0], arguments[1]);
        """
        try:
            self.driver.execute_script(js, source, target)
            self.logger.info("Drag and drop completed using JS simulation.")
        except Exception as e:
            self.logger.error(f"JS drag_and_drop failed: {e}")
            raise
        time.sleep(0.4)  # Allow DOM update

    @allure.step("Get box header")
    def get_box_header(self, box: str) -> str:
        locator = self.format_locator(DragAndDropPageLocators.BOX_HEADER, box=box)
        return self.get_dynamic_element_text(locator)
