import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List
import requests


def get_self_folder_files(self_dir: str) -> Dict[str, str]:
    self_dir_files = {}

    for file in os.listdir(self_dir):
        if os.path.isfile(os.path.join(self_dir, file)):
            # time_sec = os.path.getmtime(os.path.join(self_dir, file))
            # get_change_time = datetime.fromtimestamp(
            #     time_sec).strftime("%Y-%m-%d %H:%M:%S")

            self_dir_files[file] = calculate_file_hash(f'{self_dir}/{file}')

    return self_dir_files


def get_files_from_cloud(
        cloud_dir: str,
        request_url: str,
        headers: Dict[str, str]
) -> Dict[str, str]:

    result = requests.get(f'{request_url}?path={cloud_dir}', headers=headers)
    dir_files = result.json()['_embedded']['items']
    #print(dir_files)
    cloud_files = {}
    for i in dir_files:
        cloud_files[i['name']] = i['sha256']
        # new_time = datetime.strptime(
        #     i['created'][:-6], "%Y-%m-%dT%H:%M:%S"
        # ) + timedelta(hours=3)
        #
        # cloud_files[i['name']] = datetime.strftime(
        #     new_time, "%Y-%m-%d %H:%M:%S"
        # )

    return cloud_files


def create_folder(
        cloud_dir: str,
        request_url: str,
        headers: Dict[str, str]
) -> None:
    requests.put(f'{request_url}?path={cloud_dir}', headers=headers)


def delete_file_from_cloud(
        file: str,
        cloud_dir: str,
        request_url: str,
        headers: Dict[str, str]
) -> None:
    requests.delete(f'{request_url}?path={cloud_dir}/{file}', headers=headers)


def upload_file_to_cloud(
        file: str,
        self_dir: str,
        cloud_dir: str,
        request_url: str,
        headers: Dict[str, str],
        replace: bool = True
) -> None:
    res = requests.get(
        f'{request_url}/upload?path={cloud_dir}/{file}&overwrite={replace}',
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
    files_to_upload = []

    for file in self_files:
        if file in cloud_files:
            if cloud_files[file] != self_files[file]:
                print(cloud_files[file])
                print(self_files[file])
                files_to_upload.append(file)
        else:
            files_to_upload.append(file)
    return files_to_upload


def select_files_to_delete(
        self_files: Dict[str, str],
        cloud_files: Dict[str, str]
) -> set[str]:
    files_to_delete = cloud_files.keys() - self_files.keys()
    return files_to_delete


def calculate_file_hash(filepath):
    hash_object = hashlib.sha256()
    with open(filepath, 'rb') as file:
        while chunk := file.read(8192):
            hash_object.update(chunk)
    return hash_object.hexdigest()
