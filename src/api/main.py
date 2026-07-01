import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.api.deps import (
    get_guard_pipeline,
    get_scenarios_map,
    set_pipeline,
    set_scenarios,
)
from src.api.limiter import limiter
from src.api.routes.analyze import router as analyze_router
from src.api.routes.scenarios import router as scenarios_router
from src.pipeline.engine import GuardPipeline, get_pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    set_pipeline(get_pipeline())
    try:
        raw = json.loads(Path("data/scenarios.json").read_text())["scenarios"]
        set_scenarios({s["id"]: s for s in raw})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to load scenarios.json: {e}") from e
    yield


app = FastAPI(title="AI Guardrails Service", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(scenarios_router)


@app.get("/health")
def health(
    pipeline: GuardPipeline = Depends(get_guard_pipeline),
    scenarios: dict = Depends(get_scenarios_map),
):
    return {
        "status": "ok",
        "scenarios_loaded": len(scenarios),
        "guards_loaded": 9,
    }


static_dir = Path("frontend/out")
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
