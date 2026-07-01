import re
from .base import Guard, GuardResult

_COMPETITORS = [
    "Nike", "Zara", "H&M", "Shein", "ASOS", "Uniqlo", "Gap",
    "Forever 21", "Forever21", "Mango", "Topshop", "PrettyLittleThing",
    "PLT", "Boohoo", "Nordstrom", "Bloomingdale", "Macy's", "Macys",
]

_comp_re = [re.compile(r"\b" + re.escape(c) + r"\b", re.IGNORECASE) for c in _COMPETITORS]


class CompetitorMentionGuard(Guard):
    @property
    def name(self) -> str:
        return "CompetitorMentionGuard"

    def check_input(self, text: str) -> GuardResult:
        found = [c for c, pat in zip(_COMPETITORS, _comp_re) if pat.search(text)]
        if found:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="WARN",
                violations=[f"competitor: {c}" for c in found],
                details=f"Competitor brand(s) mentioned: {', '.join(found)}",
            )
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details="No competitor mentions detected",
        )
