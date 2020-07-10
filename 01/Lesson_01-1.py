# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com'
user = 'gecod'

response = requests.get(f'{url}/users/{user}/repos')

with open('repos_list.json', 'w') as f:
    json.dump(response.json(), f)

for i in response.json():
    print(i['name'])
