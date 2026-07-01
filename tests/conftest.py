import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from src.api.deps import get_guard_pipeline, get_scenarios_map
from src.api.main import app
from src.pipeline.engine import GuardPipeline


@pytest.fixture(scope="session")
def pipeline():
    return GuardPipeline()


@pytest.fixture(scope="session")
def scenarios_map():
    raw = json.loads(Path("data/scenarios.json").read_text())["scenarios"]
    return {s["id"]: s for s in raw}


@pytest.fixture(scope="session")
def api_client(pipeline, scenarios_map):
    app.dependency_overrides[get_guard_pipeline] = lambda: pipeline
    app.dependency_overrides[get_scenarios_map] = lambda: scenarios_map
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
