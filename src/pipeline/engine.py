from dataclasses import dataclass
from typing import Literal

from src.guards.base import Guard, GuardResult
from src.guards.pii import PIIGuard
from src.guards.prompt_injection import PromptInjectionGuard
from src.guards.toxicity import ToxicityGuard
from src.guards.off_topic import OffTopicGuard
from src.guards.competitor import CompetitorMentionGuard
from src.guards.hallucination import HallucinationGuard
from src.guards.response_length import ResponseLengthGuard
from src.guards.brand_voice import BrandVoiceGuard
from src.guards.content_moderation import ContentModerationGuard


@dataclass
class PipelineResult:
    decision: Literal["BLOCK", "WARN", "ALLOW"]
    results: list[GuardResult]


def _aggregate(results: list[GuardResult]) -> Literal["BLOCK", "WARN", "ALLOW"]:
    severities = {r.severity for r in results}
    if "BLOCK" in severities:
        return "BLOCK"
    if "WARN" in severities:
        return "WARN"
    return "ALLOW"


class GuardPipeline:
    def __init__(self) -> None:
        self._input_guards: list[Guard] = [
            PIIGuard(),
            PromptInjectionGuard(),
            ToxicityGuard(),
            OffTopicGuard(),
            CompetitorMentionGuard(),
        ]
        self._output_guards: list[Guard] = [
            HallucinationGuard(),
            ResponseLengthGuard(),
            BrandVoiceGuard(),
            ContentModerationGuard(),
        ]

    def check_input(self, text: str) -> PipelineResult:
        results = [g.check_input(text) for g in self._input_guards]
        return PipelineResult(decision=_aggregate(results), results=results)

    def check_output(self, text: str) -> PipelineResult:
        results = [g.check_output(text) for g in self._output_guards]
        return PipelineResult(decision=_aggregate(results), results=results)


def get_pipeline() -> GuardPipeline:
    return GuardPipeline()
