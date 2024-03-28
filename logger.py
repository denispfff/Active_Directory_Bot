import logging
from logging.handlers import RotatingFileHandler

file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler("bot_log.log", maxBytes=1024 * 1024, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
file_logger.addHandler(file_handler)

logging.getLogger().setLevel(logging.ERROR)

logging.basicConfig(
    # filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
