import random


def get_all_users(user) -> None:
    user.client.get("/users")


def get_single_user(user) -> None:
    user_id = random.choice(user.user_ids)
    user.client.get(f"/users/{user_id}", name="/users/{id}")


def create_user(user) -> None:
    user.client.post(
        "/users",
        json={
            "name": "test name",
            "username": "test username",
            "email": "test@email.com",
            "address": {
                "street": "test street",
                "suite": "test suite",
                "city": "test city",
                "zipcode": "test zipcode",
                "geo": {"lat": "test lat", "lng": "test lng"},
            },
        },
    )


def update_user(user) -> None:
    user_id = random.choice(user.user_ids)
    user.client.put(
        f"/users/{user_id}",
        name="/users/{id} PUT",
        json={
            "id": user_id,
            "name": "updated name",
            "username": "updated username",
            "email": "updated@email.com",
            "address": {
                "street": "updated street",
                "suite": "updated suite",
                "city": "updated city",
                "zipcode": "updated zipcode",
                "geo": {"lat": "updated lat", "lng": "updated lng"},
            },
        },
    )


def delete_user(user) -> None:
    user_id = random.choice(user.user_ids)
    user.client.delete(f"/users/{user_id}", name="/users/{id} DELETE")
