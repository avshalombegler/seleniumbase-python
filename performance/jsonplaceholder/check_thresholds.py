import csv
import sys

DEFAULT_P95_MS = 500
DEFAULT_FAILURE_RATE = 0.0

ENDPOINT_THRESHOLDS: dict[str, dict] = {
    "/photos": {"p95_ms": 400},
    "/photos/{id}": {"p95_ms": 600},
    "/comments": {"p95_ms": 350},
}


def get_threshold(name: str, metric: str) -> float:
    endpoint = ENDPOINT_THRESHOLDS.get(name, {})
    defaults = {"p95_ms": DEFAULT_P95_MS, "failure_rate": DEFAULT_FAILURE_RATE}
    return endpoint.get(metric, defaults[metric])


def check(stats_file: str) -> None:
    failures = []

    with open(stats_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Name"]
            if name == "Aggregated":
                continue

            p95 = float(row["95%"])
            failure_count = int(row["Failure Count"])
            request_count = int(row["Request Count"])
            failure_rate = failure_count / request_count if request_count > 0 else 0.0

            p95_threshold = get_threshold(name, "p95_ms")
            failure_threshold = get_threshold(name, "failure_rate")

            if p95 > p95_threshold:
                failures.append(f"FAIL p95 {name}: {p95}ms > {p95_threshold}ms")
            if failure_rate > failure_threshold:
                failures.append(f"FAIL failures {name}: {failure_rate:.1%} > {failure_threshold:.1%}")

    if failures:
        for f in failures:
            print(f)
        sys.exit(1)
    else:
        print("OK — all thresholds passed")
        sys.exit(0)


if __name__ == "__main__":
    check("results_stats.csv")
