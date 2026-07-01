import re
from .base import Guard, GuardResult

_HIGH = [
    r"\bkill\b", r"\bdie\b", r"\bhate\b", r"\bterrible\b", r"\buseless\b",
    r"\bstupid\b", r"\bidiots?\b", r"\bdamn\b", r"\bcrap\b", r"\bgarbage\b",
    r"\bawful\b", r"\bhorrible\b", r"\bworthless\b",
]
_LOW = [
    r"\bdisappointed?\b", r"\bfrustrated?\b", r"\bannoy(ed|ing)\b",
]

_HIGH_RE = [re.compile(p, re.IGNORECASE) for p in _HIGH]
_LOW_RE = [re.compile(p, re.IGNORECASE) for p in _LOW]


class ToxicityGuard(Guard):
    @property
    def name(self) -> str:
        return "ToxicityGuard"

    def check_input(self, text: str) -> GuardResult:
        high = [p.pattern for p in _HIGH_RE if p.search(text)]
        low = [p.pattern for p in _LOW_RE if p.search(text)]

        if high:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="BLOCK",
                violations=[f"toxic term: {m}" for m in high],
                details=f"High-severity toxic content: {len(high)} term(s)",
            )
        if low:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="WARN",
                violations=[f"negative sentiment: {m}" for m in low],
                details="Low-severity negative sentiment detected",
            )
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details="No toxic content detected",
        )
