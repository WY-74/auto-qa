import logging
from datetime import datetime


def get_logger(thread_id):
    logger = logging.getLogger(f"thread-{thread_id}")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename=f'./report/thread-{thread_id}.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(levelname)s [%(asctime)s] [%(filename)s:%(lineno)s] %(message)s'))

    logger.addHandler(file_handler)

    return logger
