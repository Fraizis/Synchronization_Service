"""Модуль с функциями для сервиса синхронизации"""

import os
from datetime import datetime, timedelta
from typing import Dict, List
import requests
from config import logger


def get_self_folder_files(self_dir: str) -> Dict[str, str]:
    """
    Функция для получения всех файлов по локальному пути
    :param self_dir: абсолютный путь локальной папки
    :return: словарь {'имя файла': 'дата изменения'}
    """
    self_dir_files = {}
    for file in os.listdir(self_dir):
        if os.path.isfile(os.path.join(self_dir, file)):
            time_sec = os.path.getmtime(os.path.join(self_dir, file))
            get_change_time = datetime.fromtimestamp(
                time_sec).strftime("%Y-%m-%d %H:%M:%S")
            self_dir_files[file] = get_change_time

    return self_dir_files


def get_files_from_cloud(
        cloud_dir: str,
        request_url: str,
        headers: Dict[str, str]
) -> Dict[str, str]:
    """
    Функция для получения всех файлов в хранилище
    :param cloud_dir: название папки в хранилище
    :param request_url: url сервиса
    :param headers: headers
    :return: словарь {'имя файла': 'дата изменения'}
    """
    result = requests.get(f'{request_url}?path={cloud_dir}', headers=headers)
    dir_files = result.json()['_embedded']['items']
    cloud_files = {}
    for i in dir_files:
        new_time = datetime.strptime(
            i['created'][:-6], "%Y-%m-%dT%H:%M:%S"
        ) + timedelta(hours=3)

        cloud_files[i['name']] = datetime.strftime(
            new_time, "%Y-%m-%d %H:%M:%S"
        )

    return cloud_files


def create_folder(
        cloud_dir: str,
        request_url: str,
        headers: Dict[str, str]
) -> None:
    """
    Функция для создания папки в хранилище
    :param cloud_dir: название папки в хранилище
    :param request_url: url сервиса
    :param headers: headers
    """
    requests.put(f'{request_url}?path={cloud_dir}', headers=headers)


def delete_file_from_cloud(
        file: str,
        cloud_dir: str,
        request_url: str,
        headers: Dict[str, str]
) -> None:
    """
    Функция для удаления файла из хранилища
    :param file: имя файла
    :param cloud_dir: название папки в хранилище
    :param request_url: url сервиса
    :param headers: headers
    :return: словарь {'имя файла': 'дата изменения'}
    """
    requests.delete(f'{request_url}?path={cloud_dir}/{file}', headers=headers)


def upload_file_to_cloud(
        file: str,
        self_dir: str,
        cloud_dir: str,
        request_url: str,
        headers: Dict[str, str],
        replace: bool = True
) -> None:
    """
    Функция для загрузки файла в хранилище
    :param file: имя файла
    :param self_dir: абсолютный путь локальной папки
    :param cloud_dir: название папки в хранилище
    :param request_url: url сервиса
    :param headers: headers
    :param replace: автозамена файла
    :return: словарь {'имя файла': 'дата изменения'}
    """
    res = requests.get(
        f'{request_url}/upload?path={cloud_dir}%2F{file}&overwrite={replace}',
        headers=headers
    ).json()
    try:
        with open(f'{self_dir}/{file}', 'rb') as f:
            requests.put(res['href'], files={'file': f})
    except Exception as exc:
        print(exc, type(exc))


def select_files_to_upload(
        self_files: Dict[str, str],
        cloud_files: Dict[str, str]
) -> List[str]:
    """
    Функция для сравнения и загрузки локальных файлов в хранилище
    :param self_files: локальные файлы
    :param cloud_files: файлы в хранилище
    :return: список ['имя файла']
    """
    files_to_upload = []
    for file in self_files:
        if file in cloud_files:
            if cloud_files[file] < self_files[file]:
                files_to_upload.append(file)
        else:
            files_to_upload.append(file)
    return files_to_upload


def select_files_to_delete(
        self_files: Dict[str, str],
        cloud_files: Dict[str, str]
) -> set[str]:
    """
    Функция для сравнения и удаления файлов из хранилища
    :param self_files: локальные файлы
    :param cloud_files: файлы в хранилище
    :return: множество {'имя файла'}
    """
    files_to_delete = cloud_files.keys() - self_files.keys()
    return files_to_delete


def check_path(path: str) -> None:
    """
    Функция для проверки указанного пути
    """
    if not os.path.exists(path):
        logger.error(f'"{path}" такого пути не существует. Проверьте правильность пути')
        return False
    return True
        #exit()


def check_cloud_dir(dir: str) -> None:
    """
    Функция для проверки имени папки в удалённом хранилище
    """
    if not dir:
        logger.error(f'Введите название папки в удалённом хранилище')
        return False
    return True
        #exit()


def check_token(cloud_dir: str, request_url: str, headers: Dict[str, str]) -> None:
    """
    Функция для проверки токена
    """
    result = requests.get(f'{request_url}?path={cloud_dir}', headers=headers)
    if result.status_code != 200:
        logger.error(f'Неверный токен')
        return False
    return True
        #exit()


def check_timeout(timeout) -> (int, float):
    """
    Функция для проверки периода
    """
    try:
        sync_time = float(timeout)
        return sync_time
    except (ValueError, TypeError):
        logger.error(f'SYNC_TIMEOUT должен быть числом')
        exit()



if not (check_cloud_dir('') or check_path('config.py')):
    print('exit')
