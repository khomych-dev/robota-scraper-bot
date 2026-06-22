from unittest.mock import AsyncMock, Mock, patch

from curl_cffi.requests import AsyncSession

from app.parser.client import HTTPClient


async def test_http_client_start_stop() -> None:
    """Checks if the session is created and closed correctly."""
    client = HTTPClient()
    assert client.session is None

    await client.start()
    assert isinstance(client.session, AsyncSession)

    await client.stop()
    assert client.session is None


@patch("curl_cffi.requests.AsyncSession.get")
async def test_http_client_get_html_success(mock_get: AsyncMock) -> None:
    """Checks if the client correctly returns HTML without a real request."""
    # 1. Creating a regular Mock for the response (since response is not a coroutine)
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    # In curl_cffi, text is a property, not a method
    mock_response.text = "<html>Test robota.ua</html>"

    # When await session.get() is called, return our mock_response
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
