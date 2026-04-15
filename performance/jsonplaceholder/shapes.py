import os

from locust import LoadTestShape

"""
Ramp up to peak users, hold steady, then ramp down.

Timeline:
    0-10s  : ramp up   0 → 10 users
    10-30s : steady    10 users
    30-40s : ramp down 10 → 0 users
"""
RAMP_STAGES = [
    {"duration": 10, "users": 10, "spawn_rate": 1},
    {"duration": 30, "users": 10, "spawn_rate": 1},
    {"duration": 40, "users": 0, "spawn_rate": 1},
]


"""
Spike to peak users, hold steady, then ramp down.

Timeline:
    0-10s  : ramp up   0 → 10 users
    10-15s : spike     50 users
    15-20s : ramp down 10 users
    20-30s : steady    10 → 0 users
"""
SPIKE_STAGES = [
    {"duration": 10, "users": 10, "spawn_rate": 1},
    {"duration": 15, "users": 50, "spawn_rate": 10},
    {"duration": 20, "users": 10, "spawn_rate": 10},
    {"duration": 30, "users": 0, "spawn_rate": 1},
]


class ActiveShape(LoadTestShape):
    def tick(self) -> tuple[int, int] | None:
        shape = os.getenv("LOCUST_SHAPE", "ramp")
        stages = SPIKE_STAGES if shape == "spike" else RAMP_STAGES

        run_time = self.get_run_time()
        for stage in stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None
