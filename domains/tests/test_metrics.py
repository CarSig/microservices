from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_endpoint_exists():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "http_requests_total" in r.text

def test_increment_after_request():
    # Call a real endpoint
    client.get("/health")

    # Fetch metrics
    r = client.get("/metrics")
    body = r.text

    assert 'http_requests_total{method="GET",path="/health"' in body    

def test_not_empty():
    client.get("/health")
    r = client.get("/metrics")

    lines = [l for l in r.text.splitlines() if l and not l.startswith("#")]
    assert len(lines) > 0


def _get_counter_value(metrics_text: str, needle: str) -> int:
    for line in metrics_text.splitlines():
        if line.startswith(needle):
            return int(float(line.split()[-1]))
    return 0


def test_request_counter_increments():
    before = client.get("/metrics").text

    client.get("/health")

    after = client.get("/metrics").text

    before_count = _get_counter_value(
        before, 'http_requests_total{method="GET",path="/health"'
    )
    after_count = _get_counter_value(
        after, 'http_requests_total{method="GET",path="/health"'
    )

    assert after_count == before_count + 1