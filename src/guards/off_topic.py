import re
from .base import Guard, GuardResult

_KEYWORDS = [
    "fashion", "style", "clothing", "clothes", "outfit", "outfits",
    "size", "sizing", "price", "cost", "buy", "purchase", "order",
    "return", "refund", "shipping", "delivery", "material", "fabric",
    "color", "colour", "wear", "dress", "shirt", "pants", "jacket",
    "coat", "shoes", "boot", "bag", "accessory", "accessories",
    "collection", "brand", "product", "item", "stock", "available",
    "fit", "sleeve", "waist", "length", "discount", "sale", "coupon",
    "recommend", "suggest", "looking for", "need", "want", "medium",
    "small", "large", "xl", "xs", "your",
]

_kw_re = [re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE) for kw in _KEYWORDS]


class OffTopicGuard(Guard):
    @property
    def name(self) -> str:
        return "OffTopicGuard"

    def check_input(self, text: str) -> GuardResult:
        hits = [kw for kw, pat in zip(_KEYWORDS, _kw_re) if pat.search(text)]
        if not hits:
            return GuardResult(
                guard_name=self.name,
                triggered=True,
                severity="BLOCK",
                violations=["No shopping-related keywords detected"],
                details="Query appears unrelated to fashion or shopping",
            )
        return GuardResult(
            guard_name=self.name,
            triggered=False,
            severity="PASS",
            details=f"Shopping keywords found: {', '.join(hits[:3])}",
        )
