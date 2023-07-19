from dataclasses import dataclass
import functools
from types import TracebackType
from typing import Any, Type
import httpx
from core.models.article import NewsResponse
from core.models.search import SearchEverything, SearchHeadlines
from core.utils.exception import NewsAPIError

__all__: list[str] = ["Client"]


@dataclass
class Client:
    api_key: str

    async def _call(self, url: str, params: dict[str, Any]) -> httpx.Response:
        """Call the API.

        Args:
            url (str): The URL to call.
            params (dict[str, Any]): The parameters to pass to the API.

        Raises:
            BadRequest: If the request is bad.

        Returns:
            httpx.Response: The response from the API.
        """

        headers: dict[str, str] = {"Authorization": f"Bearer {self.api_key}"}
        res: httpx.Response = await self.session.get(
            url, params=params, headers=headers
        )
        try:
            res.raise_for_status()
        except httpx.HTTPError as error:
            raise NewsAPIError(error)
        return res

    async def get_everything(self, search: SearchEverything) -> NewsResponse:
        """Get everything from the API.

        Args:
            search (SearchEverything): The search parameters.

        Returns:
            NewsResponse: The response from the API.
        """

        res: httpx.Response = await self._call(
            "https://newsapi.org/v2/everything",
            search.model_dump(exclude_none=True, by_alias=True),
        )
        try:
            return NewsResponse(**res.json())
        except ValueError as error:
            raise NewsAPIError(error)

    async def get_headlines(self, search: SearchHeadlines) -> NewsResponse:
        """Get headlines from the API.

        Args:
            search (SearchHeadlines): The search parameters.

        Returns:
            NewsResponse: The response from the API.
        """

        res: httpx.Response = await self._call(
            "https://newsapi.org/v2/top-headlines",
            search.model_dump(exclude_none=True, by_alias=True),
        )
        try:
            return NewsResponse(**res.json())
        except ValueError as error:
            raise NewsAPIError(error)

    @functools.cached_property
    def session(self) -> httpx.AsyncClient:
        """The HTTPX session.

        Returns:
            httpx.AsyncClient: The HTTPX session.
        """

        return httpx.AsyncClient()

    async def __aenter__(self) -> "Client":
        """Enter the context manager.

        Returns:
            Client: The client.
        """

        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: str | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the context manager and close httpx session.

        Args:
            exc_type (Type[BaseException] | None): Error type.
            exc_value (str | None): Error value.
            traceback (TracebackType | None): Traceback error.

        Raises:
            exc_type: The error raised.
        """

        await self.session.aclose()
        if exc_type is not None:
            raise exc_type(exc_value, traceback)
