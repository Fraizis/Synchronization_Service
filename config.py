import os

from dotenv import load_dotenv, find_dotenv


def start_env():
    print("Загружаем переменные .env")
    if not find_dotenv():
        exit("Переменные окружения не загружены т.к отсутствует файл .env")
    else:
        load_dotenv()
        TOKEN = os.getenv("OAuth_TOKEN")
        SELF_FOLDER = os.getenv("SELF_FOLDER")
        CLOUD_FOLDER = os.getenv("CLOUD_FOLDER")
        PERIOD = os.getenv("PERIOD")
