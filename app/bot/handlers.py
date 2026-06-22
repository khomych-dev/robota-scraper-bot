from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.parser.scraper import RobotaScraper

router = Router()


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
    """Command Handler /search. Searches for real vacancies."""
    await message.answer("🔍 Шукаю свіжі вакансії по слову <b>Python</b>...")

    try:
        # Now we simply pass the word for the search!
        vacancies = await scraper.scrape_vacancies("python")

        if not vacancies:
            await message.answer("🤷‍♂️ На жаль, вакансій не знайдено.")
            return

        # Let's create a nice message for the first 5 job openings
        response = f"<b>🔥 Знайдено вакансій: {len(vacancies)}. Ось вони:</b>\n\n"
        for vac in vacancies:
            response += f"🔹 <b>{vac.title}</b>\n"
            response += f"🏢 Компанія: {vac.company}\n"
            response += f"🔗 <a href='{vac.link}'>Відкрити вакансію</a>\n\n"

        # We're sending the completed list via Telegram
        await message.answer(response, disable_web_page_preview=True)

    except Exception as e:
        await message.answer(f"❌ Виникла помилка: {e}")
