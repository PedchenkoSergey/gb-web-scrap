from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from pprint import pprint
from typing import Dict, Any
import hashlib
import json
import requests
from bs4 import BeautifulSoup as bs
import time
import os

# Базу MongoDB развернул в docker контейнере: docker run -d -p 27017:27017 --name m1 mongo

class WebPortal:
    def __init__(self, base_url, url_params, headers, disk=False, cache=False):
        self.base_url = base_url
        self.url = base_url + url_params
        self.headers = headers
        self.pages = []
        self.pages_dom = []
        self.cache = cache
        self.vacancies = []

        if disk:
            self.read_portal_files()
        else:
            self.read_portal_web()

        self.scrape_vacancies()

    def read_portal_web(self):
        page = 0
        if not self.pages:
            if self.cache:
                try:
                    self.read_portal_file(page)
                except Exception:
                    self.get_page_web(page)
            else:
                self.get_page_web(page)
        pager = self.pages_dom[0].find('div', {'class': 'pager'})
        while pager.find('a', {'data-qa': 'pager-next'}):
            time.sleep(1)
            page = page + 1
            if self.cache:
                try:
                    self.read_portal_file(page)
                except Exception:
                    self.get_page_web(page)
            else:
                self.get_page_web(page)
            pager = self.pages_dom[-1].find('div', {'class': 'pager'})
            self.save_page_file()

    def get_page_web(self, page_num=0):
        response = requests.get(self.url + str(page_num), headers=headers)
        self.pages.append(response.text)
        self.pages_dom.append(bs(response.text, 'html.parser'))

    def save_page_file(self):
        with open(f"pages/page_{len(self.pages) - 1}.html", "w", encoding='utf-8') as f:
            f.write(self.pages[-1])

    def read_portal_files(self):
        files = os.listdir(path="./pages")
        for p in range(len(files)):
            with open(f"pages/page_{p}.html", "r", encoding='utf-8') as f:
                self.pages.append(f.read())
                self.pages_dom.append(bs(self.pages[p], 'html.parser'))

    def read_portal_file(self, page_num):
        with open(f"pages/page_{page_num}.html", "r", encoding='utf-8') as f:
            self.pages.append(f.read())
            self.pages_dom.append(bs(self.pages[-1], 'html.parser'))

    def scrape_vacancies(self):
        i = 0
        for p in self.pages_dom:
            vacancies = p.find_all('div', {'class': "vacancy-serp-item"})
            for vacancy in vacancies:
                vacancy_dict = {}
                vacancy_dict['site'] = self.base_url
                vacancy_dict['name'] = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
                vacancy_dict['link'] = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

                try:
                    vacancy_dict['employer'] = vacancy.find(
                        'a', {'data-qa': 'vacancy-serp__vacancy-employer'}).getText().replace('\xa0', ' ')
                except AttributeError:
                    vacancy_dict['employer'] = None

                try:
                    vacancy_dict['location'] = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-address'}).getText()
                except AttributeError:
                    vacancy_dict['location'] = None

                try:
                    vacancy_dict['compensation'] = ((
                        vacancy.find(
                            'span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText())).replace(
                        '\u202f', ''
                    )
                except AttributeError:
                    vacancy_dict['compensation'] = None

                if vacancy_dict['compensation']:
                    salary = vacancy_dict['compensation'].split()
                    vacancy_dict['compensation'] = {}
                    vacancy_dict['compensation']['currency'] = salary[-1]
                    if salary[0] == 'от':
                        vacancy_dict['compensation']['min'] = int(salary[1])
                        vacancy_dict['compensation']['max'] = None
                    elif salary[0] == 'до':
                        vacancy_dict['compensation']['min'] = None
                        vacancy_dict['compensation']['max'] = int(salary[1])
                    else:
                        vacancy_dict['compensation']['min'] = int(salary[0])
                        vacancy_dict['compensation']['max'] = int(salary[2])

                hash_vc_dict = self.dict_hash(vacancy_dict)
                vacancy_dict['_id'] = hash_vc_dict

                self.vacancies.append(vacancy_dict)

    def dict_hash(self, dictionary: Dict[str, Any]) -> str:
        """MD5 hash of a dictionary."""
        dhash = hashlib.md5()
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()


def store_db(portal, table):
    for vacancy in portal.vacancies:
        try:
            table.insert_one(vacancy)
        except DuplicateKeyError:
            print(f"Vacancy with id = {vacancy['_id']} already exists")


def get_filtered_salary(table, currency="руб.", salary=0):
    for doc in table.find({'$and': [
                                {'$or': [
                                    {'compensation.min': {'$gt': salary}},
                                    {'compensation.max': {'$gt': salary}}
                                ]},
                                {'compensation.currency': currency}]}):
        pprint(doc)


if __name__ == "__main__":
    client = MongoClient('127.0.0.1', 27017)
    db = client['hhru']
    vacancies = db.vacancies

    base_url = "https://hh.ru"
    url = '/search/vacancy/?text=data+engineer&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true&hhtmFrom=vacancy_search_list&page='
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.119 YaBrowser/22.3.0.2520 Yowser/2.5 Safari/537.36'}

    hhru = WebPortal(base_url, url, headers,
                     disk=True)  # If we have already downloaded source to minimize requests to the web portal
    # hhru = WebPortal(base_url, url, headers, cache=True)  # if we have something on disk and we would like to use it to optimize requests on the site
    # hhru = WebPortal(base_url, url, headers)  # fresh request tot the web site

    pprint(hhru.vacancies)
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(hhru.vacancies, f)

    store_db(hhru, vacancies)
    get_filtered_salary(vacancies, salary=200000)
