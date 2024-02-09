from aiogram import Bot, Dispatcher, types
import sqlite3

# Ваши данные для авторизации в Telegram
API_TOKEN = '5224696385:AAG23ZsTeQaW8dkhAUkT8w7a-0ybzKNcwJE'

# Создаем экземпляр бота
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

# Подключаемся к базе данных SQLite
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

# Получаем сообщения из базы данных
cursor.execute("SELECT message FROM messages")
messages = cursor.fetchall()

# Закрываем соединение с базой данных
conn.close()

# Получаем ID чата, в который будем отправлять сообщения
CHAT_ID = 'YOUR_CHAT_ID'


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
