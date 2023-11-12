import os
import sys

from loguru import logger

LOGFILE = "server.log"
LOGDIR = "logs"


class Logger:
    def __init__(self, file_name=None, log_dir=None, debug=False):
        if log_dir is None:
            log_dir = LOGDIR
        if file_name is None:
            file_name = LOGFILE

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, file_name)
        # Remove default loguru handler
        logger.remove()
        level = "DEBUG" if debug else "INFO"
        logger.add(sys.stdout, level=level)
        logger.add(log_file_path, rotation="02:00", level="DEBUG")
        self.logger = logger


LOGGER = Logger(debug=True).logger

if __name__ == "__main__":
    LOGGER.debug("This is a debug message.")
    LOGGER.info("This is an info message.")
    LOGGER.warning("This is a warning message.")
    LOGGER.error("This is an error message.")
