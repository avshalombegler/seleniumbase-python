"""
Module containing locators for Main Page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class MainPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".heading", "by": By.CSS_SELECTOR}

    AB_TESTING_LINK: Locator = {"selector": "A/B Testing", "by": By.LINK_TEXT}
    ADD_REMOVE_ELEMENTS_LINK: Locator = {"selector": "Add/Remove Elements", "by": By.LINK_TEXT}
    BROKEN_IMAGES_LINK: Locator = {"selector": "Broken Images", "by": By.LINK_TEXT}
    CHALLENGING_DOM_LINK: Locator = {"selector": "Challenging DOM", "by": By.LINK_TEXT}
    CHECKBOXES_LINK: Locator = {"selector": "Checkboxes", "by": By.LINK_TEXT}
    CONTEXT_MENU_LINK: Locator = {"selector": "Context Menu", "by": By.LINK_TEXT}
    DRAG_AND_DROP_LINK: Locator = {"selector": "Drag and Drop", "by": By.LINK_TEXT}
    DROPDOWN_LINK: Locator = {"selector": "Dropdown", "by": By.LINK_TEXT}
    DYNAMIC_CONTENT_LINK: Locator = {"selector": "Dynamic Content", "by": By.LINK_TEXT}
    DYNAMIC_CONTROLS_LINK: Locator = {"selector": "Dynamic Controls", "by": By.LINK_TEXT}
    DYNAMIC_LOADING_LINK: Locator = {"selector": "Dynamic Loading", "by": By.LINK_TEXT}
    ENTRY_AD_LINK: Locator = {"selector": "Entry Ad", "by": By.LINK_TEXT}
    EXIT_INTENT_LINK: Locator = {"selector": "Exit Intent", "by": By.LINK_TEXT}
    FILE_DOWNLOAD_LINK: Locator = {"selector": "File Download", "by": By.LINK_TEXT}
    FILE_UPLOAD_LINK: Locator = {"selector": "File Upload", "by": By.LINK_TEXT}
    FLOATING_MENU_LINK: Locator = {"selector": "Floating Menu", "by": By.LINK_TEXT}
    FORM_AUTH_LINK: Locator = {"selector": "Form Authentication", "by": By.LINK_TEXT}
    FRAMES_LINK: Locator = {"selector": "Frames", "by": By.LINK_TEXT}
    GEOLOCATION_LINK: Locator = {"selector": "Geolocation", "by": By.LINK_TEXT}
    HORIZONTAL_SLIDER_LINK: Locator = {"selector": "Horizontal Slider", "by": By.LINK_TEXT}
    HOVERS_LINK: Locator = {"selector": "Hovers", "by": By.LINK_TEXT}
    INFINITE_SCROLL_LINK: Locator = {"selector": "Infinite Scroll", "by": By.LINK_TEXT}
    INPUTS_LINK: Locator = {"selector": "Inputs", "by": By.LINK_TEXT}
    JQUERY_UI_MENUS_LINK: Locator = {"selector": "JQuery UI Menus", "by": By.LINK_TEXT}
    JAVASCRIPT_ALERTS_LINK: Locator = {"selector": "JavaScript Alerts", "by": By.LINK_TEXT}
    JAVASCRIPT_ONLOAD_EVENT_ERROR_LINK: Locator = {"selector": "JavaScript onload event error", "by": By.LINK_TEXT}
    KEY_PRESSES_LINK: Locator = {"selector": "Key Presses", "by": By.LINK_TEXT}
    LARGE_AND_DEEP_DOM_LINK: Locator = {"selector": "Large & Deep DOM", "by": By.LINK_TEXT}
    MULTIPLE_WINDOWS_LINK: Locator = {"selector": "Multiple Windows", "by": By.LINK_TEXT}
    NOTIFICATION_MESSAGES_LINK: Locator = {"selector": "Notification Messages", "by": By.LINK_TEXT}
    REDIRECT_LINK_LINK: Locator = {"selector": "Redirect Link", "by": By.LINK_TEXT}
    SHADOW_DOM_LINK: Locator = {"selector": "Shadow DOM", "by": By.LINK_TEXT}
    SHIFTING_CONTENT_LINK: Locator = {"selector": "Shifting Content", "by": By.LINK_TEXT}
    SORTABLE_DATA_TABLES_LINK: Locator = {"selector": "Sortable Data Tables", "by": By.LINK_TEXT}
