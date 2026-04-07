import allure
import pytest

from tests.jsonplaceholder.conftest import APITestContext
from tests.jsonplaceholder.helpers import assert_common_response_checks
from tests.jsonplaceholder.models import Comment

RESOURCE = "comments"


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Comments")
class TestCommentsGet:
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.title("GET /comments - List All")
    def test_list_all(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}"

        with allure.step("Send GET request to list all comments"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate list response"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == config.list_count

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /comments/{id} - Single Valid")
    def test_single_valid(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.valid_id}"

        with allure.step("Send GET request for single valid comment"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate comment data"):
            comment = Comment.model_validate(response.json())
            assert comment.id == config.valid_id
            assert comment.postId
            assert comment.name
            assert comment.email
            assert comment.body

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /comments/{id} - Single Not Found")
    def test_single_not_found(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.notfound_id}"

        with allure.step("Send GET request for non-existent comment"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Comments")
class TestCommentsPost:
    PAYLOAD = {"postId": 1, "name": "new comment name", "email": "test@test.com", "body": "new comment body"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("POST /comments - Create New")
    def test_create_new(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}"

        with allure.step("Send POST request to create new comment"):
            response = api_context.session.post(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=201)

        with allure.step("Validate created comment response"):
            data = response.json()
            for key, value in self.PAYLOAD.items():
                assert data.get(key) == value, f"Field '{key}' should be '{value}', got '{data.get(key)}'"
            assert data["id"] > config.list_count


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Comments")
class TestCommentsPut:
    PAYLOAD = {"postId": 1, "id": 1, "name": "updated name", "email": "updated@test.com", "body": "updated body"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PUT /comments/1 - Update Full")
    def test_update_full(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send PUT request to update comment"):
            response = api_context.session.put(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate updated comment response"):
            data = response.json()
            for key, value in self.PAYLOAD.items():
                assert data.get(key) == value, f"Field '{key}' should be '{value}', got '{data.get(key)}'"


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Comments")
class TestCommentsPatch:
    PAYLOAD = {"name": "updated name only"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PATCH /comments/1 - Update Partial")
    def test_update_partial(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send PATCH request to partially update comment"):
            response = api_context.session.patch(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate patched comment response"):
            comment = Comment.model_validate(response.json())
            for key, value in self.PAYLOAD.items():
                assert getattr(comment, key) == value, (
                    f"Field '{key}' should be '{value}', got '{getattr(comment, key)}'"
                )
            assert isinstance(comment.id, int)


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Comments")
class TestCommentsDelete:
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("DELETE /comments/1 - Delete Existing")
    def test_delete_existing(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send DELETE request to delete comment"):
            response = api_context.session.delete(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate empty response body"):
            assert response.json() == {}


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Comments")
class TestCommentsNegative:
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /comments/{id} - Negative: invalid id")
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
    @allure.title("GET /comments/{id} - Negative: string id")
    def test_string_id(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.string_id}"

        with allure.step("Send GET request with string id"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}
