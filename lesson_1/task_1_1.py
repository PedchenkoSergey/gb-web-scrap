import json
import requests
from pprint import pprint
from variable import USER


url = f'https://api.github.com/users/{USER}/repos'


response = requests.get(url)
j_data = response.json()
# pprint(j_data)

with open("json_output", "w") as fp:
    json.dump(j_data, fp)


print(f"Список репозиториев на GitHub пользователя {USER}:")
for repo in j_data:
    print(repo['name'])



