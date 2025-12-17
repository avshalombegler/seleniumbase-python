from enum import Enum

from pydantic import AnyUrl, Field, PositiveInt, field_validator
from pydantic import SecretStr as PydanticSecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvEnum(str, Enum):
    dev = "dev"
    staging = "staging"
    ci = "ci"
    prod = "prod"


class BrowserEnum(str, Enum):
    chrome = "chrome"
    firefox = "firefox"


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
    ENV: EnvEnum = EnvEnum.dev

    # Browser & SeleniumBase
    BROWSER: BrowserEnum = BrowserEnum.chrome
    HEADLESS: bool = Field(default=True, description="Run in headless mode")
    MAXIMIZED: bool = False
    UC_MODE: bool = True

    # Timeouts
    SHORT_TIMEOUT: PositiveInt = Field(default=5, ge=1, le=30)
    LONG_TIMEOUT: PositiveInt = Field(default=15, ge=5, le=60)

    # URLs
    BASE_URL: str | AnyUrl = Field(
        default="https://the-internet.herokuapp.com/",
        description="Application Under Test base URL",
    )
    ALLURE_SERVER_URL: AnyUrl | None = Field(
        default=None,
        description="Allure Server for report upload (optional in local/CI)",
    )

    # Test data
    TEST_USERNAME: str | None = Field(default=None, min_length=1)
    TEST_PASSWORD: PydanticSecretStr | None = Field(default=None)

    # Geolocation for tests
    GEOLOCATION_LAT: float = Field(
        default=32.0853,
        ge=-90.0,
        le=90.0,
        description="Latitude for browser geolocation override (Tel Aviv default)",
    )
    GEOLOCATION_LON: float = Field(
        default=34.7818,
        ge=-180.0,
        le=180.0,
        description="Longitude for browser geolocation override (Tel Aviv default)",
    )

    # Validators
    @field_validator("BASE_URL", mode="before")
    @classmethod
    def _normalize_base_url(cls, v: str | AnyUrl) -> str:
        s = str(v)
        if not s.endswith("/"):
            s = s + "/"
        return s

    @field_validator("TEST_PASSWORD", mode="after")
    @classmethod
    def _validate_password_length(cls, v: PydanticSecretStr) -> PydanticSecretStr:
        # Ensure SecretStr meets minimum length (Field(min_length) may not validate SecretStr length)
        raw = v.get_secret_value() if hasattr(v, "get_secret_value") else str(v)
        if len(raw) < 8:
            raise ValueError("TEST_PASSWORD must be at least 8 characters")
        return v


# Singleton instance
try:
    settings = Settings()
except Exception as exc:
    import structlog

    log = structlog.get_logger(__name__)
    log.error("Failed to initialize settings:", error=str(exc))
    raise

__all__ = ["settings"]
