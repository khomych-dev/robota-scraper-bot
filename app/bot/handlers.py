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
        "Я бот для пошуку вакансій.\n"
        "Натисни /search, щоб перевірити інтеграцію з парсером!"
    )


@router.message(Command("search"))
async def cmd_search(message: Message, scraper: RobotaScraper) -> None:
    """Command Handler /search."""
    await message.answer("🔍 Розумний пошук запущено. Йду на сайт...")

    # Placeholder URL for testing
    test_url = "https://robota.ua/"

    try:
        # Access our Facade!
        vacancies = await scraper.scrape_vacancies(test_url)

        if not vacancies:
            await message.answer(
                "✅ Запит пройшов успішно, HTML отримано!\n"
                "Але парсер повернув 0 вакансій.\n"
                "<i>(Це нормально, бо ми ще не налаштували реальні HTML-класи в extractor.py)</i>"
            )
            return

        # If we happen to find anything (we'll format the first 5)
        response = "<b>🔥 Знайдені вакансії:</b>\n\n"
        for vac in vacancies[:5]:
            response += f"🔹 <b>{vac.title}</b>\n"
            response += f"🏢 Компанія: {vac.company}\n"
            response += f"🔗 <a href='{vac.link}'>Відкрити</a>\n\n"

        # disable_web_page_preview=True removes the huge preview images from links
        await message.answer(response, disable_web_page_preview=True)

    except Exception as e:
        await message.answer(f"❌ Виникла помилка: {e}")
