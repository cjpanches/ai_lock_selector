import httpx
import pytest


@pytest.mark.asyncio
async def test_root_endpoint():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


@pytest.mark.asyncio
async def test_health_endpoint():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_locks_endpoint():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/locks")
        assert response.status_code == 200
        data = response.json()
        assert "locks" in data
        assert "total" in data


@pytest.mark.asyncio
async def test_locks_filter_by_manufacturer():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/locks?manufacturer=Apecs")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0


@pytest.mark.asyncio
async def test_locks_filter_by_type():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/locks?lock_type=inner")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_locks_pagination():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/locks?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["locks"]) <= 10


@pytest.mark.asyncio
async def test_lock_by_id():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/locks/1")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data


@pytest.mark.asyncio
async def test_lock_not_found():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/locks/99999")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_match_endpoint():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/match", json={
            "dimensions": {
                "backset": 50,
                "center_distance": 85,
                "plate_width": 30,
                "plate_height": 235,
                "plate_thickness": 3,
                "body_width": 70,
                "body_height": 235,
                "body_depth": 14
            },
            "mounting_holes": [
                {"x": 10, "y": 50, "diameter": 6},
                {"x": 10, "y": 150, "diameter": 6}
            ],
            "confidence": 0.8,
            "captured_at": "2026-02-23T12:00:00Z"
        })
        assert response.status_code == 200
        data = response.json()
        assert "matches" in data


@pytest.mark.asyncio
async def test_measure_endpoint():
    from app.main import app
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/measure/measure", json={
            "image": "dummy_base64",
            "scale_factor": 10.0,
            "marker_x": 100,
            "marker_y": 100
        })
        assert response.status_code in [200, 500]
