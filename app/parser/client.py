from typing import Any

from curl_cffi.requests import AsyncSession


class HTTPClient:
    """Asynchronous HTTP client that bypasses Cloudflare (impersonate)."""

    def __init__(self) -> None:
        # Use Any to prevent mypy from fussing about the complex C-library
        self.session: Any | None = None

    async def start(self) -> None:
        """Initializes the session, masking it as Google Chrome version 120."""
        if self.session is None:
            self.session = AsyncSession(impersonate="chrome120")

    async def stop(self) -> None:
        """Closes the session."""
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def get_html(self, url: str) -> str:
        """Executes a GET request and returns the HTML of the page."""
        if self.session is None:
            raise RuntimeError("HTTPClient session is not initialized. Call start() first.")

        response = await self.session.get(url)
        response.raise_for_status()

        return str(response.text)
