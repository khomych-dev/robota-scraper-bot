from app.core.config import get_app_name


async def test_get_app_name() -> None:
    """Checks if the application name is correctly returned asynchronously."""
    name = await get_app_name()
    assert name == "robota-scraper-bot"
