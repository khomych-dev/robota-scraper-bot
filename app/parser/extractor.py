from bs4 import BeautifulSoup

from app.parser.models import Vacancy


def extract_vacancies(html: str) -> list[Vacancy]:
    """
    Parses HTML page and extracts a list of vacancies.
    """
    # Initialize BeautifulSoup using the fast lxml parser
    soup = BeautifulSoup(html, "lxml")
    vacancies: list[Vacancy] = []

    # NOTE: This is a basic example (skeleton).
    # On the actual robota.ua website, the classes will be different,
    # we will update them later when we start testing the real site.
    cards = soup.find_all("div", class_="vacancy-card")

    for card in cards:
        title_elem = card.find("h2")
        company_elem = card.find("p", class_="company-name")
        link_elem = card.find("a")

        # If all required elements are found, create a Vacancy object
        if title_elem and company_elem and link_elem:
            vacancies.append(
                Vacancy(
                    title=title_elem.text.strip(),
                    company=company_elem.text.strip(),
                    link=str(link_elem.get("href", "")),
                )
            )

    return vacancies
