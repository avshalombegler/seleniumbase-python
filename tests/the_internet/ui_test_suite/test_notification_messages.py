import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage

EXPECTED_FLASH_MESSAGES = [
    "Action successful",
    "Action unsuccessful, please try again",
    "Action unsuccesful, please try again",
]


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("Notification Messages")
class TestNotificationMessages(UiBaseCase):
    """Tests Notification Messages functionality"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.CRITICAL)
    def test_flash_message_rendered_on_click(self) -> None:
        self.logger.info("Test that a flash message is rendered after clicking the 'Click here' link.")
        main_page = MainPage(self)
        page = main_page.click_notification_messages_link()

        rendered_page = page.click_here()

        self.assert_true(rendered_page.is_flash_message_visible(), "Expected flash message to be visible")
        flash_text = rendered_page.get_flash_message()
        self.assert_true(
            any(msg in flash_text for msg in EXPECTED_FLASH_MESSAGES),
            f"Expected flash message to contain one of {EXPECTED_FLASH_MESSAGES}, got '{flash_text}'",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_flash_message_can_be_dismissed(self) -> None:
        self.logger.info("Test that a flash message can be dismissed by clicking the close button.")
        main_page = MainPage(self)
        page = main_page.click_notification_messages_link()

        rendered_page = page.click_here()
        rendered_page.dismiss_flash_message()

        self.assert_false(
            rendered_page.is_flash_message_visible(), "Expected flash message to be hidden after dismissal"
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.MINOR)
    def test_repeated_clicks_produce_valid_flash_messages(self) -> None:
        self.logger.info("Test that repeated clicks on 'Click here' continue to produce valid flash messages.")
        main_page = MainPage(self)
        page = main_page.click_notification_messages_link()

        rendered_page_1 = page.click_here()
        rendered_page_2 = rendered_page_1.click_here()

        self.assert_true(
            rendered_page_2.is_flash_message_visible(), "Expected flash message to be visible after second click"
        )
        flash_text = rendered_page_2.get_flash_message()
        self.assert_true(
            any(msg in flash_text for msg in EXPECTED_FLASH_MESSAGES),
            f"Expected flash message to contain one of {EXPECTED_FLASH_MESSAGES}, got '{flash_text}'",
        )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_flash_message_visible_on_page_load(self) -> None:
        self.logger.info("Test that a flash message is already visible on the initial Notification Messages page load.")
        main_page = MainPage(self)
        page = main_page.click_notification_messages_link()

        self.assert_true(page.is_flash_message_visible(), "Expected flash message to be visible on initial page load")
        flash_text = page.get_flash_message()
        self.assert_true(
            any(msg in flash_text for msg in EXPECTED_FLASH_MESSAGES),
            f"Expected flash message to contain one of {EXPECTED_FLASH_MESSAGES}, got '{flash_text}'",
        )
