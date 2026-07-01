import re
from .base import Guard, GuardResult


def _luhn_valid(number: str) -> bool:
    digits = [int(d) for d in number if d.isdigit()]
    if len(digits) < 13 or len(digits) > 19:
        return False
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", re.IGNORECASE)
_PHONE = re.compile(r"\b(\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}\b")
_CARD = re.compile(r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b")
_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


class PIIGuard(Guard):
    @property
    def name(self) -> str:
        return "PIIGuard"

    def check_input(self, text: str) -> GuardResult:
        violations: list[str] = []

        for m in _EMAIL.finditer(text):
            local, domain = m.group().split("@", 1)
            violations.append(f"email: {local[:1]}***@{domain}")

        for m in _PHONE.finditer(text):
            violations.append(f"phone: ***-***-{m.group()[-4:]}")

        for m in _CARD.finditer(text):
            digits = re.sub(r"\D", "", m.group())
            if _luhn_valid(digits):
                violations.append(f"credit card: ****-****-****-{digits[-4:]}")

        for _ in _SSN.finditer(text):
            violations.append("SSN: ***-**-****")

        if violations:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="BLOCK",
                violations=violations,
                details=f"{len(violations)} PII entity(ies) detected",
            )
        return GuardResult(
            guard_name=self.name, triggered=False, severity="PASS", details="No PII detected"
        )
