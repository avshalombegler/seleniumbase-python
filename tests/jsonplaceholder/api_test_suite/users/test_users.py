import allure
import pytest

from tests.jsonplaceholder.conftest import APITestContext
from tests.jsonplaceholder.helpers import assert_common_response_checks
from tests.jsonplaceholder.models import User

RESOURCE = "users"


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Users")
class TestUsersGet:
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.title("GET /users - List All")
    def test_list_all(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}"

        with allure.step("Send GET request to list all users"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate list response"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == config.list_count

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /users/{id} - Single Valid")
    def test_single_valid(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.valid_id}"

        with allure.step("Send GET request for single valid user"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate user data"):
            user = User.model_validate(response.json())
            assert user.id == config.valid_id
            assert user.name
            assert user.username
            assert user.email
            assert user.phone
            assert user.website
            assert user.address.street
            assert user.address.suite
            assert user.address.city
            assert user.address.zipcode
            assert user.address.geo.lat
            assert user.address.geo.lng
            assert user.company.name
            assert user.company.catch_phrase
            assert user.company.bs

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /users/{id} - Single Not Found")
    def test_single_not_found(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.notfound_id}"

        with allure.step("Send GET request for non-existent user"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Users")
class TestUsersPost:
    PAYLOAD = {"name": "new name", "username": "new username", "email": "new@email.testing"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("POST /users - Create New")
    def test_create_new(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}"

        with allure.step("Send POST request to create new user"):
            response = api_context.session.post(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=201)

        with allure.step("Validate created user response"):
            data = response.json()
            for key, value in self.PAYLOAD.items():
                assert data.get(key) == value, f"Field '{key}' should be '{value}', got '{data.get(key)}'"
            assert isinstance(data["id"], int)
            assert data["id"] > config.list_count


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Users")
class TestUsersPut:
    PAYLOAD = {
        "id": 1,
        "name": "Updated User Name",
        "username": "updateduser",
        "email": "updated@email.com",
        "phone": "1-770-736-8031",
        "website": "updated.org",
        "address": {
            "street": "Updated Street",
            "suite": "Suite 100",
            "city": "Updated City",
            "zipcode": "12345-6789",
            "geo": {"lat": "-37.3159", "lng": "81.1496"},
        },
        "company": {
            "name": "Updated Company",
            "catchPhrase": "Updated catchphrase",
            "bs": "updated bs",
        },
    }

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PUT /users/1 - Update Full")
    def test_update_full(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send PUT request to update user"):
            response = api_context.session.put(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate updated user response"):
            data = response.json()
            assert data["id"] == 1
            assert data["name"] == "Updated User Name"
            assert data["username"] == "updateduser"
            assert data["email"] == "updated@email.com"


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Users")
class TestUsersPatch:
    PAYLOAD = {"website": "newwebsite.com"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PATCH /users/1 - Update Partial")
    def test_update_partial(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send PATCH request to partially update user"):
            response = api_context.session.patch(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate patched user response"):
            data = response.json()
            user = User.model_validate(data)
            assert data["website"] == "newwebsite.com"
            assert user.name == "Leanne Graham"
            assert user.email == "Sincere@april.biz"
            assert user.id == 1


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Users")
class TestUsersDelete:
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("DELETE /users/1 - Delete Existing")
    def test_delete_existing(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send DELETE request to delete user"):
            response = api_context.session.delete(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate empty response body"):
            assert response.json() == {}


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Users")
class TestUsersNegative:
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /users/{id} - Negative: invalid id")
    def test_negative_id(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.negative_id}"

        with allure.step("Send GET request with negative id"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /users/{id} - Negative: string id")
    def test_string_id(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.string_id}"

        with allure.step("Send GET request with string id"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}
