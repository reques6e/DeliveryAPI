import logging

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_format = "%(asctime)s %(levelname)s %(message)s"
        formatter = logging.Formatter(log_format, datefmt="%d.%m.%Y %H:%M:%S")
        return formatter.format(record)

logger = logging.getLogger("custom_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())

logger.addHandler(console_handler)

__all__ = ['logger']
