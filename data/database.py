import pandas as pd
import sqlite3


class SQLite_operations:

    def __init__(self, path, table_name):
        # self.df = df
        self.path = path
        self.table_name = table_name

    def add_data(self, df: pd.DataFrame, ):
        # Создание соединения с базой данных SQLite
        conn = sqlite3.connect(self.path)

        # Создание и добавление таблицы в базе данных
        # replace - удалить и вставить, append - добавить
        df.to_sql(self.table_name, conn, if_exists='append', index=False)
        print("Added in Database")

        # Закрытие соединения с базой данных
        conn.close()
        print("Connection closed")

    def create_table(self, conn: sqlite3.Connection):
        # Создание таблицы в базе данных SQLite
        # Возможно не работает
        cur = conn.cursor()
        cur.execute("CREATE TABLE table_name (col1 TEXT, col2 INTEGER, col3 REAL)")
        conn.close()

    def select_All(self, table_name):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        conn.close()
        return rows

    def insert_row(self, columns, values):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        # Создание SQL запроса с параметрами
        columns = ', '.join(columns)
        values_template = ', '.join(['?' for _ in values])
        sql_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values_template})"
        cur.execute(sql_query, values)
        conn.commit()
        conn.close()

    def is_record_created(self, date_create):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {self.table_name} WHERE date_create = '{date_create}'")
        rows = cur.fetchall()
        if len(rows) > 0:
            conn.close()
            return True
        else:
            conn.close()
            return False

    def check_by_name(self, title):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {self.table_name} WHERE title = '{title}'")
        rows = cur.fetchall()
        if len(rows) > 0:
            conn.close()
            return True
        else:
            conn.close()
            return False


if __name__ == "__main__":
    path = 'C:\\Users\\user\\Desktop\\Projects\\Price_monitoring\\Price_item\\online_markets.db'
    # data = select_All(path, 'AliExpress')
    # print(data)
    dns = SQLite_operations(path, 'DNS')
    dns.add_data(pd.DataFrame({'data': [1, 2, 3]}))
