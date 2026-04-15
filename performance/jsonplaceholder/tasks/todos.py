import random


def get_all_todos(user) -> None:
    user.client.get("/todos")


def get_single_todo(user) -> None:
    todo_id = random.choice(user.todo_ids)
    user.client.get(f"/todos/{todo_id}", name="/todos/{id}")


def create_todo(user) -> None:
    user.client.post(
        "/todos",
        json={
            "title": "test title",
            "body": "test body",
            "userId": random.randint(1, 10),
        },
    )


def update_todo(user) -> None:
    todo_id = random.choice(user.todo_ids)
    user.client.put(
        f"/todos/{todo_id}",
        name="/todos/{id}",
        json={
            "id": todo_id,
            "title": "updated title",
            "body": "updated body",
            "userId": random.randint(1, 10),
        },
    )


def delete_todo(user) -> None:
    todo_id = random.choice(user.todo_ids)
    user.client.delete(f"/todos/{todo_id}", name="/todos/{id}")
