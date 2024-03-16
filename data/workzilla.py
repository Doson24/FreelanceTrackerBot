import datetime
import sys
import time
from pathlib import Path
from loguru import logger
import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd().parent))

from data.database import SQLite_operations
from data.fetch_data import HtmlGetter, Task

# logger.add("logfile.log", rotation="500 MB", level="DEBUG")

current_dir = Path.cwd()
# current_dir = current_dir.parent
path_db = current_dir.joinpath('data/DB.db')
db = SQLite_operations(path_db, 'workzilla')

COOKIES = {
    '_ym_uid': '1696324596336387749',
    '_ym_d': '1696324596',
    '__stripe_mid': '377979a6-a9c1-4ba5-8dde-e51a4df5ef4539850d',
    'lang': 'ru',
    'BrowserId': 'e5f17311-5e17-4b56-b99b-9348ec935224',
    'CookieUsage': 'Allowed',
    '_gid': 'GA1.2.977611700.1707566958',
    '.AspNetCore.Session': 'CfDJ8HOGXXUKPgNCnlycWaGpdZgSTgAl48E%2FXnKW3kCBS1okm4Qd1kfbxcPJkFFF5sQTRK%2F9qDhPO2rGV2R0doV7qbroFjbALyxU5xU4liALAKuOl68eurp3TT4fd51iy1VRpagOHBIePPCaHnXrSJRvAOgkuBiSGFGuDmSCzcW%2BPyyC',
    '_ga': 'GA1.2.1003714535.1705506348',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '__stripe_sid': '0ccc9e26-b900-4353-85f1-abedfa495b1af4d0d5',
    '_ga_NHGQ9RK9FC': 'GS1.1.1707671101.9.1.1707671172.57.0.0',
    'Bearer': 'CfDJ8HOGXXUKPgNCnlycWaGpdZhaCBewXM-trdxIH90-4TyIvmoGq3uomKyKcdOx6tjLq9kXDsf5sI6tKFFQUz3AsXxgeHIO7SHSE8-JWo-fp4sPYKMNnYH_Z2mfUvKs_QM4dFWCpFmM27onDd51NevxbQeFFEl_Y_vjZGorhrqsNw3_LWIPMvLUqvTRii-rYFbY7xwvU4c39rQyBKV8q4o5QdnXzqvvEMoD-_J8O64vbS_4LptvCS3tEfVIq6xouwc5Z4sti36etWCLRNVImVYvmJJZkj5JmL0QvG7Myr_w4khxXwYrrYvzAbOD9lMF_-_lqSFQu3OONIyCxw9CuD0rrj99Uvp9m10qG5WLlxtqPitF3jJb_05V7sivlzPCYMTt8YCSSKgs9ij_AcN9wTUnsyZpDl0vIGBwJCjlrfs2iLah5D5FrB9SG2w56-VuvWJrgjpX3x_zc-SkkcCs3Gj6M0z9zZEFrf2h31s7E9w-N3bR-McIpgMEJZwnicFjA5lhUXRvAU6DRtpPc3efT9d3E1iWJbpAUqrjQFVgqtfv8qq9Dtr2ALl1B8uAf5ar8fgxWuhC9moTQjdut2D228Xl5lDkgn00IJQS5YcD9QULJI4wAJaQo9vCICdnaOhUENMgETVXqp8ObDcANEpHDR-ATb6DiDimq90ENwtYkSxslo_NXSXNtNFxu5c17G9JgEKes_bEITR7QFQb3HsQPy8mKsz-0R5Ht5L9LC4cAD9AgFKss9LYx6WOqfORJ7sGmWnvfO_lGSA4axWTKc6KjaNxRzHKKY20Z7XmZpw3af_QwRMwXG8K9vQzL7pQZRq_qpYggHrZGieS0e6kJoUfU8nuYFA',
}

HEADERS = {
    'authority': 'client.work-zilla.com',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,ko;q=0.8',
    'agentid': 'fp21-08eae231330a64adb5d2a8d2832ce8d1',
    # 'cookie': '_ym_uid=1696324596336387749; _ym_d=1696324596; __stripe_mid=377979a6-a9c1-4ba5-8dde-e51a4df5ef4539850d; lang=ru; BrowserId=e5f17311-5e17-4b56-b99b-9348ec935224; CookieUsage=Allowed; _gid=GA1.2.977611700.1707566958; .AspNetCore.Session=CfDJ8HOGXXUKPgNCnlycWaGpdZgSTgAl48E%2FXnKW3kCBS1okm4Qd1kfbxcPJkFFF5sQTRK%2F9qDhPO2rGV2R0doV7qbroFjbALyxU5xU4liALAKuOl68eurp3TT4fd51iy1VRpagOHBIePPCaHnXrSJRvAOgkuBiSGFGuDmSCzcW%2BPyyC; _ga=GA1.2.1003714535.1705506348; _ym_isad=1; _ym_visorc=w; __stripe_sid=0ccc9e26-b900-4353-85f1-abedfa495b1af4d0d5; _ga_NHGQ9RK9FC=GS1.1.1707671101.9.1.1707671172.57.0.0; Bearer=CfDJ8HOGXXUKPgNCnlycWaGpdZhaCBewXM-trdxIH90-4TyIvmoGq3uomKyKcdOx6tjLq9kXDsf5sI6tKFFQUz3AsXxgeHIO7SHSE8-JWo-fp4sPYKMNnYH_Z2mfUvKs_QM4dFWCpFmM27onDd51NevxbQeFFEl_Y_vjZGorhrqsNw3_LWIPMvLUqvTRii-rYFbY7xwvU4c39rQyBKV8q4o5QdnXzqvvEMoD-_J8O64vbS_4LptvCS3tEfVIq6xouwc5Z4sti36etWCLRNVImVYvmJJZkj5JmL0QvG7Myr_w4khxXwYrrYvzAbOD9lMF_-_lqSFQu3OONIyCxw9CuD0rrj99Uvp9m10qG5WLlxtqPitF3jJb_05V7sivlzPCYMTt8YCSSKgs9ij_AcN9wTUnsyZpDl0vIGBwJCjlrfs2iLah5D5FrB9SG2w56-VuvWJrgjpX3x_zc-SkkcCs3Gj6M0z9zZEFrf2h31s7E9w-N3bR-McIpgMEJZwnicFjA5lhUXRvAU6DRtpPc3efT9d3E1iWJbpAUqrjQFVgqtfv8qq9Dtr2ALl1B8uAf5ar8fgxWuhC9moTQjdut2D228Xl5lDkgn00IJQS5YcD9QULJI4wAJaQo9vCICdnaOhUENMgETVXqp8ObDcANEpHDR-ATb6DiDimq90ENwtYkSxslo_NXSXNtNFxu5c17G9JgEKes_bEITR7QFQb3HsQPy8mKsz-0R5Ht5L9LC4cAD9AgFKss9LYx6WOqfORJ7sGmWnvfO_lGSA4axWTKc6KjaNxRzHKKY20Z7XmZpw3af_QwRMwXG8K9vQzL7pQZRq_qpYggHrZGieS0e6kJoUfU8nuYFA',
    'referer': 'https://client.work-zilla.com/freelancer',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
}

PARAMS = {
    'hideInsolvoOrders': 'false',
}


def main():
    url = 'https://client.work-zilla.com/api/order/v4/list/open'
    response = requests.get(url,
                            params=PARAMS, cookies=COOKIES,
                            headers=HEADERS)

    try:
        orders = response.json()['data']['other']
    except Exception as e:
        logger.error(f"Ошибка получения данных: {e}")
        return
    # {'id': 174, 'categoryId': 0,
    # 'subject': 'Настройка воронки в SendPulse', 'customerId': 0, 'status': 2,
    # 'duration': 57600000, 'archived': False, 'chatClosed': False, 'description': 'Настройка воронки в SendPulse из
    # готовых шаблонов.Сделать технические настройки автоворонки в SendPulse. Шаблоны писем уже готовы (15 писем).
    # Цель и условия воронки: довести подписчиков (регистрируются в разные дни за 2 недели до вебинара) до живого
    # вебинара и прогреть после. Важно чтоб независимо от даты подписки все получили письма дня вебинара и прогрева
    # после в одинаковое время.', 'price': 700.0, 'cityId': 0, 'files': [], 'freelancerEarn': 630.0, 'modified':
    # 1707367444652, 'isPremium': False, 'isTinkoffOrder': False, 'isYooKassaOrder': False, 'isInsolvoOrder': False,
    # 'isOfferOrder': False, 'isTestOptionSelected': False, 'isRaisePriceAvailable': True, 'isPremiumAvailable':
    # True, 'hasUnreadMark': False, 'showLeaveFeedbackButton': False, 'showAcceptTaskButton': False}
    for order in orders:
        title = order['subject']
        link = 'https://client.work-zilla.com/order/' + str(order['id'])
        description = order['description']
        date_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        price = order['price']

        task = Task(title, link, description, date_create, price)

        if not db.check_by_name(title):
            columns = task.__dict__.keys()
            values = list(task.__dict__.values())
            try:
                db.insert_row(columns, values)
                logger.info(f"Добавлен новый таск: {task.title}")
            except Exception as e:
                logger.error(f"Ошибка записи таска в БД: {task.title}\n{e}")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60 * 2)
