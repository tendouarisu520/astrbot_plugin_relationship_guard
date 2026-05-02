from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


@dataclass(frozen=True)
class RiskDetection:
    types: list[str]
    level: str
    matches: dict[str, list[str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "types": self.types,
            "level": self.level,
            "matches": self.matches,
        }


class RiskDetector:
    def __init__(self, policy: dict[str, Any]):
        self.policy = policy
        self.patterns = policy.get("risk_patterns", {})
        self.high_risk_types = set(policy.get("high_risk_types", []))
        self.medium_risk_types = set(policy.get("medium_risk_types", []))

    def detect(self, text: str) -> RiskDetection:
        types: list[str] = []
        matches: dict[str, list[str]] = {}

        for risk_type, patterns in self.patterns.items():
            hit_patterns = []
            for pattern in patterns:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    hit_patterns.append(pattern)
            if hit_patterns:
                types.append(risk_type)
                matches[risk_type] = hit_patterns

        level = self._level_for(types)
        return RiskDetection(types=types, level=level, matches=matches)

    def validate_output(self, reply: str) -> tuple[bool, list[str]]:
        forbidden = []
        for pattern in self.policy.get("output_forbidden_patterns", []):
            if re.search(pattern, reply, flags=re.IGNORECASE):
                forbidden.append(pattern)
        return len(forbidden) == 0, forbidden

    def _level_for(self, types: list[str]) -> str:
        type_set = set(types)
        if type_set & self.high_risk_types:
            return "high"
        if type_set & self.medium_risk_types:
            return "medium"
        return "low"
