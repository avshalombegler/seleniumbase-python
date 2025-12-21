import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("Broken Images")
@allure.sub_suite("Verify the correct number of broken and valid images on the page")
class TestBrokenImages(UiBaseCase):
    """Tests for verifying broken and valid images"""

    EXPECTED_BROKEN_IMAGES = 2
    EXPECTED_VALID_IMAGES = 1

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_broken_images_count(self) -> None:
        self.logger.info("Verify broken images count.")
        main_page = MainPage(self)
        page = main_page.click_broken_images_link()

        self.logger.info("Getting broken images count.")
        broken_count = page.get_broken_images_count()
        self.logger.info(f"Found {broken_count} broken images.")
        self.assert_equal(
            broken_count,
            self.EXPECTED_BROKEN_IMAGES,
            f"Expected {self.EXPECTED_BROKEN_IMAGES} broken images, found {broken_count}",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_valid_images_count(self) -> None:
        self.logger.info("Verify valid images count.")
        main_page = MainPage(self)
        page = main_page.click_broken_images_link()

        self.logger.info("Getting valid images count.")
        valid_count = page.get_valid_images_count()
        self.logger.info(f"Found {valid_count} valid images.")
        self.assert_equal(
            valid_count,
            self.EXPECTED_VALID_IMAGES,
            f"Expected {self.EXPECTED_VALID_IMAGES} valid images, found {valid_count}",
        )
