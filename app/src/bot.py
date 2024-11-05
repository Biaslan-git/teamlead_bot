import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import BotCommand, BotCommandScopeDefault

import config
from handlers.admin.handlers import router as router_admin
from handlers.developer.handlers import router as router_developer

# Bot token can be obtained via https://t.me/BotFather
TOKEN = config.BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.chat.id == config.ADMIN_ID:
        await message.answer('Вызовите команду /admin')
    else:
        await message.answer('Вызовите команду /auth')


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router_admin)
    dp.include_router(router_developer)

    commands = [
        BotCommand(command='start', description='Старт'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
