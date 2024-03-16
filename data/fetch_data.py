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


def xml_parser_fl():
    cookies = {
        '__ddg1_': '4FXAIZvlPOzrqVF2CcsL',
        '_ym_uid': '1696255907687209983',
        '_ym_d': '1696255907',
        'mindboxDeviceUUID': '61935202-e2d0-4003-ab10-35f316b62bbd',
        'directCrm-session': '%7B%22deviceGuid%22%3A%2261935202-e2d0-4003-ab10-35f316b62bbd%22%7D',
        'cookies_accepted': '1',
        'carrotquest_device_guid': '35765593-e27f-48df-a0b6-b5b5e293fcbb',
        'user_device_id': 'zp3ud6xfywb7yaxiwnb3mop81fix1h2p',
        'nfastpromo_x': '%7B%22close%22%3A1%7D',
        'nfastpromo_open': '0',
        '_ga_KV4LQFT7ZN': 'GS1.1.1696351152.1.1.1696351438.0.0.0',
        'is_hide_bonus_plate': 'true',
        '_tm_lt_sid': '1707218039969.180025',
        '_ym_isad': '1',
        '_ym_visorc': 'w',
        '_gid': 'GA1.2.713486904.1710559237',
        '_ga_cid': '1808037002.1696255908',
        'new_pf0': '1',
        'new_pf10': '1',
        'hidetopprjlenta': '0',
        'XSRF-TOKEN': '7cSfhJyKRItUG8d5wzHGuJiqxTHuvr8clBY1Fe5T',
        'id': '8456393',
        'name': 'karbushev-19981',
        'pwd': 'f330fba96306bec433343eadb97af4fd',
        'PHPSESSID': '9IqiQIv3zJKIgtnllrTdOPpqXZQPmmepNHAbsfyN',
        'mobapp': '1710559844',
        'uechat_3_first_time': '1710563048418',
        'uechat_3_pages_count': '46',
        '_ga': 'GA1.1.1808037002.1696255908',
        '_ga_RD9LL0K106': 'GS1.1.1710559236.111.1.1710563279.0.0.0',
    }

    headers = {
        'authority': 'www.fl.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9,ko;q=0.8',
        'cache-control': 'max-age=0',
        # 'cookie': '__ddg1_=4FXAIZvlPOzrqVF2CcsL; _ym_uid=1696255907687209983; _ym_d=1696255907; mindboxDeviceUUID=61935202-e2d0-4003-ab10-35f316b62bbd; directCrm-session=%7B%22deviceGuid%22%3A%2261935202-e2d0-4003-ab10-35f316b62bbd%22%7D; cookies_accepted=1; carrotquest_device_guid=35765593-e27f-48df-a0b6-b5b5e293fcbb; user_device_id=zp3ud6xfywb7yaxiwnb3mop81fix1h2p; nfastpromo_x=%7B%22close%22%3A1%7D; nfastpromo_open=0; _ga_KV4LQFT7ZN=GS1.1.1696351152.1.1.1696351438.0.0.0; is_hide_bonus_plate=true; _tm_lt_sid=1707218039969.180025; _ym_isad=1; _ym_visorc=w; _gid=GA1.2.713486904.1710559237; _ga_cid=1808037002.1696255908; new_pf0=1; new_pf10=1; hidetopprjlenta=0; XSRF-TOKEN=7cSfhJyKRItUG8d5wzHGuJiqxTHuvr8clBY1Fe5T; id=8456393; name=karbushev-19981; pwd=f330fba96306bec433343eadb97af4fd; PHPSESSID=9IqiQIv3zJKIgtnllrTdOPpqXZQPmmepNHAbsfyN; mobapp=1710559844; uechat_3_first_time=1710563048418; uechat_3_pages_count=46; _ga=GA1.1.1808037002.1696255908; _ga_RD9LL0K106=GS1.1.1710559236.111.1.1710563279.0.0.0',
        'referer': 'https://www.fl.ru/projects/category/programmirovanie/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    }

    params = {
        # 'subcategory': '280',
        'category': '5',
    }

    response = requests.get('https://www.fl.ru/rss/all.xml', params=params, cookies=cookies, headers=headers)

    # Check the status code of the response
    if response.status_code != 200:
        raise Exception(f"HTTP error {response.status_code} when trying to get 'https://www.fl.ru/rss/all.xml'")

    # Parse the XML from the response content
    root = ET.fromstring(response.content)

    for item in root.findall("channel/item"):
        title = item.find("title").text
        link = item.find("link").text
        description = item.find("description").text
        date = item.find("pubDate").text
        # преобразование date в формат sql DATETIME (YYYY-MM-DD HH:MM:SS)
        date_gmt = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
        # Изменить timezone на +7
        date_out = (date_gmt.astimezone(pytz.timezone('Etc/GMT+10'))
                    .strftime("%Y-%m-%d %H:%M:%S"))
        yield Task(title, link, description, date_out)


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


if __name__ == "__main__":
    for task in xml_parser_fl():
        print(task)
    for task in xml_parser("https://freelance.habr.com/user_rss_tasks/d%2FqjtQzYArzYp8hLYr4z0g=="):
        print(task)
