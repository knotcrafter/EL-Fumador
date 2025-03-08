import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

options = []  # Список вариантов

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎲 Рулетка")],
        [KeyboardButton(text="➕ Добавить")],
        [KeyboardButton(text="❌ Сброс")],
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: types.Message):
    user_name = message.from_user.full_name  # Берем имя пользователя из Telegram
    await message.answer(
        f"Привет, {user_name}! Это рулетка для выбора сигар. Добавь варианты и испытай удачу!",
        reply_markup=keyboard
    )


@dp.message(lambda message: message.text == "🎲 Рулетка")
async def spin_roulette(message: types.Message):
    if options:
        choice = random.choice(options)
        await message.answer(f"🎯 Выпало: {choice}")
    else:
        await message.answer("Список пуст. Добавьте варианты!")


@dp.message(lambda message: message.text == "➕ Добавить")
async def add_option_prompt(message: types.Message):
    await message.answer("Отправьте новый вариант для рулетки.")


@dp.message(lambda message: message.text == "❌ Сброс")
async def reset_options(message: types.Message):
    global options
    options = []
    await message.answer("✅ Список вариантов сброшен!")


@dp.message()
async def add_option(message: types.Message):
    options.append(message.text)
    await message.answer(f"Добавлено: {message.text}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
