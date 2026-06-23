from typing import Any

from app.parser.models import Vacancy


def extract_vacancies(data: dict[str, Any]) -> list[Vacancy]:
    vacancies = []

    try:
        items = data["data"]["publishedVacancies"]["items"]
    except (KeyError, TypeError):
        return []

    for item in items:
        title = item.get("title", "Без назви")

        company_data = item.get("company") or {}
        company_name = company_data.get("name", "Невідома компанія")
        company_id = company_data.get("id", "0")

        vacancy_id = item.get("id", "")
        link = f"https://robota.ua/company{company_id}/vacancy{vacancy_id}"

        # NEW: Get the full job description
        description = item.get("description", "")

        # Add the description to our model
        vacancies.append(
            Vacancy(title=title, company=company_name, link=link, description=description)
        )

    return vacancies
