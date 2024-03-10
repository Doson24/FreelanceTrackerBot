import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytz


# dataclass для данных из xml
@dataclass
class Task:
    title: str
    link: str
    description: str
    date_create: str
    price: str = None
    high_price: str = None


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
        # преобразование text в формат sql DATETIME (YYYY-MM-DD HH:MM:SS)
        date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        # Изменить timezone на +7
        date = (date.astimezone(pytz.timezone('Asia/Novosibirsk'))
                .strftime("%Y-%m-%d %H:%M:%S"))

        yield Task(title, link, description, date)


class HtmlGetter:
    def __init__(self):
        self.options = Options()
        self.options.headless = True

    def __enter__(self):
        self.driver = webdriver.Chrome(options=self.options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def get_html(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        html = self.driver.page_source
        return html
