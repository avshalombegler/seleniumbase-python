from __future__ import annotations

from typing import TYPE_CHECKING, Any

import allure
import structlog
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from seleniumbase import BaseCase

from src.config import settings

if TYPE_CHECKING:
    from logging import Logger

    from pydantic import AnyUrl

    Locator = dict[str, str]
else:
    Locator = Any


class BasePage:
    """
    Base page object providing common web automation methods using SeleniumBase.

    Method Categories:
    1. Initialization
    2. Wait Methods
    3. Navigation Methods
    4. Frame/Window Methods
    5. Element Interaction Methods
    6. Element State Methods
    7. Element Query Methods
    8. Utility Methods
    """

    # ============================================================================
    # INITIALIZATION
    # ============================================================================

    def __init__(self, base_case: BaseCase, logger: Logger | None = None) -> None:
        # Accept an optional `logger` for backward compatibility with pages
        # that pass a logger to `super().__init__`. We derive our structured
        # logger instance below regardless of the passed value.
        self.driver = base_case
        self.actions = ActionChains(self.driver.driver)
        self.logger = structlog.get_logger(self.__class__.__name__).bind(page=self.__class__.__name__)
        self.short_wait = settings.SHORT_TIMEOUT
        self.long_wait = settings.LONG_TIMEOUT
        self.base_url = settings.BASE_URL

    # ============================================================================
    # WAIT METHODS
    # ============================================================================

    def wait_for_page_to_load(
        self, indicator_locator: Locator | None, timeout: int | float | None = None, use_ready_state: bool = True
    ) -> None:
        """
        Wait for page to load. Combines a document ready-state check with an optional
        page-specific indicator element.

        Args:
            indicator_locator: String locator for the indicator element
            timeout: Optional timeout in seconds (defaults to LONG_TIMEOUT)
            use_ready_state: Boolean for document ready-state check

        Raises:
            TimeoutException: If the indicator is not visible within timeout
            NoSuchElementException: If the locator is invalid
        """
        timeout = timeout or self.long_wait

        if use_ready_state:
            try:
                self.driver.wait_for_ready_state_complete()
            except Exception as e:
                self.logger.debug(f"readyState check failed or timed out: {e}")

        if indicator_locator:
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

    def wait_for_file_to_download(self, filename: str, timeout: int | float | None = None) -> bool:
        """
        Wait for file to finish download.

        Args:
            filename: Name of the file to wait for
            timeout: Optional timeout in seconds

        Returns:
            bool: True if file download completed, False if timeout
        """
        import time

        timeout = timeout or self.short_wait
        self.logger.info(f"Waiting for file '{filename}' to download (timeout: {timeout}s).")

        start_time = time.time()
        poll_interval = 0.5  # Check every 500ms

        try:
            while time.time() - start_time < timeout:
                if self.driver.is_downloaded_file_present(filename):
                    elapsed = time.time() - start_time
                    self.logger.debug(f"File '{filename}' downloaded successfully after {elapsed:.2f}s.")
                    return True
                time.sleep(poll_interval)

            self.logger.warning(f"File '{filename}' not found after {timeout}s timeout.")
            return False
        except Exception as e:
            self.logger.error(f"Error while waiting for file '{filename}': {str(e)}")
            return False

    # ============================================================================
    # NAVIGATION METHODS
    # ============================================================================

    @allure.step("Navigate to the page")
    def navigate_to(self, url: str) -> None:
        self.logger.info(f"Navigating to url: {url}.")
        self.driver.open(url)
        self.logger.info("Navigation completed.")

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

    def switch_to_frame(self, locator: Locator) -> None:
        """
        Switch to an iframe or frame.

        Args:
            locator: Frame element locator dict

        Raises:
            Exception: If frame switch fails
        """
        try:
            self.driver.switch_to_frame(locator["selector"])
            self.logger.debug(f"Switched to frame with locator '{locator}'.")
            return
        except Exception as e:
            self.logger.error(f"Failed to switch to frame '{locator}': {str(e)}")
            raise

    # ============================================================================
    # ELEMENT INTERACTION METHODS
    # ============================================================================

    def click_element(self, locator: Locator) -> None:
        """
        Click an element (single attempt).

        Args:
            locator: Element locator dict

        Raises:
            Exception: If click fails
        """
        try:
            self.driver.click(**locator)
            self.logger.debug(f"Clicked on element with locator '{locator}'.")
            return
        except Exception as e:
            self.logger.error(f"Failed to click element '{locator}': {str(e)}")
            raise

    def send_keys_to_element(self, locator: Locator, text: str) -> None:
        """
        Send keys to an element (single attempt).

        Args:
            locator: Element locator dict
            text: Text to send to the element

        Raises:
            Exception: If send keys fails
        """
        self.logger.info(f"Sending keys '{text}' to element '{locator}'.")
        try:
            self.driver.type(text=text, **locator)
            self.logger.debug(f"Sent keys to '{locator}'.")
            return
        except Exception as e:
            self.logger.error(f"Failed to send keys to '{locator}': {str(e)}")
            raise

    def perform_right_click(self, locator: Locator) -> None:
        """
        Perform right-click on an element (single attempt).

        Args:
            locator: Element locator dict

        Raises:
            Exception: If right-click fails
        """
        self.logger.info(f"Performing right-click on element '{locator}'.")
        try:
            elem = self.wait_for_visibility(locator)
            self.actions.context_click(elem).perform()
            self.logger.debug(f"Right-clicked on '{locator}'.")
            return
        except Exception as e:
            self.logger.error(f"Failed to perform right-click on '{locator}': {str(e)}")
            raise

    def download_file(self, locator: Locator, file_name: str, timeout: int | float | None = None) -> None:
        """
        Click a download link for a specific file (single attempt).

        Args:
            locator: Download link locator dict with selector having {file_name} placeholder
            file_name: Name of the file to download
            timeout: Optional timeout for waiting

        Raises:
            Exception: If download click fails
        """
        self.logger.info(f"Downloading file '{file_name}'.")
        formatted_locator = self.format_locator(locator, file_name=file_name)
        try:
            self.driver.click(**formatted_locator)
            self.logger.debug(f"Clicked download link for file: {file_name}")
            return
        except Exception as e:
            self.logger.error(f"Failed to click download link '{formatted_locator}': {str(e)}")
            raise

    # ============================================================================
    # ELEMENT STATE METHODS
    # ============================================================================

    def is_element_visible(self, locator: Locator, timeout: int | float | None = None) -> bool:
        """
        Check if element is visible.

        Fast-path (no wait): provide timeout=0 -> uses driver.is_element_visible() when available.
        Default: waits up to short_wait (or provided timeout) with wait_for_element_visible.
        """
        timeout = timeout if timeout is not None else self.short_wait
        try:
            # Fast immediate check (no waiting)
            if timeout == 0 and hasattr(self.driver, "is_element_visible"):
                visible = bool(self.driver.is_element_visible(**locator))
                self.logger.debug(f"is_element_visible({locator}) -> {visible} (fast)")
                return visible

            # Wait for visibility
            self.driver.wait_for_element_visible(**locator, timeout=timeout)
            self.logger.debug(f"is_element_visible({locator}) -> True (waited)")
            return True

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug(f"is_element_visible({locator}) -> False ({e})")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error checking visibility for {locator}: {e}")
            raise

    def is_element_selected(self, locator: Locator, timeout: int | float | None = None) -> bool:
        """
        Check if element is selected.

        Fast-path (no wait): provide timeout=0 -> uses driver.is_selected() when available.
        Default: waits up to short_wait (or provided timeout) for visibility then checks selected state.
        """
        timeout = timeout if timeout is not None else self.short_wait
        self.logger.info(f"Checking selected state for element '{locator}'.")
        try:
            if timeout == 0 and hasattr(self.driver, "is_selected"):
                selected = bool(self.driver.is_selected(**locator))
                self.logger.debug(f"is_element_selected({locator}) -> {selected} (fast)")
                return selected

            # Wait for visibility then check selected
            self.driver.wait_for_element_visible(**locator, timeout=timeout)
            selected = bool(self.driver.is_selected(**locator))
            self.logger.debug(f"is_element_selected({locator}) -> {selected} (waited)")
            return selected
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug(f"is_element_selected({locator}) -> False ({e})")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error checking selected state for {locator}: {e}")
            raise

    def is_element_enabled(self, locator: Locator, timeout: int | float | None = None) -> bool:
        """
        Check if element is enabled.

        Fast-path (no wait): provide timeout=0 -> uses driver.is_element_enabled() when available.
        Default: waits up to short_wait (or provided timeout) for visibility then checks enabled state.
        """
        timeout = timeout if timeout is not None else self.short_wait
        self.logger.info(f"Checking enabled state for element '{locator}'.")
        try:
            if timeout == 0 and hasattr(self.driver, "is_element_enabled"):
                enabled = bool(self.driver.is_element_enabled(**locator))
                self.logger.debug(f"is_element_enabled({locator}) -> {enabled} (fast)")
                return enabled

            # Wait for visibility then check enabled
            self.driver.wait_for_element_visible(**locator, timeout=timeout)
            enabled = bool(self.driver.is_element_enabled(**locator))
            self.logger.debug(f"is_element_enabled({locator}) -> {enabled} (waited)")
            return enabled
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug(f"is_element_enabled({locator}) -> False ({e})")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error checking enabled state for {locator}: {e}")
            raise

    # ============================================================================
    # ELEMENT QUERY METHODS
    # ============================================================================

    def get_dynamic_element_text(self, locator: Locator, timeout: int | float | None = None) -> str:
        """
        Get text from an element (single attempt).

        Args:
            locator: Element locator dict
            timeout: Optional timeout in seconds (defaults to LONG_TIMEOUT)

        Returns:
            str: Text content of the element

        Raises:
            Exception: If element cannot be found
        """
        timeout = timeout or self.long_wait

        self.logger.debug(f"Waiting for '{locator}' visibility.")
        try:
            self.driver.wait_for_element_visible(**locator, timeout=timeout)
            text = self.driver.get_text(**locator)
            self.logger.debug(f"Retrieved text: '{text}'.")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text for '{locator}': {str(e)}")
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

    def get_element_attr(self, locator: Locator, attribute: str) -> Any | None:
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

    def get_base_url(self) -> str | AnyUrl:
        """
        Get the base URL from configuration.

        Returns:
            str: Base URL
        """
        url = self.base_url
        self.logger.debug(f"Base URL: {url}")
        return url

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def format_locator(self, locator: Locator, **kwargs: Any) -> Locator:
        """
        Format a locator's selector string with provided keyword arguments and return the updated locator.

        Args:
            locator: Original locator dict with 'selector' and 'by' keys.
            **kwargs: Keyword arguments for formatting the selector string.

        Returns:
            Locator: Updated locator dict with the formatted selector.
        """
        formatted_selector = locator["selector"].format(**kwargs)
        return {"selector": formatted_selector, "by": locator["by"]}
