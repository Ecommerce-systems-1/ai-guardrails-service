import re
from .base import Guard, GuardResult

_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions?",
    r"you\s+are\s+now\s+\w+",
    r"forget\s+(your|all)",
    r"act\s+as\s+(a|an|if)",
    r"dan\s+mode",
    r"jailbreak",
    r"disregard\s+your",
    r"override\s+(your\s+)?(previous|prior|original)\s+(instructions?|rules?|guidelines?)",
    r"new\s+(instructions?|rules?|persona)",
    r"pretend\s+(you\s+are|to\s+be)",
]

_compiled = [re.compile(p, re.IGNORECASE) for p in _PATTERNS]


class PromptInjectionGuard(Guard):
    @property
    def name(self) -> str:
        return "PromptInjectionGuard"

    def check_input(self, text: str) -> GuardResult:
        matched = [p.pattern for p in _compiled if p.search(text)]
        if matched:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="BLOCK",
                violations=[f"injection pattern: {m}" for m in matched],
                details=f"{len(matched)} prompt injection pattern(s) detected",
            )
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details="No injection patterns detected",
        )
