import asyncio
from aiogram import Bot, Dispatcher
from aiogram_bot.handlers import command, callback

from config_reader import config

import win32serviceutil
import win32service
import win32event
import servicemanager


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(command.router)
    dp.include_router(callback.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
