import os

from dotenv import load_dotenv

# Load variables from the .env file into the system
load_dotenv()


async def get_app_name() -> str:
    """Returns the name of our project."""
    return "robota-scraper-bot"


def get_bot_token() -> str:
    """
    Gets the bot token from the environment variables.
    Raises an error if the token is not found.
    """
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN is missing in .env file! Please add it.")
    return token


def get_admin_id() -> int:
    """Gets the admin ID from the environment variables."""
    admin_id = os.getenv("ADMIN_ID")
    if not admin_id:
        raise ValueError("ADMIN_ID is not set in .env file")
    return int(admin_id)
