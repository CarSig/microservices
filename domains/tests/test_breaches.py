from fastapi.testclient import TestClient
from unittest.mock import patch,AsyncMock
from app.main import app

client = TestClient(app)


@patch("app.repositories.breach_repo.get_all_breaches", new=AsyncMock(return_value=[]))

def test_breaches_empty():
    """
    This safely tests the endpoint without needing a real DB.
    """
    response = client.get("/breaches")
    assert response.status_code == 200
    assert response.json() ==  {"exposedBreaches": []}

