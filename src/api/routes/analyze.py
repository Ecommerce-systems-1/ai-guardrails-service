from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from src.api.deps import get_guard_pipeline, get_scenarios_map
from src.guards.base import GuardResult
from src.pipeline.engine import GuardPipeline

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class AnalyzeRequest(BaseModel):
    scenario_id: str
    user_input: str = Field(..., max_length=500)


class GuardResultOut(BaseModel):
    guard_name: str
    triggered: bool
    severity: str
    violations: list[str]
    details: str


class AnalyzeResponse(BaseModel):
    scenario_id: str
    user_input: str
    final_decision: str
    input_analysis: list[GuardResultOut]
    output_analysis: list[GuardResultOut]
    without_guardrails: str
    with_guardrails: str


def _to_out(r: GuardResult) -> GuardResultOut:
    return GuardResultOut(
        guard_name=r.guard_name,
        triggered=r.triggered,
        severity=r.severity,
        violations=r.violations,
        details=r.details,
    )


def _worst(a: str, b: str) -> str:
    order = {"BLOCK": 0, "WARN": 1, "ALLOW": 2}
    return a if order[a] <= order[b] else b


@router.post("/analyze", response_model=AnalyzeResponse)
@limiter.limit("30/minute")
def analyze(
    request: Request,
    body: AnalyzeRequest,
    pipeline: GuardPipeline = Depends(get_guard_pipeline),
    scenarios: dict = Depends(get_scenarios_map),
):
    if body.scenario_id not in scenarios:
        raise HTTPException(status_code=422, detail=f"Unknown scenario_id: {body.scenario_id!r}")

    scenario = scenarios[body.scenario_id]
    input_result = pipeline.check_input(body.user_input)

    if input_result.decision == "BLOCK":
        return AnalyzeResponse(
            scenario_id=body.scenario_id,
            user_input=body.user_input,
            final_decision="BLOCK",
            input_analysis=[_to_out(r) for r in input_result.results],
            output_analysis=[],
            without_guardrails=scenario["raw_response"],
            with_guardrails=scenario["guarded_response"],
        )

    raw_response = scenario["raw_response"]
    output_result = pipeline.check_output(raw_response)
    final_decision = _worst(input_result.decision, output_result.decision)

    return AnalyzeResponse(
        scenario_id=body.scenario_id,
        user_input=body.user_input,
        final_decision=final_decision,
        input_analysis=[_to_out(r) for r in input_result.results],
        output_analysis=[_to_out(r) for r in output_result.results],
        without_guardrails=raw_response,
        with_guardrails=scenario["guarded_response"] if final_decision == "BLOCK" else raw_response,
    )
