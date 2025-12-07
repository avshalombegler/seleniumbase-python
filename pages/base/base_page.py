from __future__ import annotations

import time
from logging import Logger
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

import allure
from selenium.webdriver.common.action_chains import ActionChains
from seleniumbase import BaseCase

from config.env_config import BASE_URL, LONG_TIMEOUT, SHORT_TIMEOUT
from utils.logging_helper import get_logger

if TYPE_CHECKING:
    Locator = dict[str, str]
else:
    Locator = Any


class BasePage:
    """
    Base page object providing common web automation methods using SeleniumBase.

    Method Categories:
    1. Initialization
    2. Core Helpers (Private)
    3. Wait Methods
    4. Navigation Methods
    5. Frame/Window Methods
    6. Element Interaction Methods
    7. Element State Methods
    8. Element Query Methods
    9. Utility Methods
    """

    # ============================================================================
    # INITIALIZATION
    # ============================================================================

    def __init__(self, base_case: BaseCase, logger: Logger | None = None) -> None:
        self.driver = base_case
        self.actions = ActionChains(self.driver.driver)
        self.logger = logger if logger is not None else get_logger(self.__class__.__name__)
        self.short_wait = SHORT_TIMEOUT
        self.long_wait = LONG_TIMEOUT
        self.base_url = BASE_URL

    # ============================================================================
    # WAIT METHODS
    # ============================================================================

    def wait_for_page_to_load(self, indicator_locator: Locator, timeout: int | float | None = None) -> None:
        """
        Wait for page to load by checking visibility of an indicator element.

        Args:
            indicator_locator: String locator for the indicator element
            timeout: Optional timeout in seconds (defaults to LONG_TIMEOUT)

        Raises:
            TimeoutException: If the indicator is not visible within timeout
            NoSuchElementException: If the locator is invalid
        """
        timeout = timeout or self.long_wait
        self.logger.info(f"Waiting for page to load with indicator '{indicator_locator}' for {timeout}s.")
        self.driver.wait_for_element_visible(**indicator_locator, timeout=timeout)
        self.logger.info(f"Page loaded successfully with indicator '{indicator_locator}'.")

    def wait_for_visibility(self, locator: Locator, timeout: int | float | None = None) -> Any:
        """
        Wait for element to be visible.

        Args:
            locator: Element locator dict
            timeout: Optional timeout in seconds

        Returns:
            WebElement: The visible element

        Raises:
            TimeoutException: If element not visible within timeout
        """
        timeout = timeout or self.short_wait
        return self.driver.wait_for_element_visible(**locator, timeout=timeout)

    def wait_for_invisibility(self, locator: Locator, timeout: int | float | None = None) -> bool:
        """
        Wait for element to become invisible.

        Args:
            locator: Element locator dict
            timeout: Optional timeout in seconds

        Returns:
            bool: True if element became invisible

        Raises:
            TimeoutException: If element remains visible after timeout
        """
        timeout = timeout or self.short_wait
        return self.driver.wait_for_element_not_visible(**locator, timeout=timeout)

    def wait_for_loader(self, locator: Locator, timeout: int | float | None = None) -> bool:
        """
        Wait for loading indicator to appear and disappear.

        Args:
            locator: Loader element locator dict
            timeout: Optional timeout in seconds

        Returns:
            bool: True if loader completed, False if timeout
        """
        timeout = timeout or self.short_wait
        self.logger.info("Waiting for loader to complete.")

        try:
            half_timeout = timeout / 2
            self.driver.wait_for_element_visible(**locator, timeout=half_timeout)
            self.driver.wait_for_element_not_visible(**locator, timeout=half_timeout)
            self.logger.debug("Loader completed successfully.")
            return True
        except Exception as e:
            self.logger.warning(f"Loader timeout after {timeout}s: {str(e)}")
            return False

    # ============================================================================
    # NAVIGATION METHODS
    # ============================================================================

    @allure.step("Navigate to the page")
    def navigate_to(self, path: str = "") -> None:
        url = urljoin(self.base_url, path)
        self.driver.open(url)

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.logger.info("Refreshing page.")
        self.driver.refresh()
        self.logger.info("Page refreshed.")

    def navigate_back(self) -> None:
        """Navigate back."""
        self.logger.info("Navigating back.")
        self.driver.go_back()
        self.logger.info("Navigation completed.")

    # ============================================================================
    # FRAME/WINDOW METHODS
    # ============================================================================

    def switch_to_frame(self, locator: Locator, retry: int = 2) -> None:
        """
        Switch to an iframe or frame with retry.

        Args:
            locator: Frame element locator dict
            retry: Number of retry attempts

        Raises:
            Exception: If frame switch fails after all retries
        """
        for attempt in range(retry):
            try:
                self.driver.switch_to_frame(locator["selector"])
                self.logger.debug(f"Switched to frame with locator '{locator}'.")
                return
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1}/{retry} failed for frame '{locator}': {str(e)}")
                if attempt == retry - 1:
                    self.logger.error(f"All retries failed for frame '{locator}'")
                    raise

    # ============================================================================
    # ELEMENT INTERACTION METHODS
    # ============================================================================

    def click_element(self, locator: Locator, retry: int = 2) -> None:
        """
        Click an element with retry for stale/intercepted exceptions.

        Args:
            locator: Element locator dict
            retry: Number of retry attempts

        Raises:
            Exception: If click fails after all retries
        """
        for attempt in range(retry):
            try:
                self.driver.click(**locator)
                self.logger.debug(f"Clicked on element with locator '{locator}'.")
                return
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1}/{retry} failed for click '{locator}': {str(e)}")
                if attempt == retry - 1:
                    self.logger.error(f"All retries failed for click '{locator}'")
                    raise

    def send_keys_to_element(self, locator: Locator, text: str, retry: int = 2) -> None:
        """
        Send keys to an element with retry.

        Args:
            locator: Element locator dict
            text: Text to send to the element
            retry: Number of retry attempts

        Raises:
            Exception: If send keys fails after all retries
        """
        self.logger.info(f"Sending keys '{text}' to element '{locator}'.")
        for attempt in range(retry):
            try:
                self.driver.type(text=text, **locator)
                self.logger.debug(f"Sent keys to '{locator}'.")
                return
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1}/{retry} failed for send keys '{locator}': {str(e)}")
                if attempt == retry - 1:
                    self.logger.error(f"All retries failed for send keys '{locator}'")
                    raise

    def perform_right_click(self, locator: Locator, retry: int = 2) -> None:
        """
        Perform right-click on an element with retry.

        Args:
            locator: Element locator dict
            retry: Number of retry attempts

        Raises:
            Exception: If right-click fails after all retries
        """
        self.logger.info(f"Performing right-click on element '{locator}'.")
        for attempt in range(retry):
            try:
                # self.driver.right_click(**locator)
                elem = self.wait_for_visibility(locator)
                self.actions.context_click(elem).perform()
                self.logger.debug(f"Right-clicked on '{locator}'.")
                return
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1}/{retry} failed for right-click '{locator}': {str(e)}")
                if attempt == retry - 1:
                    self.logger.error(f"All retries failed for right-click '{locator}'")
                    raise

    def download_file(
        self, locator: Locator, file_name: str, timeout: int | float | None = None, retry: int = 2
    ) -> None:
        """
        Click a download link for a specific file with retry.

        Args:
            locator: Download link locator dict with selector having {file_name} placeholder
            file_name: Name of the file to download
            timeout: Optional timeout for waiting
            retry: Number of retry attempts

        Raises:
            Exception: If download click fails after all retries
        """
        self.logger.info(f"Downloading file '{file_name}'.")
        formatted_locator = self.format_locator(locator, file_name=file_name)

        for attempt in range(retry):
            try:
                self.driver.wait_for_element_visible(**formatted_locator, timeout=timeout or self.short_wait)
                self.driver.click(**formatted_locator)
                self.logger.debug(f"Clicked download link for file: {file_name}")
                return
            except Exception as e:
                self.logger.warning(
                    f"Attempt {attempt + 1}/{retry} failed for download '{formatted_locator}': {str(e)}"
                )
                if attempt == retry - 1:
                    self.logger.error(f"All retries failed for download '{formatted_locator}'")
                    raise

    # ============================================================================
    # ELEMENT STATE METHODS
    # ============================================================================

    def is_element_visible(self, locator: Locator, timeout: int | float | None = None) -> bool:
        """
        Check if element is visible (in DOM and displayed).

        Args:
            locator: Element locator dict
            timeout: Optional timeout for waiting

        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            self.driver.wait_for_element_visible(**locator, timeout=timeout or self.short_wait)
            return True
        except Exception:
            return False

    def is_element_selected(self, locator: Locator, timeout: int | float | None = None, retry: int = 2) -> bool:
        """
        Check if element is selected (e.g., checkbox, radio button).

        Args:
            locator: Element locator dict
            timeout: Optional timeout for waiting
            retry: Number of retry attempts

        Returns:
            bool: True if element is selected, False otherwise
        """
        self.logger.info(f"Checking selected state for element '{locator}'.")
        for attempt in range(retry):
            try:
                return self.driver.is_selected(**locator)
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1}/{retry} failed for selected check '{locator}': {str(e)}")
                if attempt == retry - 1:
                    self.logger.error(f"All retries failed for selected check '{locator}'")
                    return False

    def is_element_enabled(self, locator: Locator, timeout: int | float | None = None, retry: int = 2) -> bool:
        """
        Check if element is enabled (not disabled).

        Args:
            locator: Element locator dict
            timeout: Optional timeout for waiting
            retry: Number of retry attempts

        Returns:
            bool: True if element is enabled, False otherwise
        """
        self.logger.info(f"Checking enabled state for element '{locator}'.")
        for attempt in range(retry):
            try:
                return self.driver.is_element_enabled(**locator)
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1}/{retry} failed for enabled check '{locator}': {str(e)}")
                if attempt == retry - 1:
                    self.logger.error(f"All retries failed for enabled check '{locator}'")
                    return False

    # ============================================================================
    # ELEMENT QUERY METHODS
    # ============================================================================

    def get_dynamic_element_text(self, locator: Locator, timeout: int | float | None = None, retry: int = 2) -> str:
        """
        Get text from an element with retry for stale elements.

        Args:
            locator: Element locator dict
            timeout: Optional timeout in seconds (defaults to LONG_TIMEOUT)
            retry: Number of retry attempts for stale elements

        Returns:
            str: Text content of the element

        Raises:
            Exception: If element cannot be found after retries
        """
        timeout = timeout or self.long_wait

        self.logger.debug(f"Waiting for '{locator}' visibility.")
        for attempt in range(retry):
            try:
                self.driver.wait_for_element_visible(**locator, timeout=timeout)
                text = self.driver.get_text(**locator)
                self.logger.debug(f"Retrieved text: '{text}'.")
                return text
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1}/{retry} failed to get text for '{locator}': {str(e)}")
                if attempt == retry - 1:
                    self.logger.error(f"Failed to get text for '{locator}' after {retry} attempts")
                    raise

    def get_all_elements(self, locator: Locator) -> list:
        """
        Get all elements matching the locator.

        Args:
            locator: Element locator dict

        Returns:
            List[WebElement]: List of matching elements (empty if none found)
        """
        try:
            elements = self.driver.find_elements(**locator)
            return elements
        except Exception:
            self.logger.debug(f"No elements found with locator {locator}.")
            return []

    def get_number_of_elements(self, locator: Locator) -> int:
        """
        Count the number of elements matching the locator.

        Args:
            locator: Element locator dict

        Returns:
            int: Number of matching elements
        """
        self.logger.info(f"Counting elements with locator: '{locator}'.")
        elements = self.get_all_elements(locator)
        count = len(elements)
        self.logger.debug(f"Found {count} elements with locator '{locator}'.")
        return count

    def get_element_attr_js(self, locator: Locator, attribute: str) -> Any | None:
        """
        Get element attribute using JavaScript execution.

        Args:
            web_element: WebElement to get attribute from
            attr: Attribute name to retrieve

        Returns:
            Any: Attribute value or None if execution failed
        """
        try:
            result = self.driver.get_attribute(**locator, attribute=attribute)
            self.logger.debug(f"Retrieved {attribute}={result} for element.")
            return result
        except Exception as e:
            self.logger.error(f"Failed to get {attribute}: {str(e)}")
            return None

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            str: Current URL
        """
        url = self.driver.get_current_url()
        self.logger.debug(f"Current URL: {url}")
        return url

    def get_base_url(self) -> str:
        """
        Get the base URL from configuration.

        Returns:
            str: Base URL
        """
        url = self.base_url
        self.logger.debug(f"Base URL: {url}")
        return url

    def get_page_source(self, timeout: int | float | None = None, lowercase: bool = False) -> str:
        """
        Get the page source with optional wait for page readiness.

        Args:
            timeout: Optional timeout for waiting for document ready state
            lowercase: If True, return lowercase version of page source

        Returns:
            str: Page source HTML (optionally lowercased)
        """
        timeout = timeout or self.long_wait
        self.logger.info("Getting page source.")

        try:
            # Wait for document ready state
            self.driver.wait_for_ready_state_complete(timeout=timeout)

            time.sleep(1)
            page_source = self.driver.get_page_source()

            if lowercase:
                page_source = page_source.lower()
                self.logger.debug("Retrieved page source (lowercased).")
            else:
                self.logger.debug("Retrieved page source.")

            return page_source

        except Exception as e:
            self.logger.warning(f"Error getting page source: {str(e)}")
            # Return page source anyway
            page_source = self.driver.get_page_source()
            return page_source.lower() if lowercase else page_source

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def check_accessibility(self) -> None:
        """
        Run accessibility check using axe-core (built into SeleniumBase).

        Raises:
            Exception: If accessibility violations are found
        """
        self.logger.info("Running accessibility check.")
        try:
            self.driver.check_accessibility()
            self.logger.info("Accessibility check passed.")
        except Exception as e:
            self.logger.error(f"Accessibility check failed: {str(e)}")
            raise

    def check_visual_baseline(self, name: str) -> None:
        """
        Check visual baseline for regression testing (SeleniumBase feature).

        Args:
            name: Name for the baseline screenshot

        Raises:
            Exception: If visual regression detected
        """
        self.logger.info(f"Checking visual baseline: {name}")
        try:
            self.driver.check_window(name=name)
            self.logger.info(f"Visual baseline check passed for {name}.")
        except Exception as e:
            self.logger.error(f"Visual baseline check failed for {name}: {str(e)}")
            raise

    def get_files_in_directory(self, directory_path: Path) -> list:
        """
        Get all files in a directory.

        Args:
            directory_path: Path to the directory

        Returns:
            list: List of file paths in the directory
        """
        return [item for item in directory_path.iterdir() if item.is_file()]

    def format_locator(self, locator: Locator, **kwargs) -> Locator:
        """
        Format a locator's selector string with provided keyword arguments and return the updated locator.

        Args:
            locator: Original locator dict with 'selector' and 'by' keys.
            **kwargs: Keyword arguments for formatting the selector string.

        Returns:
            Locator: Updated locator dict with the formatted selector.

        Raises:
            KeyError: If a required placeholder in the selector is missing from kwargs.
        """
        formatted_selector = locator["selector"].format(**kwargs)
        return {"selector": formatted_selector, "by": locator["by"]}
