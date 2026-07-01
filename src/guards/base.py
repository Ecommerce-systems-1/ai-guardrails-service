from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class GuardResult:
    guard_name: str
    triggered: bool
    severity: Literal["BLOCK", "WARN", "PASS"]
    violations: list[str] = field(default_factory=list)
    details: str = ""


class Guard(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    def check_input(self, text: str) -> GuardResult:
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details="No input check implemented",
        )

    def check_output(self, text: str) -> GuardResult:
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details="No output check implemented",
        )
