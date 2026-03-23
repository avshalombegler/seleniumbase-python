import logging
import os
import sys

import colorama
import structlog


def remove_context_vars(logger, method_name, event_dict):
    """Processor to strip per-test context keys from console output."""
    for key in ("browser", "test_name", "page"):
        event_dict.pop(key, None)
    return event_dict


def custom_console_renderer(logger, method_name, event_dict):
    """Format logs as: timestamp | LEVEL | logger:file:line | message"""
    timestamp = event_dict.pop("timestamp", "")
    level = event_dict.pop("level", "").upper()
    logger_name = event_dict.pop("logger", "")
    filename = event_dict.pop("filename", "")
    lineno = event_dict.pop("lineno", "")

    location = f"{logger_name}:{filename}:{lineno}" if filename and lineno else logger_name

    event = event_dict.pop("event", "")
    extras = " ".join(f"{k}={v}" for k, v in event_dict.items())
    full_message = f"{event} {extras}".strip() if extras else event

    level_colors = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }
    reset = "\033[0m"
    colored_level = f"{level_colors.get(level, '')}{level:4s}{reset}"
    return f"{timestamp} | {colored_level} | {location} | {full_message}"


def configure_logging(log_level: str = "INFO") -> None:
    colorama.init()
    enable_console_logs = os.environ.get("SHOW_LOGS", "false").lower() == "true"

    root = logging.getLogger()
    if root.handlers:
        root.handlers.clear()

    # Shared processors — run once, results flow to all handlers
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.CallsiteParameterAdder(
            parameters=[
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
        structlog.processors.TimeStamper(fmt="%H:%M:%S"),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
    ]

    # Console handler — colored human-readable, context vars stripped for brevity
    if enable_console_logs:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processors=[
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    remove_context_vars,
                    custom_console_renderer,
                ],
                foreign_pre_chain=shared_processors,
            )
        )
        root.addHandler(console_handler)

    # File handler — structured JSON, all fields including test_name and browser
    worker_id = os.environ.get("PYTEST_XDIST_WORKER") or "local"
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(logs_dir, f"test_logs_{worker_id}.jsonl"))
    file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
            foreign_pre_chain=shared_processors,
        )
    )
    root.addHandler(file_handler)

    root.setLevel(log_level)

    # wrap_for_formatter must be the final processor so structlog hands off to handlers
    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
