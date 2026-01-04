import logging
import re
import sys

import colorama
import structlog
from pythonjsonlogger import jsonlogger


class AnsiStripFilter(logging.Filter):
    """Filter to strip ANSI escape codes from log messages for file output."""

    def filter(self, record):
        # Strip ANSI escape sequences (e.g., colors) from the message
        record.msg = re.sub(r'\x1b\[[0-9;]*m', '', record.msg)
        return True


def remove_context_vars(logger, method_name, event_dict):
    """Processor to remove context variables from the event dict."""
    context_keys = ['browser', 'test_name', 'page']  # Add any other context keys used in your logs
    for key in context_keys:
        event_dict.pop(key, None)
    return event_dict


def configure_logging(log_level: str = "INFO") -> None:
    # Initialize colorama to enable ANSI colors on Windows
    colorama.init()

    root = logging.getLogger()
    if root.handlers:
        root.handlers.clear()

    # Console handler with human-readable format
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)
    root.addHandler(console_handler)
    root.setLevel(log_level)

    # File handler with JSON format for parsing (strips ANSI codes)
    file_handler = logging.FileHandler("test_logs.jsonl")
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(json_formatter)
    file_handler.addFilter(AnsiStripFilter())  # Strip ANSI codes for file output
    root.addHandler(file_handler)

    # Configure structlog with console-friendly output (colors enabled for console, context removed)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            remove_context_vars,  # Remove context variables before rendering
            structlog.dev.ConsoleRenderer(
                colors=True,  # Enable colors for console output
                exception_formatter=structlog.dev.plain_traceback,
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


configure_logging()
