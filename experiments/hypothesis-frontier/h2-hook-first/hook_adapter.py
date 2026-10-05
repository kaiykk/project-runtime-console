#!/usr/bin/env python3
"""Bounded normalizer for one Codex PostToolUse hook payload.

This module intentionally does not execute hooks, start Codex, or forward data
to a sidecar. It only turns an already-observed hook payload into one canonical
runtime event when stable correlation fields are present.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any


class AdapterBoundaryError(ValueError):
    """A hook payload is outside the evidence-backed adapter boundary."""

    def __init__(self, status: str, reason: str) -> None:
        super().__init__(reason)
        self.status = status
        self.reason = reason


_MISSING = object()
_POST_TOOL_USE_NAMES = {"posttooluse", "post_tool_use"}
_RESULT_KEYS = ("tool_output", "tool_result", "output", "result")


def _string_field(payload: Mapping[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _required_string(
    payload: Mapping[str, Any], field_name: str, *keys: str
) -> str:
    value = _string_field(payload, *keys)
    if value is None:
        raise AdapterBoundaryError(
            "UNKNOWN",
            f"missing stable {field_name}; timestamp-only correlation is unsupported",
        )
    return value


def _result_value(payload: Mapping[str, Any]) -> Any:
    for key in _RESULT_KEYS:
        if key in payload and payload[key] is not None:
            return payload[key]
    raise AdapterBoundaryError(
        "UNSUPPORTED",
        "post-tool-use payload has no non-null tool result field",
    )


def _event_id(session_id: str, turn_id: str, tool_call_id: str) -> str:
    identity = json.dumps(
        ["codex_hook", session_id, turn_id, tool_call_id],
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"codex-hook-{hashlib.sha256(identity).hexdigest()}"


def normalize_post_tool_use(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize one PostToolUse payload without inventing missing identity."""

    if not isinstance(payload, Mapping):
        raise AdapterBoundaryError("UNSUPPORTED", "hook payload must be a JSON object")

    event_name = _string_field(payload, "hook_event_name", "event_name")
    if event_name is None or event_name.replace("-", "").lower() not in _POST_TOOL_USE_NAMES:
        raise AdapterBoundaryError(
            "UNSUPPORTED",
            "payload is not an observed PostToolUse hook event",
        )

    session_id = _required_string(payload, "session_id", "session_id")
    turn_id = _required_string(payload, "turn_id", "turn_id")
    tool_call_id = _required_string(
        payload,
        "tool call identity",
        "tool_call_id",
        "call_id",
    )
    result = _result_value(payload)

    agent_id = _string_field(payload, "agent_id", "thread_id")
    tool_name = _string_field(payload, "tool_name")

    event: dict[str, Any] = {
        "schema_version": "prc.runtime_event.v0",
        "event_id": _event_id(session_id, turn_id, tool_call_id),
        "source": "codex_hook",
        "event_type": "tool.result",
        "correlation_status": "CORRELATED",
        "session_id": session_id,
        "turn_id": turn_id,
        "tool_call_id": tool_call_id,
        "value": result,
        "agent_attribution": "OBSERVED" if agent_id else "UNKNOWN",
    }
    if agent_id is not None:
        event["agent_id"] = agent_id
    if tool_name is not None:
        event["tool_name"] = tool_name
    return event


def normalize_json_text(text: str) -> dict[str, Any]:
    """Parse one JSON payload and normalize it for the CLI probe."""

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise AdapterBoundaryError("UNSUPPORTED", "stdin is not valid JSON") from exc
    return normalize_post_tool_use(payload)


def main() -> int:
    import sys

    try:
        event = normalize_json_text(sys.stdin.read())
    except AdapterBoundaryError as exc:
        print(
            json.dumps(
                {"status": exc.status, "reason": exc.reason},
                ensure_ascii=True,
                sort_keys=True,
            )
        )
        return 2

    print(json.dumps(event, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
