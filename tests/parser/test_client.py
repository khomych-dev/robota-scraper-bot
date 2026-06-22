from unittest.mock import AsyncMock, Mock, patch

import aiohttp

from app.parser.client import HTTPClient


async def test_http_client_start_stop() -> None:
    """Checks if the session is created and closed correctly."""
    client = HTTPClient()
    assert client.session is None

    await client.start()
    assert isinstance(client.session, aiohttp.ClientSession)

    await client.stop()
    assert client.session is None


@patch("aiohttp.ClientSession.get")
async def test_http_client_get_html_success(mock_get: AsyncMock) -> None:
    """Checks if the client correctly returns HTML without a real request."""
    # 1. Setting up our fake (mock) response object
    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock()
    mock_response.text.return_value = "<html>Test robota.ua</html>"

    # This magic string is needed for the mock to work with 'async with'
    mock_response.__aenter__.return_value = mock_response

    # Telling the system: "When get() is called, return our mock_response"
    mock_get.return_value = mock_response

    # 2. Executing our real code
    client = HTTPClient()
    await client.start()

    html = await client.get_html("https://robota.ua/test")

    # 3. Checking results
    assert html == "<html>Test robota.ua</html>"
    mock_get.assert_called_once_with("https://robota.ua/test")
    mock_response.raise_for_status.assert_called_once()

    await client.stop()
