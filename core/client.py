from dataclasses import dataclass
from typing import Any
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

        async with httpx.AsyncClient() as client:
            headers: dict[str, str] = {"Authorization": f"Bearer {self.api_key}"}
            res: httpx.Response = await client.get(url, params=params, headers=headers)
        try:
            res.raise_for_status()
            return res
        except httpx.HTTPError as error:
            raise NewsAPIError(error)

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
