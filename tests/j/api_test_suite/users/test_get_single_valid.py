import allure
import pytest

from tests.j.conftest import APITestContext
from tests.j.helpers import assert_common_response_checks
from tests.j.models import User


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("GET Single Valid")
class TestGetSingleValid:
    """
    Test class for validating the retrieval of a single valid user from the JSONPlaceholder API.
    This class contains regression tests for the GET /users/{id} endpoint, ensuring that
    a valid user ID returns the correct user data with proper structure and constraints.
    """

    @pytest.mark.regression
    @pytest.mark.api
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_user(self, api_context: APITestContext) -> None:
        resource_name = "users"
        config = api_context.get_resource_config(resource_name)
        api_endpoint = f"{api_context.base_url}/{resource_name}/{config.valid_id}"

        with allure.step("Send GET request to users endpoint"):
            response = api_context.session.get(api_endpoint, timeout=api_context.timeout)
            
        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Parse and validate user data"):
            user = User.model_validate(response.json())
            assert user.id == config.valid_id, f"User ID mismatch: expected {config.valid_id}, got {user.id}"
            self._validate_required_fields(user)

    @allure.step("Validate all required user fields")
    def _validate_required_fields(self, user: User) -> None:
        """Helper to validate all required fields are present and non-empty."""
        required_fields = [
            (user.name, "name"),
            (user.username, "username"),
            (user.email, "email"),
            (user.address.street, "address.street"),
            (user.address.suite, "address.suite"),
            (user.address.city, "address.city"),
            (user.address.zipcode, "address.zipcode"),
            (user.address.geo.lat, "address.geo.lat"),
            (user.address.geo.lng, "address.geo.lng"),
            (user.phone, "phone"),
            (user.website, "website"),
            (user.company.name, "company.name"),
            (user.company.catch_phrase, "company.catch_phrase"),
            (user.company.bs, "company.bs"),
        ]

        for field_value, field_name in required_fields:
            assert field_value, f"User {field_name} is missing or empty"
