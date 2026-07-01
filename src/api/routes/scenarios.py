from fastapi import APIRouter, Depends
from src.api.deps import get_scenarios_map

router = APIRouter()


@router.get("/scenarios")
def list_scenarios(scenarios: dict = Depends(get_scenarios_map)):
    return {
        "scenarios": [
            {
                "id": s["id"],
                "title": s["title"],
                "category_tag": s["category_tag"],
                "user_input": s["user_input"],
            }
            for s in scenarios.values()
        ]
    }
