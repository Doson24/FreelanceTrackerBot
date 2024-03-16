from data.database import SQLite_operations
from data.fetch_data import xml_parser_fl
from loguru import logger

from pathlib import Path

# Настройка логирования
# logger.add("logfile.log", rotation="500 MB", level="INFO")


def main():
    url = 'https://www.fl.ru/rss/all.xml'
    current_dir = Path.cwd()
    path_db = current_dir.joinpath('data/DB.db')
    db = SQLite_operations(path_db, 'FLru')

    logger.info(f"Начало обработки данных с URL: {url}")
    for task in xml_parser_fl():
        if not db.is_record_created(task.date_create):
            # Подготовка строки для вставки в SQL запрос
            columns = task.__dict__.keys()
            values = list(task.__dict__.values())

            try:
                db.insert_row(columns, values)
            except Exception as e:
                logger.error(f"Ошибка записи таска в БД: {e}")
            logger.info(f"Добавлен новый таск: {task.title}")

    logger.info("Обработка данных завершена")


if __name__ == '__main__':
    main()
