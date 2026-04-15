import logging

from locust import HttpUser, between, events, tag, task
from shapes import RampUpSteadyRampDown  # noqa: F401
from tasks import albums, comments, photos, posts, todos, users


@events.test_start.add_listener
def on_test_start(environment, **kwargs) -> None:
    logging.info(f"Starting load test — target: {environment.host}")
    num_users = getattr(environment.parsed_options, "num_users", "unknown")
    logging.info(f"Users: {num_users}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs) -> None:
    logging.info("Load test finished")
    stats = environment.stats.total
    logging.info(f"Total requests: {stats.num_requests}")
    logging.info(f"Failed requests: {stats.num_failures}")
    logging.info(f"Median response time: {stats.median_response_time}ms")


class JSONPlaceholderUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self) -> None:
        self.post_ids = list(range(1, 101))
        self.album_ids = list(range(1, 101))
        self.photo_ids = list(range(1, 5001))
        self.comment_ids = list(range(1, 501))
        self.todo_ids = list(range(1, 201))
        self.user_ids = list(range(1, 11))

    @tag("read")
    @task(60)
    def task_get_all_posts(self) -> None:
        posts.get_all_posts(self)

    @tag("read")
    @task(20)
    def task_get_single_post(self) -> None:
        posts.get_single_post(self)

    @tag("write")
    @task(10)
    def task_create_post(self) -> None:
        posts.create_post(self)

    @tag("write")
    @task(5)
    def task_update_post(self) -> None:
        posts.update_post(self)

    @tag("write")
    @task(5)
    def task_delete_post(self) -> None:
        posts.delete_post(self)

    @tag("read")
    @task(60)
    def task_get_all_albums(self) -> None:
        albums.get_all_albums(self)

    @tag("read")
    @task(20)
    def task_get_single_album(self) -> None:
        albums.get_single_album(self)

    @tag("write")
    @task(10)
    def task_create_album(self) -> None:
        albums.create_album(self)

    @tag("write")
    @task(5)
    def task_update_album(self) -> None:
        albums.update_album(self)

    @tag("write")
    @task(5)
    def task_delete_album(self) -> None:
        albums.delete_album(self)

    @tag("read")
    @task(60)
    def task_get_all_comments(self) -> None:
        comments.get_all_comments(self)

    @tag("read")
    @task(20)
    def task_get_single_comment(self) -> None:
        comments.get_single_comment(self)

    @tag("write")
    @task(10)
    def task_create_comment(self) -> None:
        comments.create_comment(self)

    @tag("write")
    @task(5)
    def task_update_comment(self) -> None:
        comments.update_comment(self)

    @tag("write")
    @task(5)
    def task_delete_comment(self) -> None:
        comments.delete_comment(self)

    @tag("read")
    @task(60)
    def task_get_all_photos(self) -> None:
        photos.get_all_photos(self)

    @tag("read")
    @task(20)
    def task_get_single_photo(self) -> None:
        photos.get_single_photo(self)

    @tag("write")
    @task(10)
    def task_create_photo(self) -> None:
        photos.create_photo(self)

    @tag("write")
    @task(5)
    def task_update_photo(self) -> None:
        photos.update_photo(self)

    @tag("write")
    @task(5)
    def task_delete_photo(self) -> None:
        photos.delete_photo(self)

    @tag("read")
    @task(60)
    def task_get_all_todos(self) -> None:
        todos.get_all_todos(self)

    @tag("read")
    @task(20)
    def task_get_single_todo(self) -> None:
        todos.get_single_todo(self)

    @tag("write")
    @task(10)
    def task_create_todo(self) -> None:
        todos.create_todo(self)

    @tag("write")
    @task(5)
    def task_update_todo(self) -> None:
        todos.update_todo(self)

    @tag("write")
    @task(5)
    def task_delete_todo(self) -> None:
        todos.delete_todo(self)

    @tag("read")
    @task(60)
    def task_get_all_users(self) -> None:
        users.get_all_users(self)

    @tag("read")
    @task(20)
    def task_get_single_user(self) -> None:
        users.get_single_user(self)

    @tag("write")
    @task(10)
    def task_create_user(self) -> None:
        users.create_user(self)

    @tag("write")
    @task(5)
    def task_update_user(self) -> None:
        users.update_user(self)

    @tag("write")
    @task(5)
    def task_delete_user(self) -> None:
        users.delete_user(self)
