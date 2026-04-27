"""Test health check endpoints."""

import pytest
from fastapi.testclient import TestClient

from sparrow.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "opensparrow-core"


def test_health_detailed(client):
    response = client.get("/api/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "subsystems" in data
