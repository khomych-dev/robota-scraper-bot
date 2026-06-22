from typing import Any

from curl_cffi.requests import AsyncSession


class HTTPClient:
    """Async HTTP client for working with robota.ua API."""

    def __init__(self) -> None:
        self.session: Any | None = None

    async def start(self) -> None:
        if self.session is None:
            self.session = AsyncSession(impersonate="chrome120")

    async def stop(self) -> None:
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def get_html(self, url: str) -> str:
        if self.session is None:
            raise RuntimeError("HTTPClient session is not initialized.")
        response = await self.session.get(url)
        response.raise_for_status()
        return str(response.text)

    async def post_json(self, url: str, json_data: dict[str, Any]) -> dict[str, Any]:
        """Makes a POST request with JSON data and returns a JSON response."""
        if self.session is None:
            raise RuntimeError("HTTPClient session is not initialized.")

        response = await self.session.post(url, json=json_data)

        if response.status_code != 200:
            error_msg = response.text
            raise RuntimeError(
                f"HTTP {response.status_code}. Деталі від сервера: {error_msg[:800]}"
            )

        return dict(response.json())
