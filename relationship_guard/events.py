from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


@dataclass(frozen=True)
class UserEvent:
    type: str
    item: str | None = None
    place: str | None = None
    claimed_amount: int | None = None
    content: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "item": self.item,
            "place": self.place,
            "claimed_amount": self.claimed_amount,
            "content": self.content,
        }


class EventExtractor:
    def __init__(self, known_gifts: list[str] | None = None):
        self.known_gifts = known_gifts or ["玫瑰", "花", "巧克力", "手写信", "钻戒"]

    def extract(self, text: str, risk_types: list[str]) -> UserEvent:
        if "jailbreak" in risk_types or "prompt_leak" in risk_types:
            return UserEvent(type="rule_attack", content=text)

        if "narrative_hijack" in risk_types:
            return UserEvent(type="story_claim", content=text)

        if self._is_gentle_touch(text):
            return UserEvent(type="gentle_touch", content=text)

        gift_event = self._extract_gift(text)
        if gift_event:
            return gift_event

        if re.search(r"(出去玩|约会|看电影|吃饭|旅行|散步)", text):
            place = self._extract_place(text)
            return UserEvent(type="date_invite", place=place, content=text)

        if re.search(r"(可爱|漂亮|聪明|厉害|喜欢你|欣赏你)", text):
            return UserEvent(type="compliment", content=text)

        return UserEvent(type="normal_chat", content=text)

    def _is_gentle_touch(self, text: str) -> bool:
        return bool(re.search(r"(摸摸头|摸头|拍拍头|揉揉头|拍拍肩|抱抱)", text))

    def _extract_gift(self, text: str) -> UserEvent | None:
        if not re.search(r"(送你|给你|递给你|赠送)", text):
            return None

        item = None
        for candidate in self.known_gifts:
            if candidate in text:
                item = candidate
                break

        claimed_amount = None
        amount_match = re.search(r"(\d+)\s*(朵|个|件|枚|封)?", text)
        if amount_match:
            claimed_amount = int(amount_match.group(1))

        return UserEvent(
            type="gift_attempt",
            item=item or "未知礼物",
            claimed_amount=claimed_amount,
            content=text,
        )

    def _extract_place(self, text: str) -> str | None:
        match = re.search(r"(去|到)([^，。！？\s]{1,12})(玩|约会|吃饭|散步|旅行)?", text)
        if match:
            return match.group(2)
        return None
