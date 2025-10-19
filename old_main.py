import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F


import asyncio


load_dotenv()
BOT_TOKEN = os.getenv('TG_API_KEY')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчики команд /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Ты запустил бота")

@dp.message(Command("about"))
async def about_command(message: types.Message):
    about_text = "Я бот, созданный для демонстрации обработки команд. Автор: [@AleksanderAstapov]."
    await message.answer(about_text)

count = 0
@dp.message(Command("tab"))
async def tab_command(message: types.Message):
    global count
    count = count+1
    tab_text = f"{count}"
    await message.answer(f"Вы воспользавались кнопкой Tab - {tab_text} раз")


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__== "__main__":
    asyncio.run(main())