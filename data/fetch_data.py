import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# dataclass для данных из xml
@dataclass
class Task:
    title: str
    link: str
    description: str
    date_create: str


# Функция парсинга xml файла по ссылке
# https://freelance.habr.com/user_rss_tasks/d%2FqjtQzYArzYp8hLYr4z0g==
def xml_parser(url):
    response = requests.get(url)
    with open("tasks.xml", "wb") as file:
        file.write(response.content)

    tree = ET.parse("tasks.xml")
    root = tree.getroot()

    for item in root.findall("channel/item"):
        title = item.find("title").text
        link = item.find("link").text
        description = item.find("description").text
        date = item.find("pubDate").text
        # преобразование date в формат sql DATETIME (YYYY-MM-DD HH:MM:SS)
        date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S")

        yield Task(title, link, description, date)


def get_html(url):
    # Создаем экземпляр класса Options
    options = Options()
    # Включаем безголовый режим
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html