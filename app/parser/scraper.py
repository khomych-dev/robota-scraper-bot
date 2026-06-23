from typing import Any

from app.parser.client import HTTPClient
from app.parser.extractor import extract_vacancies
from app.parser.models import Vacancy


class RobotaScraper:
    """Main class for parsing vacancies (Facade)."""

    def __init__(self) -> None:
        self.client = HTTPClient()
        # This is the address of the robota.ua database (API)
        self.api_url = "https://dracula.robota.ua/?q=getPublishedVacanciesList"

    async def start(self) -> None:
        await self.client.start()

    async def stop(self) -> None:
        await self.client.stop()

    def _build_payload(self, keyword: str) -> dict[str, Any]:
        """Builds a GraphQL query for searching vacancies."""
        return {
            "operationName": "getPublishedVacanciesList",
            "variables": {
                "pagination": {"count": 100, "page": 0},
                "filter": {
                    "keywords": keyword,
                    "militaryVacancyDisplayMode": "APPENDED",
                    "metroBranches": [],
                    "additionalKeywords": "",
                    "branchIds": [],
                    "clusterKeywords": [],
                    "districtIds": [],
                    "gender": None,
                    "isForVeterans": False,
                    "isOfficeWithGenerator": False,
                    "isOfficeWithShelter": False,
                    "isReservation": False,
                    "location": {"longitude": 0, "latitude": 0},
                    "microDistrictIds": [],
                    "rubrics": [],
                    "salary": 0,
                    "scheduleIds": [],
                    "showAgencies": True,
                    "showOnlyNoCvApplyVacancies": False,
                    "showOnlyNotViewed": False,
                    "showOnlySpecialNeeds": False,
                    "showOnlyWithoutExperience": False,
                    "showWithoutSalary": True,
                },
                "sort": "BY_DATE",
            },
            "query": "query getPublishedVacanciesList($filter: PublishedVacanciesFilterInput!,"
            " $pagination: PublishedVacanciesPaginationInput!,"
            " $sort: PublishedVacanciesSortType!) {\n  publishedVacancies(filter: $filter,"
            " pagination: $pagination, sort: $sort) {\n    totalCount\n    items {\n"
            "      ...PublishedVacanciesItem\n      __typename\n    }\n    __typename\n  }"
            "\n}\n\nfragment PublishedVacanciesItem on Vacancy {\n  id\n  title\n  description\n"
            "  company {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n",
        }

    def _filter_vacancies(self, vacancies: list[Vacancy]) -> list[Vacancy]:
        """Filters job listings, keeping only those that are suitable for beginners."""
        # Our list of suggested words (feel free to add your own!)
        good_words = [
            "навчання",
            "можна без досвіду",
            "безкоштовне навчання",
            "без досвіду",
            "junior",
            "trainee",
            "студент",
            "intern",
            "стажист",
            "початківець",
            "без досвіду роботи",
        ]

        filtered = []
        for vac in vacancies:
            # Combine title and description into one lowercase string
            full_text = (vac.title + " " + vac.description).lower()

            # Check if at least one desired word is present in the text
            if any(word in full_text for word in good_words):
                filtered.append(vac)

        return filtered

    async def scrape_vacancies(self, keyword: str) -> list[Vacancy]:
        """
        Sends a request to the API, receives vacancies, and filters them.
        """
        payload = self._build_payload(keyword)
        json_response = await self.client.post_json(self.api_url, payload)

        # Get ALL vacancies (for example, 20 pieces)
        all_vacancies = extract_vacancies(json_response)

        # We run it through our Smart Filter
        good_vacancies = self._filter_vacancies(all_vacancies)

        return good_vacancies
