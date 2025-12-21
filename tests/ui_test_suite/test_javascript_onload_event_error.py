import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("UI Test Suite")
@allure.suite("JavaScript onload event error")
@allure.sub_suite("Tests JavaScript onload event error functionality")
class TestJavaScriptOnloadRventError(UiBaseCase):
    """Tests JavaScript onload event error functionality"""

    EXPECTE_ERROR_MSG = "Cannot read properties of undefined (reading 'xyz')"

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_javascript_onload_event_error_functionality(self) -> None:
        self.logger.info("Tests JavaScript onload event error.")
        main_page = MainPage(self)
        main_page.click_javascript_onload_event_error_link()

        self.logger.info("Getting driver log errors.")
        if self.driver.capabilities.get("browserName", "").lower() == "chrome":
            logs = self.driver.get_log("browser")
        else:
            pytest.skip("Browser log retrieval not supported for this browser")
        errors = [e for e in logs if e.get("level") == "SEVERE"]

        self.logger.info("Filter out known noisy messages (optimizely / favicon)")
        messages = [e.get("message", "") for e in errors]
        filtered_messages = [m for m in messages if "optimizely" not in m.lower() and "favicon" not in m.lower()]

        self.logger.info("Verify exactly one relevant error, then assert its text")
        self.assert_equal(
            len(filtered_messages),
            1,
            f"Expected exactly 1 relevant SEVERE error, found {len(filtered_messages)}. Logs: {filtered_messages}",
        )
        self.assert_in(
            self.EXPECTE_ERROR_MSG,
            filtered_messages[0],
            f"Expected error message not found in browser logs. Logs: {filtered_messages}",
        )
