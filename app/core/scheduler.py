import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database import Database
from app.parser.scraper import RobotaScraper

logger = logging.getLogger(__name__)


async def scheduled_parsing_task(bot: Bot, scraper: RobotaScraper, db: Database, chat_id: int) -> None:
    """A background task for regularly parsing and submitting new job postings."""
    logger.info("Запуск планового парсингу...")

    try:
        all_vacancies = await scraper.scrape_vacancies("python")

        # We select only new job openings
        new_vacancies = [vac for vac in all_vacancies if not db.is_seen(vac.link)]

        if not new_vacancies:
            logger.info("Нових цільових вакансій не знайдено.")
            return

        response = f"<b>🔄 АВТОМАТИЧНИЙ ПОШУК: Знайдено НОВИХ вакансій: {len(new_vacancies)}.</b>\n\n"
        for vac in new_vacancies:
            response += f"🔹 <b>{vac.title}</b>\n"
            response += f"🏢 Компанія: {vac.company}\n"
            response += f"🔗 <a href='{vac.link}'>Відкрити вакансію</a>\n\n"

        await bot.send_message(chat_id=chat_id, text=response, disable_web_page_preview=True)

        for vac in new_vacancies:
            db.mark_as_seen(vac.link)

        logger.info(f"Успішно відправлено {len(new_vacancies)} нових вакансій.")

    except Exception as e:
        logger.error(f"Помилка під час планового парсингу: {e}")
        # Optional: Notify the administrator if the parser crashes
        await bot.send_message(chat_id=chat_id, text=f"❌ Помилка фонового парсингу: {e}")


def setup_scheduler(bot: Bot, scraper: RobotaScraper, db: Database, chat_id: int) -> AsyncIOScheduler:
    """Initializes and configures the task scheduler."""
    scheduler = AsyncIOScheduler()

    # Registering a task with an interval of 1 hour
    scheduler.add_job(
        scheduled_parsing_task,
        trigger="interval",
        hours=1,
        kwargs={"bot": bot, "scraper": scraper, "db": db, "chat_id": chat_id},
    )

    return scheduler
