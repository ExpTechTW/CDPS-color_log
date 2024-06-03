import logging
import sys

import pytz

from cdps.config import Config
import cdps.utils.logger
from cdps.utils.logger import (CustomTimedRotatingFileHandler,
                               Log)


class PlainFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)


class _ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[0;36m",
        "INFO": "\033[0;32m",
        "WARNING": "\033[0;33m",
        "ERROR": "\033[0;31m",
        "RESET": "\033[0m"
    }

    def __init__(self, fmt, datefmt=None, tz=None):
        super().__init__(fmt, datefmt)
        self.tz = tz if tz else pytz.UTC

    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            color = self.COLORS.get(levelname, self.COLORS["RESET"])
            message = f"{color}{message}{self.COLORS['RESET']}"
        return message


def _setup_logger(self, *, url):
    logger = logging.getLogger("MyLogger")
    logger.handlers.clear()
    logger.setLevel("DEBUG")
    logger.propagate = False

    tz_utc_8 = pytz.timezone('Asia/Taipei')

    file_handler = CustomTimedRotatingFileHandler(
        self.log_dir,
        when="midnight",
        interval=1,
        backupCount=5
    )

    file_formatter = PlainFormatter(
        '[%(asctime)s][%(levelname)s]: %(message)s', '%H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = _ColoredFormatter(
        '[%(asctime)s][%(levelname)s]: %(message)s', '%H:%M:%S', tz=tz_utc_8
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    self.logger = logger


cdps.utils.logger.Log.setup_logger = _setup_logger

Log.reset_instance()
log = Log()
config = Config()
log.logger.setLevel(config._data['log_level'])
log.logger.day = config._data['log_save_days']


def initialize(completion_event):
    completion_event.set()
