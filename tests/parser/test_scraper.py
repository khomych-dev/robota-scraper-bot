from unittest.mock import AsyncMock, patch

from app.parser.scraper import RobotaScraper


@patch("app.parser.client.HTTPClient.post_json")
async def test_scraper_pipeline(mock_post_json: AsyncMock) -> None:
    """Tests the scraper's operation using the GraphQL API."""

    # 1. Setting up a fake response from the API
    mock_post_json.return_value = {
        "data": {
            "publishedVacancies": {
                "items": [
                    {
                        "id": "999",
                        "title": "Backend Python",
                        "company": {"id": "888", "name": "Google"},
                    }
                ]
            }
        }
    }

    # 2. Initialize and start the scraper
    scraper = RobotaScraper()
    await scraper.start()

    # 3. Perform parsing for the word "python"
    vacancies = await scraper.scrape_vacancies("python")

    # 4. Checking the results
    assert len(vacancies) == 1
    assert vacancies[0].title == "Backend Python"
    assert vacancies[0].company == "Google"
    assert vacancies[0].link == "https://robota.ua/company888/vacancy999"

    # Checking that the correct URL was called
    mock_post_json.assert_called_once()
    args, kwargs = mock_post_json.call_args
    assert args[0] == "https://dracula.robota.ua/?q=getPublishedVacanciesList"

    await scraper.stop()
