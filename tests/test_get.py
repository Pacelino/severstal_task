import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app


@pytest.mark.asyncio
async def test_get_rolls():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        response = await ac.get("/api/rolls/")
        assert response.status_code == 200

        data = response.json()
        print(data)
        # assert len(data) == 2
        
@pytest.mark.asyncio
async def test_post_books():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        response = await ac.post("/api/add_rolls/", json={
            "length": 110,
            "weight": 110,
        })
        assert response.status_code == 200

        data = response.json()
        print(data)