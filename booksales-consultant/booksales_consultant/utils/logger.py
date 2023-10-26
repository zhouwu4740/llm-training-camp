import os
import sys

from loguru import logger

LOGFILE = "app.log"


class Logger:
    def __init__(self, log_dir="logs", debug=False):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, LOGFILE)
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
