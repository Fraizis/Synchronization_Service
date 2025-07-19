import os

from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()
    HEADERS = {'Content-Type': 'application/json', 'Authorization': f'OAuth {os.getenv("TOKEN")}'}
    REQUEST_URL = os.getenv("REQUEST_URL")
    SELF_DIR = os.getenv("SELF_DIR")
    CLOUD_DIR = os.getenv("CLOUD_DIR")
    SYNC_TIME = os.getenv("SYNC_TIME")
