from aiogram import Bot, Dispatcher, types
import sqlite3
from data.database import SQLite_operations

# Ваши данные для авторизации в Telegram
API_TOKEN = '5224696385:AAG23ZsTeQaW8dkhAUkT8w7a-0ybzKNcwJE'
# Получаем ID чата, в который будем отправлять сообщения
CHAT_ID = '-1002101634086'

# Создаем экземпляр бота
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(name=bot)

db = SQLite_operations('data/database.db', 'kwork')
messages = db.select_All('kwork')


# Отправляем сообщения в чат
async def send_messages_to_chat():
    for message in messages:
        await bot.send_message(CHAT_ID, message[0])


# Запускаем бота
async def main():
    await send_messages_to_chat()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
