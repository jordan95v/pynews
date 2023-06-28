from typing import Any
import httpx
import pytest
from pytest_mock import MockerFixture
from conftest import ResponseMock
from core.client import Client
from core.utils.exception import BadRequest


@pytest.mark.asyncio
class TestClient:
    async def test_client_init(self) -> None:
        client: Client = Client(api_key="test")
        assert client.api_key == "test"

    @pytest.mark.parametrize(
        "status_code, expected, throwable",
        [
            (200, dict(holla="joaquim"), None),
            (400, dict(), BadRequest),
        ],
    )
    async def test_call(
        self,
        status_code: int,
        expected: dict[str, Any],
        throwable: Exception | None,
        mocker: MockerFixture,
    ) -> None:
        client: Client = Client(api_key="test")
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
