from app.parser.extractor import extract_vacancies
from app.parser.models import Vacancy


def test_extract_vacancies() -> None:
    """Checks the correctness of data extraction from JSON."""
    # 1. Prepare fake JSON that imitates the server response
    fake_json = {
        "data": {
            "publishedVacancies": {
                "items": [
                    {
                        "id": "111",
                        "title": "Python Developer",
                        "company": {"id": "222", "name": "Tech Core"},
                    },
                    {
                        "id": "333",
                        "title": "Data Scientist",
                        "company": {"id": "444", "name": "AI Solutions"},
                    },
                ]
            }
        }
    }

    # 2. Call our function
    vacancies = extract_vacancies(fake_json)

    # 3. Check results
    assert len(vacancies) == 2

    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].company == "Tech Core"
    assert vacancies[0].link == "https://robota.ua/company222/vacancy111"

    assert vacancies[1].title == "Data Scientist"
    assert vacancies[1].company == "AI Solutions"
    assert vacancies[1].link == "https://robota.ua/company444/vacancy333"


def test_extract_vacancies_empty() -> None:
    """Checks how the function handles empty or invalid JSON."""
    assert extract_vacancies({}) == []
    assert extract_vacancies({"data": None}) == []
