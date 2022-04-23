# Взял для примера новый API Яндекс 360, который требует авторизации через oAuth авторизацию - мне это как раз нужно по работе
# Описание API: https://yandex.ru/dev/api360/
import json
from pprint import pprint
import requests
from variable import orgId, access_token
from new_user import info_new_user


class API360:
    def __init__(self, org_id, access_token):
        self.url = f"https://api360.yandex.net/directory/v1/org/{org_id}/"
        self.headers = {
            "Authorization": f"OAuth {access_token}"
        }

    def get_departments_list(self):
        """
        Чтение всех департаментов предприятия
        """
        response = requests.get(f"{self.url}departments", headers=self.headers)
        return response.json()

    def get_all_department_info(self):
        """
        Посмотреть информацию о подразделении
        :return: json с информацией о подразделении в компании
        """
        deps = []
        for dep in self.get_departments_list()["departments"]:
            response = requests.get(f"{self.url}departments/{dep['id']}", headers=self.headers)
            deps.append(response.json())
        return deps

    def get_all_users(self):
        """
        Get all users of the organisation
        :return:
        """
        response = requests.get(f"{self.url}users", headers=self.headers)
        pprint(response)
        return response.json()

    def get_all_users_id(self):
        """
        Get all users id in the organisation
        :return:
        """
        users = self.get_all_users()
        ids = []
        for user in users['users']:
            ids.append(user['id'])
        return ids

    def post_create_new_user(self, user_info):
        """
        Creating the new user with provided dict
        :param user_info: dict with the new user info
        :return: displays success or error message
        """
        response = requests.post(f"{self.url}users", json=user_info, headers=self.headers)
        if response.status_code == 200:
            print(f"User {user_info['nickname']} was created successfully")
        else:
            print(f"During creating user occured error: {response.content.decode(encoding='UTF-8')}")


if __name__ == "__main__":
    organisation = API360(orgId, access_token)
    # pprint(organisation.get_departments_list())
    # with open("file_output.txt", "w") as output:
    #     for dep in organisation.get_departments_list()["departments"]:
    #         output.write(f"{dep['name']}\n")
    # pprint(organisation.get_all_department_info())
    # pprint(organisation.get_all_users())
    pprint(organisation.get_all_users_id())
    # organisation.post_create_new_user(info_new_user)
