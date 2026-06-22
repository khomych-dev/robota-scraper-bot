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
                "pagination": {"count": 20, "page": 0},
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
                "sort": "BY_BUSINESS_SCORE",
            },
            "query": "query getPublishedVacanciesList($filter: PublishedVacanciesFilterInput!,"
            " $pagination: PublishedVacanciesPaginationInput!,"
            " $sort: PublishedVacanciesSortType!) {\n  publishedVacancies(filter: $filter,"
            " pagination: $pagination, sort: $sort) {\n    totalCount\n    items {\n"
            "      ...PublishedVacanciesItem\n      __typename\n    }\n    __typename\n  }"
            "\n}\n\nfragment PublishedVacanciesItem on Vacancy {\n  id\n  title\n  company {\n"
            "    id\n    name\n    __typename\n  }\n  __typename\n}\n",
        }

    async def scrape_vacancies(self, keyword: str) -> list[Vacancy]:
        """
        Sends a request to the API and returns a list of vacancies by keyword.
        """
        # 1. Form the correct JSON for the query
        payload = self._build_payload(keyword)

        # 2. Send a POST request to the database
        json_response = await self.client.post_json(self.api_url, payload)

        # 3. Pass the response to the extractor
        vacancies = extract_vacancies(json_response)

        return vacancies
