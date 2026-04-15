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
            "title": "test title",
            "body": "test body",
            "userId": random.randint(1, 10),
        },
    )


def update_user(user) -> None:
    user_id = random.choice(user.user_ids)
    user.client.put(
        f"/users/{user_id}",
        name="/users/{id}",
        json={
            "id": user_id,
            "title": "updated title",
            "body": "updated body",
            "userId": random.randint(1, 10),
        },
    )


def delete_user(user) -> None:
    user_id = random.choice(user.user_ids)
    user.client.delete(f"/users/{user_id}", name="/users/{id}")
