import os
from datetime import datetime, timedelta

import requests

from config import TOKEN

URL = "https://cloud-api.yandex.net/v1/disk/resources"

HEADERS = {'Content-Type': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
SAVE_DIR = 'test'

directory = os.path.join(os.path.abspath(os.getcwd()), SAVE_DIR)

print(directory)


def get_self_folder_files(self_dir):
    self_dir_files = {}

    for i in os.listdir(self_dir):
        time_sec = os.path.getmtime(os.path.join(self_dir, i))
        get_change_time = datetime.fromtimestamp(time_sec).strftime("%Y-%m-%d %H:%M:%S")
        self_dir_files[i] = get_change_time
        # print(i)
        # print(get_change_time)
    return self_dir_files


def get_cloud_files(path):
    result = requests.get(f'{URL}?path={path}', headers=HEADERS)
    dir_files = result.json()['_embedded']['items']
    cloud_files = {}
    for i in dir_files:
        #print(type(i['created']))
        new_time = datetime.strptime(i['created'][:-6], "%Y-%m-%dT%H:%M:%S") + timedelta(hours = 3)
        cloud_files[i['name']] = datetime.strftime(new_time, "%Y-%m-%d %H:%M:%S")
        #print('new_time',new_time)

        #print(i['name'], i['created'])

    return cloud_files



def create_folder(path):
    requests.put(f'{URL}?path={path}', headers=HEADERS)


def delete_folder(path):
    requests.delete(f'{URL}?path={path}', headers=HEADERS)


def upload_file(loadfile, replace=True):
    """Загрузка файла.
    loadfile: Путь к загружаемому файлу
    replace: true or false Замена файла на Диске"""
    res = requests.get(f'{URL}/upload?path={SAVE_DIR}/{loadfile}&overwrite={replace}', headers=HEADERS).json()
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file':f})
        except KeyError:
            print(res)

self_files = get_self_folder_files(directory)
cloud_files = get_cloud_files(SAVE_DIR)

print(self_files)
print(cloud_files)
#create_folder('test/12345.docx')
#delete_folder('test/12345.docx')

#upload_file('logic.py')
