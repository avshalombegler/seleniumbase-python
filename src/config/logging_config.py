import logging
import os
import re
import sys

import colorama
import structlog
from pythonjsonlogger import jsonlogger


class AnsiStripFilter(logging.Filter):
    """Filter to strip ANSI escape codes from log messages for file output."""

    def filter(self, record):
        # Strip ANSI escape sequences (e.g., colors) from the message
        record.msg = re.sub(r"\x1b\[[0-9;]*m", "", record.msg)
        return True


def remove_context_vars(logger, method_name, event_dict):
    """Processor to remove context variables from the event dict."""
    context_keys = ["browser", "test_name", "page"]  # Add any other context keys used in your logs
    for key in context_keys:
        event_dict.pop(key, None)
    return event_dict


def custom_console_renderer(logger, method_name, event_dict):
    """Custom processor to format logs with timestamp | level | logger:file:line | message with colors."""
    timestamp = event_dict.pop("timestamp", "")
    level = event_dict.pop("level", "").upper()
    logger_name = event_dict.pop("logger", "")

    # Extract filename and line number from event_dict if available
    filename = event_dict.pop("filename", "")
    lineno = event_dict.pop("lineno", "")

    # Build the location string (logger:file:line)
    if filename and lineno:
        location = f"{logger_name}:{filename}:{lineno}"
    else:
        location = logger_name

    # Extract the main message
    event = event_dict.pop("event", "")

    # Format any remaining key-value pairs
    extras = " ".join(f"{k}={v}" for k, v in event_dict.items())

    # Combine message and extras
    full_message = f"{event} {extras}".strip() if extras else event

    # Color codes based on log level
    level_colors = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    reset = "\033[0m"

    # Apply color to level
    colored_level = f"{level_colors.get(level, '')}{level:4s}{reset}"

    # Format the final log line with colors
    return f"{timestamp} | {colored_level} | {location} | {full_message}"


def configure_logging(log_level: str = "INFO") -> None:
    colorama.init()

    # Check environment variable to toggle console logging
    enable_console_logs = os.environ.get("SHOW_LOGS", "false").lower() == "true"

    root = logging.getLogger()
    if root.handlers:
        root.handlers.clear()

    # Console handler - only add if enabled
    if enable_console_logs:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        root.addHandler(console_handler)

    root.setLevel(log_level)

    # File handler with JSON format (always enabled)
    file_handler = logging.FileHandler("test_logs.jsonl")
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(json_formatter)
    file_handler.addFilter(AnsiStripFilter())
    root.addHandler(file_handler)

    # Configure structlog
    structlog.configure(
        processors=[
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
            remove_context_vars,
            custom_console_renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
