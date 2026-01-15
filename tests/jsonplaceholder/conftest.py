"""
Pytest fixtures and configuration for JSONPlaceholder API tests.

This module provides:
- API configuration management via Pydantic settings
- HTTP session setup with retry logic
- Test context bundling for simplified test signatures
- Resource configuration objects for type-safe access to test data
"""

from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

import pytest
import requests
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tests.jsonplaceholder.api_test_suite.api_constants import JSONPlaceholderConfig

# ============================================================================
# CONFIGURATION
# ============================================================================


class APISettings(BaseSettings):
    """
    API configuration settings loaded from environment or defaults.

    Attributes:
        api_base_url: Base URL for the API (can be overridden via .env)
        request_timeout: Request timeout in seconds (can be overridden via .env)
    """

    api_base_url: str = JSONPlaceholderConfig.BASE_URL
    request_timeout: float = JSONPlaceholderConfig.REQUEST_TIMEOUT

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")


@dataclass
class ResourceConfigObject:
    """
    Configuration object for API resources.

    Provides type-safe access to resource-specific test data like valid IDs,
    expected counts, and edge case values.

    Attributes:
        list_count: Expected number of items when fetching all resources
        valid_id: ID of a known valid resource
        notfound_id: ID that should return 404
        negative_id: Negative ID for edge case testing (optional)
        string_id: String ID for invalid format testing (optional)
    """

    list_count: int
    valid_id: int
    notfound_id: int
    negative_id: int | None = None
    string_id: str | None = None

    @classmethod
    def from_dict(cls, config_dict: dict) -> ResourceConfigObject:
        """
        Create ResourceConfigObject from dictionary with validation.

        Args:
            config_dict: Dictionary containing resource configuration

        Returns:
            ResourceConfigObject instance

        Raises:
            ValueError: If required keys are missing
        """
        required = ["list_count", "valid_id", "notfound_id"]
        missing = [key for key in required if key not in config_dict]
        if missing:
            raise ValueError(f"Missing required config keys: {missing}")
        return cls(**config_dict)


@dataclass
class APITestContext:
    """
    Bundled context for API tests.

    Provides a single fixture that contains all necessary components for API testing,
    simplifying test signatures and making dependencies explicit.

    Attributes:
        session: HTTP session with retry logic configured
        base_url: Base URL for API endpoints
        timeout: Request timeout in seconds
    """

    session: requests.Session
    base_url: str
    timeout: float

    def get_resource_config(self, resource_name: str) -> ResourceConfigObject:
        """
        Get configuration for a specific resource.

        Args:
            resource_name: Name of the resource (e.g., "users", "posts")

        Returns:
            ResourceConfigObject with resource-specific test data

        Raises:
            ValueError: If resource configuration not found
        """
        config_dict = JSONPlaceholderConfig.RESOURCES.get(resource_name.lower())
        if not config_dict:
            raise ValueError(f"No configuration found for resource: {resource_name}")
        return ResourceConfigObject.from_dict(config_dict)


# ============================================================================
# FIXTURES - Settings
# ============================================================================


@pytest.fixture(scope="session")
def api_settings() -> APISettings:
    """
    Provide API settings for the test session.

    Session-scoped to load settings once per test run.
    Can be overridden via .env file.

    Returns:
        APISettings instance with base URL and timeout
    """
    return APISettings()


@pytest.fixture
def api_base_url(api_settings: APISettings) -> str:
    """
    Provide the API base URL.

    Args:
        api_settings: API settings fixture

    Returns:
        Base URL string
    """
    return api_settings.api_base_url


# ============================================================================
# FIXTURES - HTTP Session
# ============================================================================


@pytest.fixture(scope="function")
def api_session() -> Generator[Session, Any, None]:
    """
    Provide an HTTP session with retry logic.

    Function-scoped to ensure test isolation (new session per test).
    Configured with:
    - JSON accept header
    - Retry strategy (3 attempts, exponential backoff)
    - Auto-retry on server errors (429, 5xx)

    Yields:
        requests.Session: Configured session

    Cleanup:
        Automatically closes session after test
    """
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    # Configure retry strategy for resilience
    retry_strategy = Retry(
        total=3,  # 3 retry attempts
        backoff_factor=0.3,  # Wait 0.3s, 0.6s, 1.2s between retries
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    yield session

    # Cleanup: close session after test
    session.close()


# ============================================================================
# FIXTURES - Test Context
# ============================================================================


@pytest.fixture
def api_context(api_session: requests.Session, api_base_url: str, api_settings: APISettings) -> APITestContext:
    """
    Provide bundled API test context.

    Combines session, base URL, timeout, and resource config access into
    a single fixture for simplified test signatures.

    Args:
        api_session: HTTP session fixture
        api_base_url: Base URL fixture
        api_settings: Settings fixture (for timeout)

    Returns:
        APITestContext with all test dependencies

    Example:
        def test_get_user(api_context):
            config = api_context.get_resource_config("users")
            response = api_context.session.get(
                f"{api_context.base_url}/users/{config.valid_id}",
                timeout=api_context.timeout
            )
    """
    return APITestContext(session=api_session, base_url=api_base_url, timeout=api_settings.request_timeout)
