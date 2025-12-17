from typing import Literal

from pydantic import AnyUrl, Field, PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        case_sensitive=False,
        validate_default=True,
    )

    # Environment
    ENV: Literal["dev", "staging", "ci", "prod"] = "dev"

    # Browser & SeleniumBase
    BROWSER: Literal["chrome", "firefox"] = "chrome"
    HEADLESS: bool = Field(default=True, description="Run in headless mode")
    MAXIMIZED: bool = False
    UC_MODE: bool = True

    # Timeouts
    SHORT_TIMEOUT: PositiveInt = Field(default=5, ge=1, le=30)
    LONG_TIMEOUT: PositiveInt = Field(default=15, ge=5, le=60)

    # URLs
    BASE_URL: AnyUrl = Field(
        default="https://the-internet.herokuapp.com/", env="BASE_URL", description="Application Under Test base URL"
    )
    ALLURE_SERVER_URL: AnyUrl | None = Field(
        default=None, env="ALLURE_SERVER_URL", description="Allure Server for report upload (optional in local/CI)"
    )

    # Test data
    TEST_USERNAME: str = Field(..., env="TEST_USERNAME", min_length=1)
    TEST_PASSWORD: SecretStr = Field(..., env="TEST_PASSWORD", min_length=8)

    # Geolocation for tests
    GEOLOCATION_LAT: float = Field(
        default=32.0853,
        ge=-90.0,
        le=90.0,
        env="GEOLOCATION_LAT",
        description="Latitude for browser geolocation override (Tel Aviv default)",
    )
    GEOLOCATION_LON: float = Field(
        default=34.7818,
        ge=-180.0,
        le=180.0,
        env="GEOLOCATION_LON",
        description="Longitude for browser geolocation override (Tel Aviv default)",
    )


# Singleton instance
try:
    settings = Settings()
except Exception as exc:
    import logging

    log = logging.getLogger(__name__)
    log.error("Failed to initialize settings: %s", exc)
    raise

__all__ = ["settings"]
