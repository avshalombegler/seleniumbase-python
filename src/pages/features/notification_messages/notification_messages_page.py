from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.notification_messages.locators import NotificationMessagesLocators

if TYPE_CHECKING:
    pass


class NotificationMessagesPage(BasePage):
    """Page object for the Notification Messages landing page containing methods to navigate and check flash visibility."""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(NotificationMessagesLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Click here link")
    def click_here(self) -> NotificationMessageRenderedPage:
        self.click_element(NotificationMessagesLocators.CLICK_HERE_LINK)

        return NotificationMessageRenderedPage(self.driver)

    @allure.step("Get flash message text")
    def get_flash_message(self) -> str:
        return self.get_dynamic_element_text(NotificationMessagesLocators.FLASH_MESSAGE)

    @allure.step("Check if flash message is visible")
    def is_flash_message_visible(self) -> bool:
        return self.is_element_visible(NotificationMessagesLocators.FLASH_MESSAGE, timeout=0)


class NotificationMessageRenderedPage(BasePage):
    """Page object for the Notification Message Rendered page containing methods to interact with flash messages."""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(NotificationMessagesLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Get flash message text")
    def get_flash_message(self) -> str:
        return self.get_dynamic_element_text(NotificationMessagesLocators.FLASH_MESSAGE)

    @allure.step("Check if flash message is visible")
    def is_flash_message_visible(self) -> bool:
        return self.is_element_visible(NotificationMessagesLocators.FLASH_MESSAGE, timeout=0)

    @allure.step("Dismiss flash message")
    def dismiss_flash_message(self) -> None:
        self.click_element(NotificationMessagesLocators.FLASH_CLOSE_BUTTON)
        self.wait_for_invisibility(NotificationMessagesLocators.FLASH_MESSAGE)

    @allure.step("Click here link")
    def click_here(self) -> NotificationMessageRenderedPage:
        self.click_element(NotificationMessagesLocators.CLICK_HERE_LINK)

        return NotificationMessageRenderedPage(self.driver)
