import requests


URL = "https://cloud-api.yandex.net/v1/disk/resources?path=test"

headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

response = requests.get()
