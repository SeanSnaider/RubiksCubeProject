"""
Tests for the /api/solves endpoints.

Tests marked `needs_mongo` talk to a real MongoDB (MONGODB_URL, default
localhost) and are skipped when none is reachable, so `pytest` passes on a
fresh clone. The rest check request validation and error handling, which work
with or without a database.
"""
import pytest
from fastapi.testclient import TestClient

from app.database import db
from app.main import app

# A well-formed ObjectId that no solve will have.
UNKNOWN_SOLVE_ID = "0123456789abcdef01234567"


@pytest.fixture(scope="module")
def client():
    """A TestClient with the app's lifespan (MongoDB connect) run once per module."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mongo_client(client):
    """The TestClient, skipping the test when MongoDB isn't reachable."""
    if not db.available:
        pytest.skip("MongoDB is not reachable")
    return client


def test_list_solves_returns_a_list(mongo_client):
    response = mongo_client.get("/api/solves/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_created_solve_keeps_its_mode(mongo_client):
    response = mongo_client.post("/api/solves/", json={
        "time_ms": 15000, "scramble": "", "mode": "timer",
    })
    assert response.status_code == 200
    solve_id = response.json()["id"]
    try:
        timer_solves = mongo_client.get("/api/solves/", params={"mode": "timer"}).json()
        assert solve_id in [s["_id"] for s in timer_solves]
    finally:
        mongo_client.delete(f"/api/solves/{solve_id}")


def test_unknown_solve_id_is_not_found(mongo_client):
    assert mongo_client.delete(f"/api/solves/{UNKNOWN_SOLVE_ID}").status_code == 404


def test_malformed_solve_id_is_not_found_rather_than_a_server_error(client):
    assert client.delete("/api/solves/not-an-id").status_code == 404
    assert client.patch("/api/solves/not-an-id", json={"penalty": "+2"}).status_code == 404


def test_impossibly_fast_solve_is_rejected(client):
    response = client.post("/api/solves/", json={"time_ms": 100, "scramble": "R U"})
    assert response.status_code == 422


def test_unknown_penalty_is_rejected(client):
    response = client.patch(f"/api/solves/{UNKNOWN_SOLVE_ID}", json={"penalty": "+4"})
    assert response.status_code == 422


def test_requests_fail_fast_with_503_when_mongo_is_down(client):
    if db.available:
        pytest.skip("MongoDB is reachable; nothing to check")
    response = client.get("/api/solves/")
    assert response.status_code == 503
    assert "MongoDB" in response.json()["detail"]
