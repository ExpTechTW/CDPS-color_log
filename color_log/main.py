import logging

import pytz

import cdps.utils.logger
from cdps.utils.logger import (CustomFormatter, CustomTimedRotatingFileHandler,
                               Log)


class _ColoredFormatter(CustomFormatter):
    COLORS = {
        "DEBUG": "\033[0;36m",
        "INFO": "\033[0;32m",
        "WARNING": "\033[0;33m",
        "ERROR": "\033[0;31m",
        "CRITICAL": "\033[0;35m",
        "RESET": "\033[0m"
    }

    def __init__(self, fmt, datefmt, tz):
        super().__init__(fmt, datefmt, tz)

    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        return f"{self.COLORS.get(levelname, self.COLORS['RESET'])}{message}{self.COLORS['RESET']}"


def _setup_logger(self, *, url):
    logger = logging.getLogger("MyLogger")
    logger.handlers.clear()
    logger.setLevel("DEBUG")

    handler = CustomTimedRotatingFileHandler(
        self.log_dir,
        when="midnight",
        interval=1,
        backupCount=5
    )

    tz_utc_8 = pytz.timezone('Asia/Taipei')
    formatter = _ColoredFormatter(
        '[%(asctime)s][%(levelname)s] -> %(message)s', '%H:%M:%S', tz_utc_8
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    self.logger = logger


cdps.utils.logger.Log.setup_logger = _setup_logger

Log.reset_instance()


def initialize(completion_event):
    completion_event.set()
