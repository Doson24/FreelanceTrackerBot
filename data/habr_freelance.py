import pandas as pd

from data.fetch_data import xml_parser
from database import SQLite_operations


def main():
    url = "https://freelance.habr.com/user_rss_tasks/d%2FqjtQzYArzYp8hLYr4z0g=="
    db = SQLite_operations('DB.db', 'habr_freelance')
    for task in xml_parser(url):
        if not db.is_record_created(task.date_create):
            # Подготовка строки для вставки в SQL запрос
            columns = task.__dict__.keys()
            values = list(task.__dict__.values())

            db.insert_row(columns, values)
            print(task)


if __name__ == "__main__":
    main()
