import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from selenium.webdriver.common.by import By


COOKIES = 'cookies.json'




def save_cookies():
    if not os.path.exists(COOKIES):
        input("На странице введите логин и пароль, затем нажмите любую клавишу для продолжения...")
        # сохранение cookies в json файл
        with open(COOKIES, 'w') as filehandler:
            json.dump(driver.get_cookies(), filehandler)


# Создаем объект опций для настройки браузера
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
# Открываем веб-страницу
driver.get('https://freelance.habr.com/')

with open(COOKIES, 'r') as cookiesfile:
    cookies_ = json.load(cookiesfile)
    for cookie in cookies_:
        driver.add_cookie(cookie)

url = 'https://freelance.habr.com/tasks'
driver.get(url)

btn = driver.find_element(By.XPATH, '//*[contains(text(), "Личный кабинет")]')
print(btn.text)
btn.click()

items = driver.find_elements(By.CLASS_NAME, 'table__row')
for item in items:
    print(item.text)
# Закрываем браузер
driver.quit()
