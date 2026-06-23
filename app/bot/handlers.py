from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.database import Database
from app.parser.scraper import RobotaScraper

router = Router()
db = Database()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Command Handler /start."""
    await message.answer(
        "Привіт! 👋\n"
        "Я бот для пошуку вакансій на robota.ua.\n"
        "Натисни /search, щоб знайти свіжі вакансії для Python!"
    )


@router.message(Command("search"))
async def cmd_search(message: Message, scraper: RobotaScraper) -> None:
    """Command Handler /search. Searches for vacancies and filters out already seen ones."""
    await message.answer("🔍 Searching for fresh vacancies by the word <b>Python</b>...")

    try:
        # 1. Get all good vacancies (the same 18 pieces)
        all_good_vacancies = await scraper.scrape_vacancies("python")

        # 2. Filtering out vacancies that have already been seen.
        new_vacancies = []
        for vac in all_good_vacancies:
            if not db.is_seen(vac.link):
                new_vacancies.append(vac)

        # 3. If there are no new ones - say so
        if not new_vacancies:
            await message.answer(
                "🤷‍♂️ Нових цільових вакансій поки немає. Всі знайдені я вже надсилав раніше!"
            )
            return

        # 4. We only create posts for NEW job openings
        response = f"<b>🔥 Знайдено НОВИХ вакансій: {len(new_vacancies)}. Ось вони:</b>\n\n"
        for vac in new_vacancies:
            response += f"🔹 <b>{vac.title}</b>\n"
            response += f"🏢 Компанія: {vac.company}\n"
            response += f"🔗 <a href='{vac.link}'>Відкрити вакансію</a>\n\n"

        # 5. We're sending the completed list via Telegram
        await message.answer(response, disable_web_page_preview=True)

        # 6. Immediately after sending, we save them to the database!
        for vac in new_vacancies:
            db.mark_as_seen(vac.link)

    except Exception as e:
        await message.answer(f"❌ Виникла помилка: {e}")
