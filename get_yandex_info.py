"""Модуль с классом для синхронизации"""

import time
from loguru import logger

from config import REQUEST_URL, HEADERS, CLOUD_DIR, SELF_DIR, SYNC_TIMEOUT
from logic import get_self_folder_files, get_files_from_cloud, create_folder, upload_file_to_cloud, \
    delete_file_from_cloud, select_files_to_upload, select_files_to_delete, check_path

logger.add("log_info.log")


class SyncYaCloud:
    """
    Класс с методами для синхронизации файлов локального пути с Яндекс диском
    """
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
        """
        Создать папку в "облаке"
        """
        create_folder(**self.get_data)

    def get_self_files(self):
        """
        Получить локальные файлы
        :return: Dict{str, str}
        """
        self_dir_files = get_self_folder_files(self.self_dir)
        return self_dir_files

    def get_cloud_files(self):
        """
        Получить файлы в облаке
        :return: Dict{str, str}
        """
        cloud_files = get_files_from_cloud(**self.get_data)
        return cloud_files

    def get_files_to_upload(self):
        """
        Получить список файлов для загрузки
        :return: List[str]
        """
        files_to_upload = select_files_to_upload(
            self.get_self_files(),
            self.get_cloud_files()
        )
        if not files_to_upload:
            logger.info('Nothing to upload')
        else:
            logger.info(f'Detect local change: {files_to_upload}')

        return files_to_upload

    def get_files_to_delete(self):
        """
        Получить список файлов для удаления
        :return: set{str}
        """
        files_to_delete = select_files_to_delete(
            self.get_self_files(),
            self.get_cloud_files()
        )
        if not files_to_delete:
            logger.info('Nothing to delete from cloud')
        else:
            logger.info(f'Files to delete from cloud: {files_to_delete}')

        return files_to_delete

    def upload_file(self, file):
        """
        Загрузить файл
        :param file: имя файла
        """
        upload_file_to_cloud(file, self.self_dir, **self.get_data)

    def delete_file(self, file):
        """
        Удалить файл
        :param file: имя файла
        """
        delete_file_from_cloud(file, **self.get_data)

    def run_app(self):
        """
        Запуск приложения
        """
        if not check_path(self.self_dir):
            logger.debug(f'{self.self_dir} такого пути не существует. Проверьте правильность пути')
            exit(404)

        logger.info('Starting synchronization')
        self.create_cloud_dir()
        [self.upload_file(i) for i in self.get_files_to_upload()]
        [self.delete_file(i) for i in self.get_files_to_delete()]
        logger.info(f'Local files: {sorted([item for item in self.get_self_files().keys()])}')
        logger.info(f'Cloud files: {[item for item in self.get_cloud_files().keys()]}')
        logger.info('Synchronization complete')
        logger.info(f'Next synchronization in {self.sync_timeout} sec')
        time.sleep(self.sync_timeout)
