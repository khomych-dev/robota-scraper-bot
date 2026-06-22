import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from app.bot.handlers import router
from app.core.config import get_bot_token


async def main() -> None:
    # 1. Set up logging (so you can see what the bot is doing in the terminal)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # 2. Get the bot token from our .env file
    token = get_bot_token()

    # 3. Initialize the bot and dispatcher
    bot = Bot(token=token)
    dp = Dispatcher()

    # 4. Let's register our router with handlers
    dp.include_router(router)

    # 5. Start Polling (the bot begins listening on Telegram)
    logging.info("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Let's run the asynchronous main() function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинений користувачем.")
