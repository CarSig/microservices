from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


@patch("services.breaches_service.fetch_breaches", return_value=[])
def test_breaches_empty(mock_service):
    """
    This safely tests the endpoint without needing a real DB.
    """
    response = client.get("/breaches")
    assert response.status_code == 200
    assert response.json() == []

@patch("services.breaches_service.fetch_breaches", return_value=[{"id": 1, "name": "Test Breach"}])
def test_breaches_non_empty(mock_service):
    """
    This safely tests the endpoint without needing a real DB.
    """
    response = client.get("/breaches/test")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Breach"}]