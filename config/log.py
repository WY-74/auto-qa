import logging
from datetime import datetime


def get_logger():
    _now = datetime.now().strftime("%Y%m%d")

    logger = logging.getLogger(f"auto-qa")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename=f'./report/{_now}.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(levelname)s [%(asctime)s] [%(filename)s:%(lineno)s] %(message)s'))

    logger.addHandler(file_handler)

    return logger
