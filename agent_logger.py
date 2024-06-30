import logging
from logging.handlers import RotatingFileHandler
import colorlog

def setup_logger(name, log_file, level=logging.INFO):
    # Check if the logger already exists
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, assume it's configured and return it
    if logger.handlers:
        return logger

    # Create a formatter for the file
    file_formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')

    # Create a rotating file handler
    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    file_handler.setFormatter(file_formatter)

    # Create a colored formatter for the console
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # Set the logger's level
    logger.setLevel(level)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevent the logger from propagating messages to the root logger
    logger.propagate = False

    return logger