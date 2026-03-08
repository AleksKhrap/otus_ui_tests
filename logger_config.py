import logging
import os
from datetime import datetime


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    log_filename = f"logs/test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger()
    logger.info(f"Лог-файл: {log_filename}")

    return logger
