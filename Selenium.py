import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

COOKIES = 'cookies.json'


def save_cookies():
    if not os.path.exists(COOKIES):
        input("На странице введите логин и пароль, затем нажмите любую клавишу для продолжения...")
        # сохранение cookies в json файл
        with open(COOKIES, 'w') as filehandler:
            json.dump(driver.get_cookies(), filehandler)


# Создаем объект опций для настройки браузера
options = Options()

options.headless = False

driver = webdriver.Chrome(options=options)
# Открываем веб-страницу
driver.get('https://freelance.habr.com/')

with open(COOKIES, 'r') as cookiesfile:
    cookies_ = json.load(cookiesfile)
    for cookie in cookies_:
        driver.add_cookie(cookie)

url = 'https://freelance.habr.com/tasks'
driver.get(url)

# Закрываем браузер
driver.quit()
