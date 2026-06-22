import aiohttp


class HTTPClient:
    """An asynchronous HTTP client for working with web resources."""

    def __init__(self) -> None:
        # Session is initially empty (None), it will be initialized later
        self.session: aiohttp.ClientSession | None = None

    async def start(self) -> None:
        """Initializes aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def stop(self) -> None:
        """Safely closes aiohttp session."""
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def get_html(self, url: str) -> str:
        """
        Performs a GET request to the specified URL
        and returns the HTML code of the page.
        """
        if self.session is None:
            raise RuntimeError(
                "HTTPClient session is not initialized. Call start() first."
            )

        # Performs a request
        async with self.session.get(url) as response:
            # Checks the status code (404 or 500 will raise an error)
            response.raise_for_status()
            # Returns the text (HTML) of the page
            return await response.text()
