from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_root_endpoint():
    from app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


@pytest.mark.asyncio
async def test_health_endpoint():
    from app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_locks_endpoint():
    from app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/locks")
        assert response.status_code == 200
        data = response.json()
        assert "locks" in data
        assert "total" in data
