from datetime import datetime
import asyncio
from pathlib import Path

from aiogram import Bot
from loguru import logger

from data.database import SQLite_operations

# Ваши данные для авторизации в Telegram
API_TOKEN = '5224696385:AAG23ZsTeQaW8dkhAUkT8w7a-0ybzKNcwJE'
# Получаем ID чата, в который будем отправлять сообщения
CHAT_ID = '-1002101634086'

# Создаем экземпляр бота
bot = Bot(token=API_TOKEN)


def get_messages(start_time):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Запрос сообщений с {start_time} по {current_time}")

    # Создаем объект Path для текущего каталога
    current_dir = Path.cwd()
    dir_db = current_dir.parent
    path_db = dir_db.joinpath('data/DB.db')

    db = SQLite_operations(path_db, 'kwork')

    messages = db.select_by_datetime(start_time)

    logger.info(f"Найдено {len(messages)} новых сообщений")

    return messages


def format_order_message(title, link, description, date_create):
    message = f"📝 Название: {title}\n\n" \
              f"🔗 Ссылка: {link}\n" \
              f"📄 Описание: {description}\n" \
              f"📅 Дата создания: {date_create}\n"
    return message


async def send_messages_to_chat(message):
    try:
        await bot.send_message(CHAT_ID, message)
        logger.info("Сообщение успешно отправлено в чат")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в чат: {e}")


async def main():
    # start_time = '2024-02-10 00:14:50'
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    while True:
        messages = get_messages(start_time)
        if messages:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for message in messages:
            format_message = format_order_message(*message)
            await send_messages_to_chat(format_message)
        await asyncio.sleep(60 * 5)


def run_telegram_wrapper():
    # Настройка логирования
    logger.add("logfile.log", rotation="500 MB", level="DEBUG")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    run_telegram_wrapper()
