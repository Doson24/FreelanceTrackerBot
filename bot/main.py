from datetime import datetime
import asyncio
from pathlib import Path

from aiogram import Bot
from loguru import logger
import sys

sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd().parent))

from data.database import SQLite_operations
import configparser
from datetime import datetime
import pytz

# Достать API_TOKEN из config.ini
config = configparser.ConfigParser()
dir_conf = Path.cwd()
# dir_conf = dir_conf.parent
dir_conf = dir_conf.joinpath('config.ini')

config.read(dir_conf)
API_TOKEN = config['telegram']['API_TOKEN']
CHAT_ID = config['telegram']['CHAT_ID']

krasnoyarsk_tz = pytz.timezone('Asia/Krasnoyarsk')
# Создаем экземпляр бота
bot = Bot(token=API_TOKEN)


def get_messages(start_time):
    current_time = datetime.now(krasnoyarsk_tz).strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Запрос сообщений с {start_time} по {current_time}")

    # Создаем объект Path для текущего каталога
    current_dir = Path.cwd()
    # dir_db = current_dir.parent
    dir_db = current_dir
    path_db = dir_db.joinpath('data/DB.db')

    db_kwork = SQLite_operations(path_db, 'kwork')
    messages_kwork = db_kwork.select_by_datetime(start_time)
    db_habr = SQLite_operations(path_db, 'habr_freelance')
    messages_habr = db_habr.select_by_datetime(start_time)
    db_fl = SQLite_operations(path_db, 'FLru')
    messages_fl = db_fl.select_by_datetime(start_time)

    logger.info(f"Найдено {len(messages_kwork) + len(messages_habr) + len(messages_fl)} "
                f"новых сообщений")

    return messages_kwork + messages_habr + messages_fl


def format_order_message(title, link, description, date_create,
                         price=None, high_price=None):
    message = f"📝 Название: {title}\n\n" + \
              (f"💰 {price}\n" if price else '') + \
              (f"💰 {high_price}\n" if high_price else '') + \
              f"🔗 Ссылка: {link}\n" \
              f"📄 Описание: {description}\n" \
              f"📅 Дата создания: {date_create}\n"
    return message


async def send_messages_to_chat(message):
    try:
        await bot.send_message(CHAT_ID, message, disable_notification=True, request_timeout=30)
        title = message.split('\n\n')[0]
        logger.info(f"Сообщение успешно отправлено в чат {title}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в чат: {e}")


async def main():
    # start_time = '2024-02-11 18:14:50'

    start_time = datetime.now(krasnoyarsk_tz).strftime("%Y-%m-%d %H:%M:%S")
    while True:
        messages = get_messages(start_time)
        if messages:
            start_time = datetime.now(krasnoyarsk_tz).strftime("%Y-%m-%d %H:%M:%S")
        for message in messages:
            format_message = format_order_message(*message)
            await send_messages_to_chat(format_message)
        await asyncio.sleep(60 * 2)


def run_telegram_wrapper():
    # Настройка логирования
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    run_telegram_wrapper()
