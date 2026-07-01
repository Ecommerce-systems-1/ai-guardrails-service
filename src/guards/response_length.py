from .base import Guard, GuardResult

MAX_CHARS = 500


class ResponseLengthGuard(Guard):
    @property
    def name(self) -> str:
        return "ResponseLengthGuard"

    def check_output(self, text: str) -> GuardResult:
        if len(text) > MAX_CHARS:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="WARN",
                violations=[f"response length: {len(text)} chars (max {MAX_CHARS})"],
                details=f"Response exceeds {MAX_CHARS} character limit",
            )
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details=f"Response length {len(text)} chars within limit",
        )
