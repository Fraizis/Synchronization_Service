import os

from dotenv import load_dotenv, find_dotenv

directory = os.path.abspath(os.getcwd())
files = os.listdir(directory)

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    SELF_PATH = os.getenv("SELF_PATH")
    CLOUD_DIR_NAME = os.getenv("CLOUD_DIR_NAME")
    SYNC_TIME = os.getenv("SYNC_TIME")
