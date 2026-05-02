from __future__ import annotations

import json
from typing import Any

from .engine import GuardEngine, GuardResult
from .state import CharacterState


def build_openai_messages(
    system_guard_prompt: str,
    reply_contract_prompt: str,
    guard_result: GuardResult,
) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system_guard_prompt},
        {"role": "system", "content": reply_contract_prompt},
        {
            "role": "user",
            "content": json.dumps(
                guard_result.safe_context,
                ensure_ascii=False,
                indent=2,
            ),
        },
    ]


def process_chat_payload(
    payload: dict[str, Any],
    engine: GuardEngine,
    state: CharacterState | dict[str, Any],
    input_key: str = "message",
) -> dict[str, Any]:
    user_input = str(payload.get(input_key, ""))
    result = engine.process_user_input(user_input=user_input, state=state)
    return result.to_dict()


def safe_commit_state(
    old_state: CharacterState,
    result: GuardResult,
    model_reply: str,
    engine: GuardEngine,
) -> tuple[CharacterState, str, bool]:
    valid, _blocked_patterns = engine.validate_model_output(model_reply)
    if not valid:
        return old_state, engine.fallback_reply(result.risk), False
    return result.next_state, model_reply, True
