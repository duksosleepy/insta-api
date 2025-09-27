import logging
import sys

from loguru import logger

from .formatters import LogFormatter
from .handler import InterceptHandler


def init_logging():
    log_formatter = LogFormatter()
    logger.remove()
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    for _logger in (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "uvicorn.asgi",
        "fastapi",
        "fastapi.error",
    ):
        logging_logger = logging.getLogger(_logger)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False
        logging_logger.setLevel(logging.DEBUG)

    logger.add(
        sys.stdout,
        format=log_formatter.console_format,
        level="INFO",
        backtrace=False,
        diagnose=True,
        colorize=True,
    )

    return logger
