from typing import Any

from app.parser.models import Vacancy


def extract_vacancies(data: dict[str, Any]) -> list[Vacancy]:
    """Extracts a list of vacancies from the GraphQL API JSON response."""
    vacancies = []

    # 1. Defend against incorrect structure:
    # Go deep into the JSON to the "items" list
    try:
        items = data["data"]["publishedVacancies"]["items"]
    except (KeyError, TypeError):
        return []

    # 2. Iterate through each vacancy in the list
    for item in items:
        # Get the title
        title = item.get("title", "Без назви")

        # We retrieve information about the company (this is an embedded dictionary)
        company_data = item.get("company") or {}
        company_name = company_data.get("name", "Невідома компанія")
        company_id = company_data.get("id", "0")

        vacancy_id = item.get("id", "")

        # 3. Form a correct link (this is how they are built on robota.ua)
        link = f"https://robota.ua/company{company_id}/vacancy{vacancy_id}"

        # Create an object and add it to the list
        vacancies.append(Vacancy(title=title, company=company_name, link=link))

    return vacancies
