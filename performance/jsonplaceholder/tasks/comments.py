import random


def get_all_comments(user) -> None:
    user.client.get("/comments")


def get_single_comment(user) -> None:
    comment_id = random.choice(user.comment_ids)
    user.client.get(f"/comments/{comment_id}", name="/comments/{id}")


def create_comment(user) -> None:
    user.client.post(
        "/comments",
        json={
            "title": "test title",
            "body": "test body",
            "userId": random.randint(1, 10),
        },
    )


def update_comment(user) -> None:
    comment_id = random.choice(user.comment_ids)
    user.client.put(
        f"/comments/{comment_id}",
        name="/comments/{id}",
        json={
            "id": comment_id,
            "title": "updated title",
            "body": "updated body",
            "userId": random.randint(1, 10),
        },
    )


def delete_comment(user) -> None:
    comment_id = random.choice(user.comment_ids)
    user.client.delete(f"/comments/{comment_id}", name="/comments/{id}")
