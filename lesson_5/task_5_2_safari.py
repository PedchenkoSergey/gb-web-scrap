import re
import time
import hashlib
import json
from typing import Dict, Any

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


# Базу MongoDB развернул в docker контейнере: docker run -d -p 27017:27017 --name m1 mongo

def dict_md5_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def store_db(obj_list, table, hash_func):
    for obj in obj_list:
        obj['_id'] = hash_func(obj)
        try:
            table.insert_one(obj)
        except DuplicateKeyError:
            print(f"Object with id = {obj['_id']} already exists")


driver = webdriver.Safari()
driver.maximize_window()
driver.get('https://www.mvideo.ru')

time.sleep(5)
wait = WebDriverWait(driver, 15)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//mvid-carousel/div[1]/div/button[2]")))
time.sleep(0.5)
button.click()
goods = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel//mvid-product-cards-group/div")

goods_name = []
goods_price = []
goods_price_promo = []
goods_bonus = []
for good in goods:
    if 'product-mini-card__name' in good.get_attribute("class"):
        print(good.text)
        goods_name.append(good.text)
    elif 'product-mini-card__price' in good.get_attribute("class"):
        print(int(re.findall(r'\d+',
                             good.find_element(By.XPATH, './/span[@class="price__main-value"]').text.replace(' ', ''))[
                      0]))
        goods_price.append(int(re.findall(r'\d+', good.find_element(By.XPATH,
                                                                    './/span[@class="price__main-value"]').text.replace(
            ' ', ''))[0]))
        try:
            print(int(good.find_element(By.XPATH, './/span[contains(@class, "price__sale-value")]').text.replace(' ',
                                                                                                                 '')))
            goods_price_promo.append(
                int(good.find_element(By.XPATH, './/span[contains(@class, "price__sale-value")]').text.replace(' ',
                                                                                                               '')))
        except Exception:
            print(None)
            goods_price_promo.append(None)
    elif 'product-mini-card__bonus-rubles' in good.get_attribute("class"):
        print(int(re.findall(r'\d+', good.text.replace(' ', ''))[0]))
        goods_bonus.append(int(re.findall(r'\d+', good.text.replace(' ', ''))[0]))

goods_list = []
for i in range(len(goods_name)):
    good_dict = {}
    good_dict['name'] = goods_name[i]
    good_dict['price'] = goods_price[i]
    good_dict['start_price'] = goods_price_promo[i]
    good_dict['bonus'] = goods_bonus[i]
    goods_list.append(good_dict)

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
tranding = db.tranding

store_db(goods_list, tranding, dict_md5_hash)
