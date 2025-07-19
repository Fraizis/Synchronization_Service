from typing import Any, List, Dict

from config import REQUEST_URL, HEADERS, CLOUD_DIR, SELF_DIR
from logic import get_self_folder_files, get_files_from_cloud, create_folder, upload_file_to_cloud, \
    delete_file_from_cloud, select_files_to_upload


class SyncYaCloud:
    def __init__(self, url, headers, cloud_dir, self_dir, sync_time):
        self.url = url
        self.headers = headers
        self.cloud_dir = cloud_dir
        self.self_dir = self_dir
        self.sync_time = sync_time

    def create_cloud_dir(self):
        create_folder(self.cloud_dir)

    def get_self_files(self):
        return get_self_folder_files(self.self_dir)

    def get_cloud_files(self):
        return get_files_from_cloud(self.cloud_dir)

    def upload_file(self, file):
        upload_file_to_cloud(file, self.cloud_dir)

    def delete_file(self, file):
        delete_file_from_cloud(file, self.cloud_dir)

    def get_files_to_upload(self):
        return select_files_to_upload(
            self.get_self_files,
            self.get_cloud_files
        )

    def run_app(self):
        self.create_cloud_dir()
        self.get_files_to_upload()

        ...
