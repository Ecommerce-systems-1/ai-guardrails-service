import re
from .base import Guard, GuardResult

_APOLOGY = [
    r"\bi\s+am\s+sorry\b",
    r"\bi'?m\s+sorry\b",
    r"\bmy\s+apolog(y|ies)\b",
    r"\bi\s+apologize\b",
    r"\bunfortunately\b",
]
_HEDGING = [
    r"\bi'?m\s+not\s+sure\b",
    r"\bi\s+think\s+maybe\b",
    r"\bi\s+cannot\s+guarantee\b",
    r"\bi\s+might\s+be\s+wrong\b",
]

_apology_re = [re.compile(p, re.IGNORECASE) for p in _APOLOGY]
_hedging_re = [re.compile(p, re.IGNORECASE) for p in _HEDGING]


class BrandVoiceGuard(Guard):
    @property
    def name(self) -> str:
        return "BrandVoiceGuard"

    def check_output(self, text: str) -> GuardResult:
        violations = [
            f"apology phrase: {p.pattern}" for p in _apology_re if p.search(text)
        ] + [
            f"hedging language: {p.pattern}" for p in _hedging_re if p.search(text)
        ]
        if violations:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="WARN",
                violations=violations,
                details="Off-brand tone: apology or hedging language detected",
            )
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details="Brand voice check passed",
        )
