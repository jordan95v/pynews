import pytest
from core.client import Client


@pytest.mark.asyncio
class TestClient:
    async def test_client_init(self) -> None:
        client: Client = Client(api_key="test")
        assert client.api_key == "test"
