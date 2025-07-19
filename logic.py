import os
from datetime import datetime, timedelta
from typing import Dict, List

import requests

from config import REQUEST_URL, HEADERS, CLOUD_DIR, SELF_DIR


def get_self_folder_files(self_dir: str) -> Dict[str, str]:
    self_dir_files = {}

    for i in os.listdir(self_dir):
        time_sec = os.path.getmtime(os.path.join(self_dir, i))
        get_change_time = datetime.fromtimestamp(time_sec).strftime("%Y-%m-%d %H:%M:%S")
        self_dir_files[i] = get_change_time
        # print(i)
        # print(get_change_time)
    return self_dir_files


def get_files_from_cloud(path: str) -> Dict[str, str]:
    result = requests.get(f'{REQUEST_URL}?path={path}', headers=HEADERS)
    dir_files = result.json()['_embedded']['items']
    cloud_files = {}
    for i in dir_files:
        # print(type(i['created']))
        new_time = datetime.strptime(i['created'][:-6], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=3)
        cloud_files[i['name']] = datetime.strftime(new_time, "%Y-%m-%d %H:%M:%S")
        # print('new_time',new_time)

        # print(i['name'], i['created'])

    return cloud_files


def create_folder(folder: str) -> None:
    requests.put(f'{REQUEST_URL}?path={folder}', headers=HEADERS)


def delete_file_from_cloud(file: str, cloud_dir: str) -> None:
    requests.delete(f'{REQUEST_URL}?path={cloud_dir}/{file}', headers=HEADERS)


def upload_file_to_cloud(file: str, cloud_dir: str, replace: bool = True) -> None:
    res = requests.get(f'{REQUEST_URL}/upload?path={cloud_dir}%2f{file}&overwrite={replace}', headers=HEADERS).json()
    try:
        with open(file, 'rb') as f:
            requests.put(res['href'], files={'file': f})
    except Exception as exc:
        print(exc, type(exc))


def select_files_to_upload(
        self_files: Dict[str, str],
        cloud_files: Dict[str, str]
) -> List[str]:

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


self_files = get_self_folder_files(SELF_DIR)
cloud_files = get_files_from_cloud(CLOUD_DIR)

print(self_files)
print(cloud_files)

# [delete_file(i) for i in files_to_delete_from_cloud]

# if len(cloud_files) > len(self_files):
files_to_delete_from_cloud = cloud_files.keys() - self_files.keys()
print(files_to_delete_from_cloud)

select_files_to_upload(self_files, cloud_files)

# create_folder('test')
# delete_file_from_cloud('logic.py', CLOUD_DIR)

#upload_file_to_cloud('logic.py', CLOUD_DIR)

self_files = get_self_folder_files(SELF_DIR)
cloud_files = get_files_from_cloud(CLOUD_DIR)

print(self_files)
print(cloud_files)
