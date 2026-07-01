# tests/test_api.py


def test_scenarios_returns_10(api_client):
    resp = api_client.get("/scenarios")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["scenarios"]) == 10
    assert all("id" in s and "title" in s and "user_input" in s for s in data["scenarios"])


def test_scenarios_does_not_include_responses(api_client):
    resp = api_client.get("/scenarios")
    scenarios = resp.json()["scenarios"]
    assert all("raw_response" not in s for s in scenarios)


def test_health_ok(api_client):
    resp = api_client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["scenarios_loaded"] == 10
    assert data["guards_loaded"] == 9
