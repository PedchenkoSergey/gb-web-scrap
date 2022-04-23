from lxml import html
import requests
from datetime import datetime
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import Dict, Any
import hashlib
import json


def save_page():
    url = 'https://yandex.ru/news/?utm_source=main_stripe_big'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.119 YaBrowser/22.3.0.2520 Yowser/2.5 Safari/537.36'}

    response = requests.get(url, headers=headers)

    with open("yandex_news.html", "w") as f:
        f.write(response.text)


def load_page():
    with open("yandex_news.html", "r") as f:
        dom_text = f.read()
        dom = html.fromstring(dom_text)
    return dom


def store_db(list_dict, table):
    for el in list_dict:
        try:
            table.insert_one(el)
        except DuplicateKeyError:
            print(f"Element with id = {el['_id']} already exists")


def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


if __name__ == "__main__":
    save_page()  # Изначальная загрузка документа, не всегда сайт отвечает корректно, сохраняем локальную копию для удобства
    dom = load_page()

    news_list_dom = dom.xpath("//div[contains(@class,'news-top-flexible-stories')]/div")

    news_list = []
    for news in news_list_dom:
        new = {}
        new['name'] = news.xpath(".//a[@class='mg-card__link']/text()")[0].replace('\xa0', ' ')
        new['link'] = news.xpath(".//a[@class='mg-card__link']/@href")[0]
        new['source'] = news.xpath(".//a[@class='mg-card__source-link']/text()")[0]
        time = news.xpath(".//span[@class='mg-card-source__time']/text()")[0]
        new['date'] = f"{str(datetime.now().date())} {time}"
        new['_id'] = dict_hash(new)
        news_list.append(new)

    pprint(news_list)

    # Сохраняем в БД:
    client = MongoClient('127.0.0.1', 27017)
    db = client['ya_news']
    hot_news = db.hot_news

    store_db(news_list, hot_news)
