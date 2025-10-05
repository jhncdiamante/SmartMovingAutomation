import logging
import sys

def setup_logger(name=None):
    logger = logging.getLogger(name if name else "")
    logger.setLevel(logging.DEBUG)  # or INFO

    # Prevent adding handlers twice if setup_logger is called multiple times
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler("bot.log", mode="w")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
