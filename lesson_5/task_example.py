from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Safari()

driver.get('https://5ka.ru/special_offers')

time.sleep(60)
print()
wait = WebDriverWait(driver, 120)

button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cookie-message page-container']//button")))
print(f'The first button: {button}')
button.click()
actions = ActionChains(driver)
actions.move_to_element(articles[-1])
actions.perform()

button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn-main focus-btn red small']")))
print(f'The second button: {button}')
button.click()

page = 0
while page < 3:
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='add-more-btn']")))
        # button = driver.find_element(By.XPATH, "//button[@class='add-more-btn']")
        button.click()
        page += 1
    except exceptions.TimeoutException:
        print("РљРЅРѕРїРєР° Р±РѕР»РµРµ РЅРµ РґРѕСЃС‚СѓРїРЅР°")
        break

time.sleep(.5)
goods = driver.find_elements(By.XPATH, "//div[@class='product-card item']")

for good in goods:
    print(good.find_element(By.XPATH, ".//div[@class='item-name']").text)

# if __name__ == "__main__":
#     pass
