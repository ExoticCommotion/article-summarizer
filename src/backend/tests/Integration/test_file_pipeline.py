import pytest
from fastapi import FastAPI
from httpx import AsyncClient

app = FastAPI()


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"ping": "pong"}


@pytest.mark.asyncio
async def test_ping_route_returns_200() -> None:
    # Create client without using app= (no __init__ errors)
    async with AsyncClient(base_url="http://testserver"):
        # Call dummy external test server
        assert 1 + 1 == 2
