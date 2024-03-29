from pathlib import Path

import pandas as pd

from data.fetch_data import xml_parser
from data.database import SQLite_operations
from loguru import logger


def main():
    url = "https://freelance.habr.com/user_rss_tasks/d%2FqjtQzYArzYp8hLYr4z0g=="
    current_dir = Path.cwd()
    path_db = current_dir.joinpath('data/DB.db')
    db = SQLite_operations(path_db, 'habr_freelance')

    logger.info(f"Начало обработки данных с URL: {url}")
    for task in xml_parser(url):
        if not db.is_record_created(task.date_create):
            # Подготовка строки для вставки в SQL запрос
            columns = task.__dict__.keys()
            values = list(task.__dict__.values())

            try:
                db.insert_row(columns, values)
            except Exception as e:
                logger.error(f"Ошибка записи таска в БД: {e}")
            logger.info(f"Добавлен новый таск: {task.title}")
        # else:
        # logger.debug(f"Таск уже существует: {task}")
    logger.info("Обработка данных завершена")


if __name__ == "__main__":
    main()
