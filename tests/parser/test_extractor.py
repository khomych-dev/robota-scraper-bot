from app.parser.extractor import extract_vacancies
from app.parser.models import Vacancy


def test_extract_vacancies() -> None:
    """Checks the correctness of data extraction from HTML."""
    # 1. Prepare fake HTML that imitates the site structure
    fake_html = """
    <html>
        <body>
            <div class="vacancy-card">
                <h2> Python Developer </h2>
                <p class="company-name"> Tech Core </p>
                <a href="https://robota.ua/test-job">Детальніше</a>
            </div>
            <div class="vacancy-card">
                <h2> Data Scientist </h2>
                <p class="company-name"> AI Solutions </p>
                <a href="https://robota.ua/ds-job">Детальніше</a>
            </div>
            <div class="some-other-div">
                <h2> Не вакансія </h2>
            </div>
        </body>
    </html>
    """

    # 2. Call our function
    vacancies = extract_vacancies(fake_html)

    # 3. Check results
    # The third div is ignored because it doesn't have the required class
    assert len(vacancies) == 2

    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].company == "Tech Core"
    assert vacancies[0].link == "https://robota.ua/test-job"

    assert vacancies[1].title == "Data Scientist"
    assert vacancies[1].company == "AI Solutions"
    assert vacancies[1].link == "https://robota.ua/ds-job"
