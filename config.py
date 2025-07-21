"""Модуль с конфигом"""

import os

from dotenv import load_dotenv, find_dotenv
from loguru import logger

logger.add("log_info.log")

if not find_dotenv():
    logger.debug('Переменные окружения не загружены т.к отсутствует файл .env')
    exit()
else:
    load_dotenv()
    HEADERS = {'Content-Type': 'application/json', 'Authorization': f'OAuth {os.getenv("TOKEN")}'}
    REQUEST_URL = os.getenv("REQUEST_URL")
    SELF_DIR = os.getenv("SELF_DIR")
    CLOUD_DIR = os.getenv("CLOUD_DIR")
    SYNC_TIMEOUT = int(os.getenv("SYNC_TIMEOUT"))
