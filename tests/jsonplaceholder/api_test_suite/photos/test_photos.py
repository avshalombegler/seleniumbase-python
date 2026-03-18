import allure
import pytest

from tests.jsonplaceholder.conftest import APITestContext
from tests.jsonplaceholder.helpers import assert_common_response_checks
from tests.jsonplaceholder.models import Photo

RESOURCE = "photos"


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Photos")
class TestPhotosGet:
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.title("GET /photos - List All")
    def test_list_all(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}"

        with allure.step("Send GET request to list all photos"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate list response"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == config.list_count

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /photos/{id} - Single Valid")
    def test_single_valid(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.valid_id}"

        with allure.step("Send GET request for single valid photo"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate photo data"):
            photo = Photo.model_validate(response.json())
            assert photo.id == config.valid_id
            assert photo.title
            assert photo.url
            assert photo.thumbnailUrl

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /photos/{id} - Single Not Found")
    def test_single_not_found(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.notfound_id}"

        with allure.step("Send GET request for non-existent photo"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Photos")
class TestPhotosPost:
    PAYLOAD = {
        "albumId": 1,
        "title": "new photo title",
        "url": "https://via.placeholder.com/600/new",
        "thumbnailUrl": "https://via.placeholder.com/150/new",
    }

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("POST /photos - Create New")
    def test_create_new(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}"

        with allure.step("Send POST request to create new photo"):
            response = api_context.session.post(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=201)

        with allure.step("Validate created photo response"):
            data = response.json()
            for key, value in self.PAYLOAD.items():
                assert data.get(key) == value, f"Field '{key}' should be '{value}', got '{data.get(key)}'"
            assert data["id"] > config.list_count


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Photos")
class TestPhotosPut:
    PAYLOAD = {
        "albumId": 1,
        "id": 1,
        "title": "updated photo title",
        "url": "https://via.placeholder.com/600/updated",
        "thumbnailUrl": "https://via.placeholder.com/150/updated",
    }

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PUT /photos/1 - Update Full")
    def test_update_full(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send PUT request to update photo"):
            response = api_context.session.put(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate updated photo response"):
            data = response.json()
            for key, value in self.PAYLOAD.items():
                assert data.get(key) == value, f"Field '{key}' should be '{value}', got '{data.get(key)}'"


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Photos")
class TestPhotosPatch:
    PAYLOAD = {"title": "updated photo title only"}

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PATCH /photos/1 - Update Partial")
    def test_update_partial(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send PATCH request to partially update photo"):
            response = api_context.session.patch(url, json=self.PAYLOAD, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate patched photo response"):
            photo = Photo.model_validate(response.json())
            for key, value in self.PAYLOAD.items():
                assert getattr(photo, key) == value, f"Field '{key}' should be '{value}', got '{getattr(photo, key)}'"
            assert isinstance(photo.id, int)


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Photos")
class TestPhotosDelete:
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("DELETE /photos/1 - Delete Existing")
    def test_delete_existing(self, api_context: APITestContext) -> None:
        url = f"{api_context.base_url}/{RESOURCE}/1"

        with allure.step("Send DELETE request to delete photo"):
            response = api_context.session.delete(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout)

        with allure.step("Validate empty response body"):
            assert response.json() == {}


@allure.parent_suite("JSONPlaceholder")
@allure.suite("API Test Suite")
@allure.sub_suite("Photos")
class TestPhotosNegative:
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /photos/{id} - Negative: invalid id")
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
    @allure.title("GET /photos/{id} - Negative: string id")
    def test_string_id(self, api_context: APITestContext) -> None:
        config = api_context.get_resource_config(RESOURCE)
        url = f"{api_context.base_url}/{RESOURCE}/{config.string_id}"

        with allure.step("Send GET request with string id"):
            response = api_context.session.get(url, timeout=api_context.timeout)

        assert_common_response_checks(response, api_context.timeout, expected_status=404)

        with allure.step("Validate empty response body"):
            assert response.json() == {}
