import allure
import pytest

from tests.jsonplaceholder.conftest import APITestContext
from tests.jsonplaceholder.helpers import assert_common_response_checks
from tests.jsonplaceholder.models import Post

RESOURCE = "posts"


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Posts")
class TestPostsGet:
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.title("GET /posts - List All")
    def test_list_all(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}"

        with allure.step("Send GET request to list all posts"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate list response"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == config.list_count

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /posts/{id} - Single Valid")
    def test_single_valid(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.valid_id}"

        with allure.step("Send GET request for single valid post"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate post data"):
            post = Post.model_validate(response.json())
            assert post.id == config.valid_id
            assert post.title
            assert post.body
            assert isinstance(post.userId, int)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /posts/{id} - Single Not Found")
    def test_single_not_found(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.notfound_id}"

        with allure.step("Send GET request for non-existent post"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Posts")
class TestPostsPost:
    PAYLOAD = {"userId": 1, "title": "new title for testing", "body": "new body for testing"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("POST /posts - Create New")
    def test_create_new(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}"

        with allure.step("Send POST request to create new post"):
            response = api_context.session.post(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=201)

        with allure.step("Validate created post response"):
            data = response.json()
            for key, value in self.PAYLOAD.items():
                assert data.get(key) == value, f"Field '{key}' should be '{value}', got '{data.get(key)}'"
            assert data["id"] > config.list_count


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Posts")
class TestPostsPut:
    PAYLOAD = {"userId": 1, "id": 1, "title": "new title for testing", "body": "new body for testing"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PUT /posts/1 - Update Full")
    def test_update_full(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send PUT request to update post"):
            response = api_context.session.put(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate updated post response"):
            data = response.json()
            for key, value in self.PAYLOAD.items():
                assert data.get(key) == value, f"Field '{key}' should be '{value}', got '{data.get(key)}'"
            assert isinstance(data["id"], int)
            assert isinstance(data["title"], str)
            assert isinstance(data["body"], str)


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Posts")
class TestPostsPatch:
    PAYLOAD = {"title": "new title for testing"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PATCH /posts/1 - Update Partial")
    def test_update_partial(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send PATCH request to partially update post"):
            response = api_context.session.patch(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate patched post response"):
            post = Post.model_validate(response.json())
            for key, value in self.PAYLOAD.items():
                assert getattr(post, key) == value, f"Field '{key}' should be '{value}', got '{getattr(post, key)}'"
            assert isinstance(post.id, int)
            assert isinstance(post.body, str)


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Posts")
class TestPostsDelete:
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("DELETE /posts/1 - Delete Existing")
    def test_delete_existing(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send DELETE request to delete post"):
            response = api_context.session.delete(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate empty response body"):
            assert response.json() == {}


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Posts")
class TestPostsNegative:
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /posts/{id} - Negative: invalid id")
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
    @allure.title("GET /posts/{id} - Negative: string id")
    def test_string_id(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.string_id}"

        with allure.step("Send GET request with string id"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}
