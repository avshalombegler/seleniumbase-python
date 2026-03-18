from typing import TypedDict


class ResourceConfig(TypedDict, total=False):
    list_count: int
    valid_id: int
    notfound_id: int
    negative_id: int
    string_id: str


class JSONPlaceholderConfig:
    BASE_URL = "https://jsonplaceholder.typicode.com"
    REQUEST_TIMEOUT = 5

    RESOURCES: dict[str, ResourceConfig] = {
        "albums": {
            "list_count": 100,
            "valid_id": 5,
            "notfound_id": 9999,
            "negative_id": -1,
            "string_id": "abc",
        },
        "comments": {
            "list_count": 500,
            "valid_id": 5,
            "notfound_id": 9999,
            "negative_id": -1,
            "string_id": "abc",
        },
        "photos": {
            "list_count": 5000,
            "valid_id": 5,
            "notfound_id": 9999,
            "negative_id": -1,
            "string_id": "abc",
        },
        "posts": {
            "list_count": 100,
            "valid_id": 5,
            "notfound_id": 9999,
            "negative_id": -1,
            "string_id": "abc",
        },
        "todos": {
            "list_count": 200,
            "valid_id": 5,
            "notfound_id": 9999,
            "negative_id": -1,
            "string_id": "abc",
        },
        "users": {
            "list_count": 10,
            "valid_id": 5,
            "notfound_id": 9999,
            "negative_id": -1,
            "string_id": "abc",
        },
    }
