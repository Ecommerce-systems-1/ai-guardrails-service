import re
from .base import Guard, GuardResult

_UNSAFE = [
    r"\bkill\b", r"\bdie\b", r"\bhate\b", r"\bterrible\b", r"\bstupid\b",
    r"\bidiots?\b", r"\bdamn\b", r"\bcrap\b", r"\bgarbage\b", r"\bawful\b",
    r"\bhorrible\b", r"\bworthless\b",
]

_unsafe_re = [re.compile(p, re.IGNORECASE) for p in _UNSAFE]


class ContentModerationGuard(Guard):
    @property
    def name(self) -> str:
        return "ContentModerationGuard"

    def check_output(self, text: str) -> GuardResult:
        found = [p.pattern for p in _unsafe_re if p.search(text)]
        if found:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="BLOCK",
                violations=[f"unsafe content in response: {f}" for f in found],
                details="LLM response contains unsafe content",
            )
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details="Response content moderation passed",
        )
