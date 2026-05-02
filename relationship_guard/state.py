from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CharacterState:
    affection: int = 0
    relationship_stage: str = "stranger"
    inventory: dict[str, int] = field(default_factory=dict)
    daily_gift_count: int = 0
    flags: dict[str, bool] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CharacterState":
        return cls(
            affection=int(data.get("affection", 0)),
            relationship_stage=str(data.get("relationship_stage", "stranger")),
            inventory=dict(data.get("inventory", {})),
            daily_gift_count=int(data.get("daily_gift_count", 0)),
            flags=dict(data.get("flags", {})),
            metadata=dict(data.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "affection": self.affection,
            "relationship_stage": self.relationship_stage,
            "inventory": dict(self.inventory),
            "daily_gift_count": self.daily_gift_count,
            "flags": dict(self.flags),
            "metadata": dict(self.metadata),
        }

    def clone(self) -> "CharacterState":
        return CharacterState.from_dict(self.to_dict())

