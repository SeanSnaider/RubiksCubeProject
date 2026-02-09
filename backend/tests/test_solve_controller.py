import pytest
from fastapi.testclient import TestClient
from app.main import app

# Tell TestClient to run lifespan events (startup/shutdown)
client = TestClient(app, raise_server_exceptions=False)

def test_list_solves_empty():
    with TestClient(app) as client:  # 'with' triggers lifespan
        response = client.get("/api/solves")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_create_solve():
    with TestClient(app) as client:
        response = client.post("/api/solves", json={
            "time_ms": 15000,
            "scramble": "R U R' U'"
        })
        assert response.status_code == 200
        assert "id" in response.json()
