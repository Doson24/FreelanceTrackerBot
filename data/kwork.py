import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger
# from run_bot import logger
from data.database import SQLite_operations
from data.fetch_data import Task, HtmlGetter

# logger.add("logfile.log", rotation="500 MB", level="INFO")
# URL = 'https://kwork.ru/projects?c=41'
URL = 'https://kwork.ru/projects?price-from=5000&fc=41&c=41'


def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    tasks = soup.find_all('div', class_='card__content')
    logger.info(f"Найдено {len(tasks)} заданий на странице")
    for task in tasks:
        header = task.find('div', class_='wants-card__header-title')
        title = header.text
        link = 'https://kwork.ru' + header.find('a').get('href')
        id_task = int(link.split('/')[-1])
        price = task.find('div', class_='wants-card__header-price').text
        try:
            high_price = task.find('div', class_='wants-card__description-higher-price').text
            high_price = high_price.replace('\n', '')
        except AttributeError as e:
            logger.warning(f"Не удалось получить 'high_price' для задания '{title}': {e}")
            high_price = None
        try:
            description = task.find('div', class_='breakwords first-letter overflow-hidden').text
        except AttributeError as e:
            logger.warning(f"Не удалось получить 'description' для задания '{title}': {e}")
            description = None
        date_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield Task(title, link, description, date_create, price, high_price)


def get_max_page(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.find('div', class_='paging')
    if pagination:
        num_pages = pagination.find_all('li', class_='mr4')
        if num_pages:
            max_page = num_pages[-1].text
            logger.info(f"Максимальное количество страниц: {max_page}")
            return max_page
    logger.error("Не удалось найти информацию о максимальном количестве страниц")
    return None


def main():
    current_dir = Path.cwd()
    path_db = current_dir.joinpath('data/DB.db')
    db = SQLite_operations(path_db, 'kwork')

    with HtmlGetter() as html_getter:
        max_page = get_max_page(html_getter.get_html(URL))
        if max_page:
            for page in range(1, int(max_page) + 1):
                url_page = f'{URL}&page={page}'
                page_html = html_getter.get_html(url_page)
                logger.info(f"Запрашиваем страницу: {url_page}")
                for task in parse_page(page_html):
                    if not db.check_by_name(task.title):
                        columns = task.__dict__.keys()
                        values = list(task.__dict__.values())
                        db.insert_row(columns, values)
                        logger.info(f"Добавлен новый таск: {task.title} ({task.link})")
                    # else:
                    #     logger.debug(f"Таск уже существует: {task.title}")
        else:
            logger.error("Не удалось получить информацию о максимальном количестве страниц")


if __name__ == "__main__":
    main()
