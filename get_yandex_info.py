import os
from datetime import datetime, timedelta

import requests

from config import TOKEN

URL = "https://cloud-api.yandex.net/v1/disk/resources"

HEADERS = {'Content-Type': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
CLOUD_DIR = 'test'

directory = os.path.join(os.path.abspath(os.getcwd()), 'test')

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
        # print(type(i['created']))
        new_time = datetime.strptime(i['created'][:-6], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=3)
        cloud_files[i['name']] = datetime.strftime(new_time, "%Y-%m-%d %H:%M:%S")
        # print('new_time',new_time)

        # print(i['name'], i['created'])

    return cloud_files


def create_folder(folder):
    requests.put(f'{URL}?path={folder}', headers=HEADERS)


def delete_file(file, cloud_dir):
    requests.delete(f'{URL}?path={cloud_dir}/{file}', headers=HEADERS)


def upload_file(file, cloud_dir, replace=True):
    res = requests.get(f'{URL}/upload?path={cloud_dir}%2f{file}&overwrite={replace}', headers=HEADERS).json()
    with open(file, 'rb') as f:
        try:
            requests.put(res['href'], files={'file': f})
        except KeyError:
            print(res)


def select_files_to_upload(self_files, cloud_files):
    files_to_upload = []

    for file in self_files:
        if file in cloud_files:
            if cloud_files[file] < self_files[file]:
                files_to_upload.append(file)
                del cloud_files[file]
        else:
            files_to_upload.append(file)

    print('files_to_upload:', files_to_upload)
    return files_to_upload


self_files = get_self_folder_files(directory)
cloud_files = get_cloud_files(CLOUD_DIR)

print(self_files)
print(cloud_files)

# [delete_file(i) for i in files_to_delete_from_cloud]

# if len(cloud_files) > len(self_files):
files_to_delete_from_cloud = cloud_files.keys() - self_files.keys()
print(files_to_delete_from_cloud)

select_files_to_upload(self_files, cloud_files)

#create_folder('test/123')
#delete_file('123456', CLOUD_DIR)

#upload_file('logic.py', CLOUD_DIR)

self_files = get_self_folder_files(directory)
cloud_files = get_cloud_files(CLOUD_DIR)

print(self_files)
print(cloud_files)
