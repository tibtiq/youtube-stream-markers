"""This module handles all the setup for logging.

Usage:
1. Import the module
    import logger

2. Initialize the logger:
    LOGGER = logger.setup_logging(pathlib.Path(__file__).name,
                                pathlib.Path(__file__).parent.parent / 'logs')

3. Use the logger in your code:
    LOGGER.info("This is an informational message.")
    LOGGER.error("This is an error message.")
"""

import logging
import pathlib
from datetime import datetime

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


def clean_up_logs(log_dir: pathlib.Path, max_log_limit: int = 10) -> None:
    """Clean up log files. Delete oldest logs until number of logs matches max_log_limit.

    This function has an issue where it can't delete log files created during the application
    session. In normal use this shouldn't be a problem. It is reproducible by refreshing the
    script enough times to reach a log created during this session.

    Args:
        log_dir: pathlib.Path
            Directory containing logs.
        max_log_number: int = 10
            Max number of log files to keep.
    """
    log_paths = list(log_dir.rglob("*.log"))
    if len(log_paths) <= max_log_limit:
        return

    while len(log_paths) > max_log_limit:
        try:
            log_paths.pop(0).unlink()
        except PermissionError:
            continue


def setup_logging(
    logger_name: str, log_dir: pathlib.Path, log_level: int = logging.DEBUG
) -> logging.Logger:
    """Set up console and file logging.

    File logger is always set to DEBUG level.

    Args:
        logger_name: str
            Name of the logger.
        log_dir: pathlib.Path
            Directory to place log files.
        log_level: int = logging.DEBUG
            Log level to set console logger.
    """
    clean_up_logs(log_dir)

    log_level = 50 - (log_level * 10)
    formatter = logging.Formatter(
        fmt=f"%(asctime)s {'| ' + logger_name or ''} | %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    log_dir = log_dir.resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    log_file = log_dir / f"{now.strftime('%Y-%m-%d %H-%M-%S')}.log"

    file_handler = logging.FileHandler(filename=log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
