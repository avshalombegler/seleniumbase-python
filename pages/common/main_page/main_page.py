from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urljoin

import allure

from config import settings
from pages.base.base_page import BaseCase, BasePage
from pages.common.main_page.locators import MainPageLocators
from pages.features.ab_testing.ab_testing_page import ABTestingPage
from pages.features.add_remove_elements.add_remove_elements_page import AddRemoveElementsPage
from pages.features.basic_auth.basic_auth_page import BasicAuthPage
from pages.features.broken_images.broken_images_page import BrokenImagesPage
from pages.features.challenging_dom.challenging_dom_page import ChallengingDomPage
from pages.features.checkboxes.checkboxes_page import CheckboxesPage
from pages.features.context_menu.context_menu_page import ContextMenuPage
from pages.features.digest_auth.digest_auth_page import DigestAuthPage
from pages.features.drag_and_drop.drag_and_drop_page import DragAndDropPage
from pages.features.dropdown_list.dropdown_list_page import DropdownListPage
from pages.features.dynamic_content.dynamic_content_page import DynamicContentPage
from pages.features.dynamic_controls.dynamic_controls_page import DynamicControlsPage
from pages.features.dynamic_loading.dynamic_loading_page import DynamicLoadingPage
from pages.features.entry_ad.entry_ad_page import EntryAdPage
from pages.features.exit_intent.exit_intent_page import ExitIntentPage
from pages.features.files_download.files_download_page import FilesDownloadPage
from pages.features.files_upload.files_upload_page import FileUploadPage
from pages.features.floating_menu.floating_menu_page import FloatingMenuPage
from pages.features.form_authentication.form_authentication_page import FormAuthenticationPage
from pages.features.frames.frames_page import FramesPage
from pages.features.geolocation.geolocation_page import GeolocationPage
from pages.features.horizontal_slider.horizontal_slider_page import HorizontalSliderPage
from pages.features.hovers.hovers_page import HoversPage
from pages.features.infinite_scroll.infinite_scroll_page import InfiniteScrollPage
from pages.features.inputs.inputs_page import InputsPage
from pages.features.javascript_alerts.javascript_alerts_page import JavaScriptAlertsPage
from pages.features.javascript_onload_event_error.javascript_onload_event_error_page import (
    JavaScriptOnloadRventErrorPage,
)
from pages.features.jquery_ui_menus.jquery_ui_menus_page import JQueryUIMenusPage
from pages.features.key_presses.key_presses_page import KeyPressesPage

if TYPE_CHECKING:
    from logging import Logger


class MainPage(BasePage):
    def __init__(self, driver: BaseCase, logger: Logger | None = None) -> None:
        super().__init__(driver, logger)
        if hasattr(self.driver, "request") and self.driver.request.node.get_closest_marker("ui"):
            self.wait_for_page_to_load(MainPageLocators.PAGE_LOADED_INDICATOR)
            self.base_url = settings.BASE_URL

    @allure.step("Navigate to {page_name} page")
    def click_ab_testing_link(self, page_name: str = "A/B Testing") -> ABTestingPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.AB_TESTING_LINK)

        return ABTestingPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_add_remove_elements_link(self, page_name: str = "Add/Remove Elements") -> AddRemoveElementsPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.ADD_REMOVE_ELEMENTS_LINK)

        return AddRemoveElementsPage(self.driver, self.logger)

    @allure.step("Returning object of {page_name} page")
    def get_basic_auth_page(self, page_name: str = "Basic Auth") -> BasicAuthPage:
        self.logger.info(f"Returning object of {page_name} page.")

        return BasicAuthPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_broken_images_link(self, page_name: str = "Broken Images") -> BrokenImagesPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.BROKEN_IMAGES_LINK)

        return BrokenImagesPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_challenging_dom_link(self, page_name: str = "Challenging DOM") -> ChallengingDomPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.CHALLENGING_DOM_LINK)

        return ChallengingDomPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_checkboxes_link(self, page_name: str = "Checkboxes") -> CheckboxesPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.CHECKBOXES_LINK)

        return CheckboxesPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_context_menu_link(self, page_name: str = "Context Menu") -> ContextMenuPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.CONTEXT_MENU_LINK)

        return ContextMenuPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def get_digest_auth_page(
        self, username: str, password: str, page_name: str = "Digest Authentication"
    ) -> DigestAuthPage:
        self.logger.info(f"Navigating to {page_name} page.")
        if not username or not password:
            raise ValueError(f"Invalid credentials: username='{username}', password='{password or ''}'")
        base_path = urljoin(str(self.base_url), "digest_auth")
        url = base_path.replace("https://", f"https://{username}:{password}@")
        self.navigate_to(url)

        return DigestAuthPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_drag_and_drop_link(self, page_name: str = "Drag and Drop") -> DragAndDropPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DRAG_AND_DROP_LINK)

        return DragAndDropPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_dropdown_list_link(self, page_name: str = "Dropdown List") -> DropdownListPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DROPDOWN_LINK)

        return DropdownListPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_dynamic_content_link(self, page_name: str = "Dynamic Content") -> DynamicContentPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DYNAMIC_CONTENT_LINK)

        return DynamicContentPage(self.driver, self.logger)

    @allure.step("Return object of {page_name} page")
    def get_dynamic_content_page(self, page_name: str = "Dynamic Content") -> DynamicContentPage:
        self.logger.info(f"Returning object of {page_name} page.")

        return DynamicContentPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_dynamic_controls_link(self, page_name: str = "Dynamic Controls") -> DynamicControlsPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DYNAMIC_CONTROLS_LINK)

        return DynamicControlsPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_dynamic_loading_link(self, page_name: str = "Dynamic Loading") -> DynamicLoadingPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.DYNAMIC_LOADING_LINK)

        return DynamicLoadingPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_entry_ad_link(self, page_name: str = "Entry Ad") -> EntryAdPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.ENTRY_AD_LINK)

        return EntryAdPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_exit_intent_link(self, page_name: str = "Exit Intent") -> ExitIntentPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.EXIT_INTENT_LINK)

        return ExitIntentPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_file_download_link(self, page_name: str = "File Download") -> FilesDownloadPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.FILE_DOWNLOAD_LINK)

        return FilesDownloadPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_file_upload_link(self, page_name: str = "File Upload") -> FileUploadPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.FILE_UPLOAD_LINK)

        return FileUploadPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_floating_menu_link(self, page_name: str = "Floating Menu") -> FloatingMenuPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.FLOATING_MENU_LINK)

        return FloatingMenuPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_form_authentication_link(self, page_name: str = "Form Authentication") -> FormAuthenticationPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.FORM_AUTH_LINK)

        return FormAuthenticationPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_frames_link(self, page_name: str = "Frames") -> FramesPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.FRAMES_LINK)

        return FramesPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_geolocation_link(self, page_name: str = "Geolocation") -> GeolocationPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.GEOLOCATION_LINK)

        return GeolocationPage(self.driver, self.logger, wait_for_load=True)

    @allure.step("Navigate to {page_name} page")
    def click_horizontal_slider_link(self, page_name: str = "Horizontal Slider") -> HorizontalSliderPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.HORIZONTAL_SLIDER_LINK)

        return HorizontalSliderPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_hovers_link(self, page_name: str = "Hovers") -> HoversPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.HOVERS_LINK)

        return HoversPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_infinite_scroll_link(self, page_name: str = "Infinite Scroll") -> InfiniteScrollPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.INFINITE_SCROLL_LINK)

        return InfiniteScrollPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_inputs_link(self, page_name: str = "Inputs") -> InputsPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.INPUTS_LINK)

        return InputsPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_jquery_ui_menus_link(self, page_name: str = "JQuery UI Menus") -> JQueryUIMenusPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.JQUERY_UI_MENUS_LINK)

        return JQueryUIMenusPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_javascript_alerts_link(self, page_name: str = "JavaScript Alerts") -> JavaScriptAlertsPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.JAVASCRIPT_ALERTS_LINK)

        return JavaScriptAlertsPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_javascript_onload_event_error_link(
        self, page_name: str = "JavaScript Alerts"
    ) -> JavaScriptOnloadRventErrorPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.JAVASCRIPT_ONLOAD_EVENT_ERROR_LINK)

        return JavaScriptOnloadRventErrorPage(self.driver, self.logger)

    @allure.step("Navigate to {page_name} page")
    def click_key_presses_link(self, page_name: str = "Key Presses") -> KeyPressesPage:
        self.logger.info(f"Navigating to {page_name} page.")
        self.click_element(MainPageLocators.KEY_PRESSES_LINK)

        return KeyPressesPage(self.driver, self.logger)
