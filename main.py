from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import asyncio
from aiogram.enums import ParseMode

from src import games
from aiogram.filters.command import Command

load_dotenv()
token = getenv('TOKEN')
assert token is not None, "Token is not set! Make sure .env file exists."
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command('ping'))
async def ping(message: types.Message):
    await message.reply('pong')


async def main():
    dp.include_router(games.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
