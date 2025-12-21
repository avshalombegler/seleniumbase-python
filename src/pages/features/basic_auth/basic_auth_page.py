from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urljoin

import allure
import requests
from bs4 import BeautifulSoup

from src.pages.base.base_page import BaseCase, BasePage

if TYPE_CHECKING:
    from typing import Any


class BasicAuthPage(BasePage):
    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)

    def _extract_message_from_response(self, response_text: str) -> str:
        soup = BeautifulSoup(response_text, "html.parser")
        message_tag = soup.find("p")
        return message_tag.get_text(strip=True) if message_tag else ""

    @allure.step("Initialize URL based on username and password")
    def init_url(self, username: str, password: str) -> str:
        if username == "" and password == "":
            return urljoin(str(self.base_url), "basic_auth")
        else:
            return f"http://{username}:{password}@the-internet.herokuapp.com/basic_auth"

    @allure.step("Get status code and authorization message")
    def get_status_code_and_auth_message(self, url: str) -> tuple[int, str | Any]:
        response = requests.get(url)
        if response.status_code == 401:
            message = response.text
        elif response.status_code == 200:
            message = self._extract_message_from_response(response.text)

        return response.status_code, message
