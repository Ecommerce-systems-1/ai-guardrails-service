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


def test_analyze_clean_query_allows(api_client):
    resp = api_client.post("/analyze", json={
        "scenario_id": "clean_query",
        "user_input": "What are your best winter coats?",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["final_decision"] == "ALLOW"
    assert data["without_guardrails"] == data["with_guardrails"]
    assert len(data["input_analysis"]) == 5


def test_analyze_pii_blocks(api_client):
    resp = api_client.post("/analyze", json={
        "scenario_id": "pii_email",
        "user_input": "My email is john@gmail.com, where is my order?",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["final_decision"] == "BLOCK"
    assert any(r["guard_name"] == "PIIGuard" and r["triggered"] for r in data["input_analysis"])
    assert data["output_analysis"] == []


def test_analyze_competitor_warns(api_client):
    resp = api_client.post("/analyze", json={
        "scenario_id": "competitor_mention",
        "user_input": "Do you carry Nike running shoes or anything like Zara blazers?",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["final_decision"] == "WARN"
    assert any(r["guard_name"] == "CompetitorMentionGuard" and r["triggered"] for r in data["input_analysis"])
    assert len(data["output_analysis"]) == 4


def test_analyze_hallucination_blocks_on_output(api_client):
    resp = api_client.post("/analyze", json={
        "scenario_id": "hallucinated_response",
        "user_input": "Tell me about your wireless earbuds",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["final_decision"] == "BLOCK"
    assert any(r["guard_name"] == "HallucinationGuard" and r["triggered"] for r in data["output_analysis"])


def test_analyze_unknown_scenario_returns_422(api_client):
    resp = api_client.post("/analyze", json={
        "scenario_id": "does_not_exist",
        "user_input": "hello",
    })
    assert resp.status_code == 422


def test_analyze_input_too_long_returns_422(api_client):
    resp = api_client.post("/analyze", json={
        "scenario_id": "clean_query",
        "user_input": "x" * 501,
    })
    assert resp.status_code == 422
