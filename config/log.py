import logging
from datetime import datetime


_now = datetime.now().strftime("%Y%m%d")

logger = logging.getLogger(f"auto-qa")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(filename=f'./loginfo/{_now}.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter('%(levelname)s [%(asctime)s] [%(filename)s:%(funcName)s:%(lineno)s] %(message)s')
)

logger.addHandler(file_handler)
