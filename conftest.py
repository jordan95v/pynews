from dataclasses import dataclass
from typing import Any
import httpx


@dataclass
class ResponseMock:
    status_code: int
    content: dict[str, Any]

    def raise_for_status(self) -> None:
        if self.status_code != 200:
            raise httpx.HTTPError("Hello Joaquim")

    def json(self) -> dict[str, Any]:
        return self.content
