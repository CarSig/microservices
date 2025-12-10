from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


@patch("services.breach_service.fetch_all_breaches", return_value=[])
def test_breaches_empty(mock_service):
    """
    This safely tests the endpoint without needing a real DB.
    """
    response = client.get("/breaches")
    assert response.status_code == 200
    assert response.json() == []

