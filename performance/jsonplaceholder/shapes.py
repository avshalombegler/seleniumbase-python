from locust import LoadTestShape


class RampUpSteadyRampDown(LoadTestShape):
    """
    Ramp up to peak users, hold steady, then ramp down.

    Timeline:
      0-10s  : ramp up   0 → 10 users
      10-30s : steady    10 users
      30-40s : ramp down 10 → 0 users
    """

    stages = [
        {"duration": 10, "users": 10, "spawn_rate": 1},
        {"duration": 30, "users": 10, "spawn_rate": 1},
        {"duration": 40, "users": 0, "spawn_rate": 1},
    ]

    def tick(self) -> tuple[int, int] | None:
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
