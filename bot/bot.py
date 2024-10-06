import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from utils import users_list


load_dotenv()
token = os.getenv('BOT_TOKEN')

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    result = await users_list()
    await message.answer(f"Hello {message.from_user.username} 👌\n"
                         f"Users ({len(result)}): {result}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())