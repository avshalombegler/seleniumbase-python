import re
from urllib.parse import urlparse

from pydantic import BaseModel, EmailStr, Field, field_validator


class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catch_phrase: str = Field(..., alias="catchPhrase")
    bs: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    website: str
    company: Company

    model_config = {"populate_by_name": True}

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """
        Ensure phone has at least 10 digits.

        Accepts formats like: 1-770-736-8031, (123) 456-7890, +1234567890
        Validates that after removing non-digits, at least 10 remain.

        Raises:
            ValueError: If fewer than 10 digits found
        """
        digits = re.sub(r"\D", "", v)
        if len(digits) < 10:
            raise ValueError(f"Phone must have at least 10 digits, got {len(digits)} in '{v}'")
        return v

    # THIS VALIDATOR MAY NEED TO CHANGE
    @field_validator("website")
    @classmethod
    def validate_website(cls, v: str) -> str:
        """Ensure website is a valid domain or URL."""

        # If no scheme, assume https://
        if not v.startswith(("http://", "https://")):
            v = f"https://{v}"

        parsed = urlparse(v)
        if not parsed.netloc or not re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", parsed.netloc):
            raise ValueError(f"Invalid website: {v}")
        return v
