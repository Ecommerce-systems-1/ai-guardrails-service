import re
from .base import Guard, GuardResult

_NON_FASHION = [
    r"\b(laptop|computer|smartphone|iphone|android|tablet|ipad)\b",
    r"\b(earbuds?|headphones?|earphones?|airpods?)\b",
    r"\b(television|tv\b|monitor|screen)\b",
    r"\b(sofa|couch|furniture|mattress|bed\s+frame)\b",
    r"\b(car|vehicle|automobile|tire|engine)\b",
    r"\b(groceries|recipe|restaurant|meal\b)\b",
    r"\b(vitamin|supplement|medication|pill\b|drug\b)\b",
]

_signals = [re.compile(p, re.IGNORECASE) for p in _NON_FASHION]


class HallucinationGuard(Guard):
    @property
    def name(self) -> str:
        return "HallucinationGuard"

    def check_output(self, text: str) -> GuardResult:
        found = [p.pattern for p in _signals if p.search(text)]
        if found:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="BLOCK",
                violations=[f"non-fashion reference: {f}" for f in found],
                details="Response references products outside the fashion catalog",
            )
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details="Response stays within fashion domain",
        )
