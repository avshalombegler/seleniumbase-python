import random


def get_all_posts(user) -> None:
    user.client.get("/posts")


def get_single_post(user) -> None:
    post_id = random.choice(user.post_ids)
    user.client.get(f"/posts/{post_id}", name="/posts/{id}")


def create_post(user) -> None:
    user.client.post(
        "/posts",
        json={
            "title": "test title",
            "body": "test body",
            "userId": random.randint(1, 10),
        },
    )


def update_post(user) -> None:
    post_id = random.choice(user.post_ids)
    user.client.put(
        f"/posts/{post_id}",
        name="/posts/{id} PUT",
        json={
            "id": post_id,
            "title": "updated title",
            "body": "updated body",
            "userId": random.randint(1, 10),
        },
    )


def delete_post(user) -> None:
    post_id = random.choice(user.post_ids)
    user.client.delete(f"/posts/{post_id}", name="/posts/{id} DELETE")
