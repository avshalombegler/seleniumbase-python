# Common assertions (status code, content type, response time)

import allure


@allure.step("Validate common response checks")
def assert_common_response_checks(
    response, request_timeout: float, expected_status: int = 200, expected_content_type: str = "application/json"
) -> None:
    """
    Validate common response attributes.

    Args:
        response: The HTTP response object
        request_timeout: Maximum allowed response time in seconds
        expected_status: Expected HTTP status code (default: 200)
        expected_content_type: Expected content type (default: application/json)
    """
    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, got {response.status_code}"
    )
    assert expected_content_type in response.headers.get("Content-Type", ""), (
        f"Expected {expected_content_type} content type, got {response.headers.get('Content-Type')}"
    )
    assert response.elapsed.total_seconds() <= request_timeout, (
        f"Response took too long: {response.elapsed.total_seconds()}s (max: {request_timeout}s)"
    )
