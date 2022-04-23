cd /путь/до/драйвера/
sudo chmod +x geckodriver
cd /путь/до/драйвера/
sudo chmod +x geckodriver
Теперь, когда вы будете запускать код в Python, вы должны указать Selenium на этот файл.

Python
from selenium import webdriver
 
driver = webdriver.Firefox('/путь/до/драйвера/geckodriver')
driver.get("http://www.google.com")