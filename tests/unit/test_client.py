import json
from pathlib import Path
from typing import Any
import httpx
import pytest
from pytest_mock import MockerFixture
from conftest import ResponseMock
from core import Client
from core.models import NewsResponse, SearchEverything, SearchHeadlines
from core.utils.exception import NewsAPIError


@pytest.fixture
def client() -> Client:
    return Client(api_key="test")


@pytest.mark.asyncio
class TestClient:
    async def test_client_init(self) -> None:
        client: Client = Client(api_key="test")
        assert client.api_key == "test"

    @pytest.mark.parametrize(
        "status_code, expected, throwable",
        [
            (200, dict(holla="joaquim"), None),
            (400, dict(), NewsAPIError),
        ],
    )
    async def test_call(
        self,
        client: Client,
        status_code: int,
        expected: dict[str, Any],
        throwable: Exception | None,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch(
            "httpx.AsyncClient.get",
            return_value=ResponseMock(status_code, expected),
        )
        if throwable:
            with pytest.raises(throwable):
                await client._call("https://test.com", dict(fake="param"))
        else:
            res: httpx.Response = await client._call(
                "https://test.com", dict(fake="param")
            )
            assert res.status_code == status_code
            assert res.json() == expected

    @pytest.mark.parametrize(
        "data, throwable",
        [
            (json.loads(Path("tests/samples/everything.json").read_bytes()), None),
            (
                json.loads(Path("tests/samples/bad_data.json").read_bytes()),
                NewsAPIError,
            ),
        ],
    )
    async def test_get_everything(
        self,
        client: Client,
        data: dict[str, Any],
        throwable: Exception | None,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch("httpx.AsyncClient.get", return_value=ResponseMock(200, data))
        search: SearchEverything = SearchEverything(q="fake_query")
        if throwable:
            with pytest.raises(throwable):
                await client.get_everything(search)
        else:
            res: NewsResponse = await client.get_everything(search)
            assert res.status == "ok"
            assert res.total_results == 11959
            assert len(res.articles) == 100

    @pytest.mark.parametrize(
        "data, throwable",
        [
            (json.loads(Path("tests/samples/headlines.json").read_bytes()), None),
            (
                json.loads(Path("tests/samples/bad_data.json").read_bytes()),
                NewsAPIError,
            ),
        ],
    )
    async def test_get_headlines(
        self,
        client: Client,
        data: dict[str, Any],
        throwable: Exception | None,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch("httpx.AsyncClient.get", return_value=ResponseMock(200, data))
        search: SearchHeadlines = SearchHeadlines(q="fake_query", country="us")
        if throwable:
            with pytest.raises(throwable):
                await client.get_headlines(search)
        else:
            res: NewsResponse = await client.get_headlines(search)
            assert res.status == "ok"
            assert res.total_results == 36
            assert len(res.articles) == 20
