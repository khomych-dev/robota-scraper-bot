from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

# Create a router for message handling
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handler for the /start command."""
    # Send a response to the user
    await message.answer(
        "Привіт! 👋\n"
        "Я бот для пошуку вакансій на robota.ua.\n"
        "Напиши мені що-небудь, і скоро я навчуся надсилати тобі вакансії!"
    )
