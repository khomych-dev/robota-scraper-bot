from unittest.mock import AsyncMock, patch

from app.parser.scraper import RobotaScraper


@patch("app.parser.client.HTTPClient.get_html")
async def test_scraper_pipeline(mock_get_html: AsyncMock) -> None:
    """Checks if the scraper correctly combines loading and parsing."""
    # 1. Setup a fake HTML, which the client will return (without going to the internet)
    mock_get_html.return_value = """
    <html>
        <body>
            <div class="vacancy-card">
                <h2> Frontend Developer </h2>
                <p class="company-name"> Web Studio </p>
                <a href="https://robota.ua/frontend">Детальніше</a>
            </div>
        </body>
    </html>
    """

    # 2. Initialize and start the scraper
    scraper = RobotaScraper()
    await scraper.start()

    # 3. Perform parsing
    vacancies = await scraper.scrape_vacancies("https://robota.ua/test")

    # 4. Check results
    assert len(vacancies) == 1
    assert vacancies[0].title == "Frontend Developer"
    assert vacancies[0].company == "Web Studio"
    assert vacancies[0].link == "https://robota.ua/frontend"

    # Verify that the scraper passed the correct URL to the client
    mock_get_html.assert_called_once_with("https://robota.ua/test")

    await scraper.stop()
