import random


def get_all_albums(user) -> None:
    user.client.get("/albums")


def get_single_album(user) -> None:
    album_id = random.choice(user.album_ids)
    user.client.get(f"/albums/{album_id}", name="/albums/{id}")


def create_album(user) -> None:
    user.client.post(
        "/albums",
        json={
            "title": "test title",
            "userId": random.randint(1, 10),
        },
    )


def update_album(user) -> None:
    album_id = random.choice(user.album_ids)
    user.client.put(
        f"/albums/{album_id}",
        name="/albums/{id} PUT",
        json={
            "id": album_id,
            "title": "updated title",
            "userId": random.randint(1, 10),
        },
    )


def delete_album(user) -> None:
    album_id = random.choice(user.album_ids)
    user.client.delete(f"/albums/{album_id}", name="/albums/{id} DELETE")
