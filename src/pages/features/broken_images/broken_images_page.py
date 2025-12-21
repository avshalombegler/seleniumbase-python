from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.broken_images.locators import BrokenImagesPageLocators

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

    from src.pages.base.base_page import Locator


class BrokenImagesPage(BasePage):
    """Page object for the Broken Images page containing methods to interact with and validate images."""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(BrokenImagesPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get all image elements")
    def _get_all_images(self) -> list:
        self.logger.info("Get all image elements.")
        return self.get_all_elements(BrokenImagesPageLocators.IMAGES)

    def _get_locator_from_element(self, image: WebElement) -> Locator:
        tag = image.tag_name
        src = image.get_attribute("src")
        if src is None:
            raise ValueError("Image element has no 'src' attribute")
        image_name = src.split("/")[-1]
        locator = self.format_locator(BrokenImagesPageLocators.IMAGE, tag=tag, image_name=image_name)
        return locator

    @allure.step("Get image natural width")
    def _get_image_natural_width(self, image: WebElement) -> dict:
        self.logger.info("Check if image is broken.")
        locator = self._get_locator_from_element(image)
        natural_width = self.get_element_attr(locator, "naturalWidth")
        return {"natural_width": natural_width}

    @allure.step("Get count of broken images")
    def get_broken_images_count(self) -> int:
        images = self._get_all_images()
        results = [self._get_image_natural_width(img) for img in images]
        return len([img for img in results if int(img["natural_width"]) == 0])

    @allure.step("Get count of valid images")
    def get_valid_images_count(self) -> int:
        images = self._get_all_images()
        results = [self._get_image_natural_width(img) for img in images]
        return len([img for img in results if int(img["natural_width"]) > 0])
