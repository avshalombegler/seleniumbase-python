import random


def get_all_photos(user) -> None:
    user.client.get("/photos")


def get_single_photo(user) -> None:
    photo_id = random.choice(user.photo_ids)
    user.client.get(f"/photos/{photo_id}", name="/photos/{id}")


def create_photo(user) -> None:
    user.client.post(
        "/photos",
        json={
            "title": "test title",
            "url": "test url",
            "thumbnailUrl": "test thumbnailUrl",
            "albumId": random.randint(1, 10),
        },
    )


def update_photo(user) -> None:
    photo_id = random.choice(user.photo_ids)
    user.client.put(
        f"/photos/{photo_id}",
        name="/photos/{id} PUT",
        json={
            "id": photo_id,
            "title": "updated title",
            "url": "updated url",
            "thumbnailUrl": "updated thumbnailUrl",
            "albumId": random.randint(1, 10),
        },
    )


def delete_photo(user) -> None:
    photo_id = random.choice(user.photo_ids)
    user.client.delete(f"/photos/{photo_id}", name="/photos/{id} DELETE")
