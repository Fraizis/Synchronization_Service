import time

from config import REQUEST_URL, HEADERS, CLOUD_DIR, SELF_DIR, SYNC_TIMEOUT
from logic import get_self_folder_files, get_files_from_cloud, create_folder, upload_file_to_cloud, \
    delete_file_from_cloud, select_files_to_upload, select_files_to_delete


class SyncYaCloud:
    def __init__(
            self,
            url=REQUEST_URL,
            headers=HEADERS,
            cloud_dir=CLOUD_DIR,
            self_dir=SELF_DIR,
            sync_timeout=SYNC_TIMEOUT
    ):
        self.self_dir = self_dir
        self.sync_timeout = sync_timeout
        self.get_data = {
            'cloud_dir': cloud_dir,
            'request_url': url,
            'headers': headers
        }

    def create_cloud_dir(self):
        create_folder(**self.get_data)

    def get_self_files(self):
        self_dir_files = get_self_folder_files(self.self_dir)
        return self_dir_files

    def get_cloud_files(self):
        cloud_files = get_files_from_cloud(**self.get_data)
        return cloud_files

    def get_files_to_upload(self):
        files_to_upload = select_files_to_upload(
            self.get_self_files(),
            self.get_cloud_files()
        )
        if not files_to_upload:
            print('Nothing to upload')
        else:
            print('files_to_upload:', files_to_upload)

        return files_to_upload

    def get_files_to_delete(self):
        files_to_delete = select_files_to_delete(
            self.get_self_files(),
            self.get_cloud_files()
        )
        if not files_to_delete:
            print('Nothing to delete')
        else:
            print('files_to_delete:', files_to_delete)

        return files_to_delete

    def upload_file(self, file):
        upload_file_to_cloud(file, self.self_dir, **self.get_data)

    def delete_file(self, file):
        delete_file_from_cloud(file, **self.get_data)

    def run_app(self):
        self.create_cloud_dir()
        print('self_dir_files:', self.get_self_files())
        print('cloud_files:', self.get_cloud_files())
        [self.upload_file(i) for i in self.get_files_to_upload()]
        [self.delete_file(i) for i in self.get_files_to_delete()]
        print('self_dir_files:', self.get_self_files())
        print('cloud_files:', self.get_cloud_files())
        print('Synchronization complete')
        time.sleep(self.sync_timeout)


sync_run = SyncYaCloud()

# print(sync_run.get_self_files())
# print(sync_run.get_cloud_files())

while True:
    sync_run.run_app()

# print(sync_run.get_self_files())
# print(sync_run.get_cloud_files())
