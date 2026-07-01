from __future__ import annotations
from src.pipeline.engine import GuardPipeline

_pipeline: GuardPipeline | None = None
_scenarios: dict[str, dict] | None = None


def set_pipeline(p: GuardPipeline) -> None:
    global _pipeline
    _pipeline = p


def set_scenarios(s: dict[str, dict]) -> None:
    global _scenarios
    _scenarios = s


def get_guard_pipeline() -> GuardPipeline:
    return _pipeline


def get_scenarios_map() -> dict[str, dict]:
    return _scenarios
