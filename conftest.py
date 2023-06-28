from dataclasses import dataclass
from typing import Any
import httpx


article_dict: dict[str, Any] = {
    "source": {"id": "fake_id", "name": "fake_name"},
    "author": "fake_author",
    "title": "fake_title",
    "description": "fake_description",
    "url": "fake_url",
    "urlToImage": "fake_url_to_image",
    "publishedAt": "2023-06-09T17:28:51Z",
    "content": "fake_content",
}


@dataclass
class ResponseMock:
    status_code: int
    content: dict[str, Any]

    def raise_for_status(self) -> None:
        if self.status_code != 200:
            raise httpx.HTTPError("Hello Joaquim")

    def json(self) -> dict[str, Any]:
        return self.content
