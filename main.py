import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.handlers import router
from app.core.config import get_admin_id, get_bot_token
from app.core.scheduler import setup_scheduler
from app.database import Database
from app.parser.scraper import RobotaScraper


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    token = get_bot_token()
    admin_id = get_admin_id()  # We retrieve your ID from .env

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    # 1. Initialize our scraper
    scraper = RobotaScraper()
    await scraper.start()
    db = Database()

    # 2. Configure and start the scheduler
    scheduler = setup_scheduler(bot, scraper, db, admin_id)
    scheduler.start()

    logging.info("Запуск бота та планувальника...")
    try:
        # 3. Pass scraper and db to our handlers
        await dp.start_polling(bot, scraper=scraper, db=db)
    finally:
        # 4. Guaranteed to stop everything when turned off
        scheduler.shutdown()
        await scraper.stop()
        db.close()
        logging.info("Бот, планувальник та скрейпер зупинені.")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинений користувачем.")
