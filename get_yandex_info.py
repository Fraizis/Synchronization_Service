import requests

from config import TOKEN

URL = "https://cloud-api.yandex.net/v1/disk/resources"

HEADERS = {'Content-Type': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
SAVE_DIR = 'test'

def get_folder_files(path):
    result = requests.get(f'{URL}?path={path}', headers=HEADERS)
    dir_files = result.json()['_embedded']['items']
    cloud_files = {}
    for i in dir_files:
        cloud_files[i['name']] = i['created']

        #print(i['name'], i['created'])

    print(cloud_files)



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


get_folder_files('test')

#create_folder('test/12345.docx')
#delete_folder('test/12345.docx')

upload_file('logic.py')
