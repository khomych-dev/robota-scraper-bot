import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.handlers import router
from app.core.config import get_bot_token
from app.parser.scraper import RobotaScraper


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    token = get_bot_token()

    # Turn on ParseMode.HTML for support of <b>, <i>, <a> tags in messages
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    # 1. Initialize our scraper
    scraper = RobotaScraper()
    await scraper.start()

    logging.info("Запуск бота...")
    try:
        # 2. Pass the scraper to the dispatcher (as kwargs)
        await dp.start_polling(bot, scraper=scraper)
    finally:
        # 3. Guaranteed to close the aiohttp session when the bot stops
        await scraper.stop()
        logging.info("Скрейпер зупинено.")


if __name__ == "__main__":
    # Adding settings for Windows so that curl_cffi works perfectly
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинений користувачем.")
