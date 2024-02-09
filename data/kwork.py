# Description: Этот файл содержит код для сбора данных с kwork.ru.
import datetime

import pandas as pd
from bs4 import BeautifulSoup

from data.database import SQLite_operations
from fetch_data import Task, get_html


def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    tasks = soup.find_all('div', class_='card__content')
    for task in tasks:
        header = task.find('div', class_='wants-card__header-title')
        title = header.text
        link = 'https://kwork.ru' + header.find('a').get('href')
        # price = task.find('div', class_='wants-card__header-price').text.split(':')[1]
        description = task.find('div', class_='breakwords first-letter overflow-hidden').text
        # Формат даты: 2021-08-25 12:00:00
        date_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield Task(title, link, description, date_create)


# Функция поиска последней страницы
def get_max_page(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.find('div', class_='paging')
    num_pages = pagination.find_all('li', class_='mr4')
    return num_pages[-1].text


def main():
    url = 'https://kwork.ru/projects?c=41'
    db = SQLite_operations('DB.db', 'kwork')
    page_html = get_html(url)
    for page in range(1, int(get_max_page(page_html)) + 1):
        url = f'https://kwork.ru/projects?c=41&page={page}'
        page_html = get_html(url)
        for task in parse_page(page_html):
            # Проверка на наличие записи в базе данных
            if not db.check_by_name(task.title):
                # Подготовка строки для вставки в SQL запрос
                columns = task.__dict__.keys()
                values = list(task.__dict__.values())
                # Добавление записи в базу данных
                db.insert_row(columns, values)
                print(task)


if __name__ == "__main__":
    main()
