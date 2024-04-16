import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)

async def run_bot():

    bot = Bot(token="6028027938:AAFtbZSBZy8j8Lj6IVC0XunHOLh8HDfIyGg")
    dp = Dispatcher()
    
    registration_data = { }

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Привет! Я бот для записи на марафон. Пожалуйста, введите ваше ФИО.")

    @dp.message(Command("list"))
    async def cmd_list(message: types.Message):
        if registration_data:
            response = "Список зарегистрированных участников:\n"
            for user_id, info in registration_data.items():
                response += f"{info['fio']} - {info['race_type']} км\n"
            await message.answer(response)
        else:
            await message.answer("На данный момент нет зарегистрированных участников.")

    @dp.message()
    async def collect_data(message: types.Message):
        user_id = message.from_user.id
        if user_id not in registration_data:
            registration_data[user_id] = {"fio": message.text}
            await message.answer("Спасибо! Теперь введите тип забега (20 или 40 км).")
        elif "fio" in registration_data[user_id] and "race_type" not in registration_data[user_id]:
            if message.text.strip() in ["20", "40"]:
                registration_data[user_id]["race_type"] = message.text.strip()
                await message.answer(f"Вы зарегистрированы на забег {message.text} км. Ваше ФИО: {registration_data[user_id]['fio']}")
            else:
                await message.answer("Пожалуйста, выберите между 20 и 40 км для забега.")

    await dp.start_polling(bot)
