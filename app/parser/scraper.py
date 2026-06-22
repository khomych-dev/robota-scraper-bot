from app.parser.client import HTTPClient
from app.parser.extractor import extract_vacancies
from app.parser.models import Vacancy


class RobotaScraper:
    """Main class for parsing vacancies (Facade)."""

    def __init__(self) -> None:
        # Initialize our HTTP client when the scraper is created
        self.client = HTTPClient()

    async def start(self) -> None:
        """Starts internal processes (HTTP session)."""
        await self.client.start()

    async def stop(self) -> None:
        """Stops all processes and frees up resources."""
        await self.client.stop()

    async def scrape_vacancies(self, url: str) -> list[Vacancy]:
        """
        Downloads a page from the specified URL and returns a list of vacancies.
        """
        # 1. Load HTML through our client
        html = await self.client.get_html(url)

        # 2. Parse HTML and convert it into a list of objects
        vacancies = extract_vacancies(html)

        # 3. Return the final result
        return vacancies
