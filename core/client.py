from dataclasses import dataclass
from typing import Any
import httpx

from core.utils.exception import BadRequest


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
            raise BadRequest(error)
