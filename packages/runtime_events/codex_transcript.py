"""Read-only Codex transcript ingestion for the Step 1 H1 slice."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

CALL_RECORD_TYPES = frozenset({"function_call", "custom_tool_call"})
OUTPUT_RECORD_TYPES = frozenset(
    {"function_call_output", "custom_tool_call_output"}
)


def _string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _event_id(session_id: str | None, call_id: str | None, ordinal: Any) -> str | None:
    if not session_id or not call_id or ordinal is None:
        return None
    identity = json.dumps(
        [session_id, call_id, ordinal],
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"codex-transcript-{hashlib.sha256(identity).hexdigest()[:24]}"


def normalize_tool_output(
    record: dict[str, Any],
    *,
    session_id: str | None,
    turn_id: str | None,
    tool_name: str | None,
    source_path: str,
) -> dict[str, Any] | None:
    """Normalize one observed output record without changing the source."""

    if record.get("type") != "response_item":
        return None
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return None
    record_type = payload.get("type")
    if record_type not in OUTPUT_RECORD_TYPES:
        return None

    call_id = _string(payload.get("call_id"))
    if session_id and call_id:
        correlation_state = "CORRELATED"
    elif session_id or call_id:
        correlation_state = "PARTIAL"
    else:
        correlation_state = "UNKNOWN"

    return {
        "event_id": _event_id(session_id, call_id, record.get("ordinal")),
        "event_type": "tool.output.value",
        "mode": "SHADOW",
        "source": "codex.transcript",
        "source_path": source_path,
        "source_record_type": record_type,
        "source_ordinal": record.get("ordinal"),
        "observed_at": record.get("timestamp"),
        "session_id": session_id,
        "turn_id": turn_id,
        "call_id": call_id,
        "tool_name": tool_name,
        "correlation_key": f"{session_id}:{call_id}" if session_id and call_id else None,
        "correlation_state": correlation_state,
        "tool_output": payload.get("output"),
    }


class TranscriptParser:
    """Parse ordered Codex JSONL records into canonical tool-result events."""

    def __init__(self, source_path: str) -> None:
        self.source_path = source_path
        self.session_id: str | None = None
        self.turn_id: str | None = None
        self._calls: dict[str, str | None] = {}

    def feed_line(self, line: bytes | str) -> dict[str, Any] | None:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        try:
            record = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        if not isinstance(record, dict):
            return None
        return self.feed_record(record)

    def feed_record(self, record: dict[str, Any]) -> dict[str, Any] | None:
        record_type = record.get("type")
        payload = record.get("payload")
        if not isinstance(payload, dict):
            return None
        if record_type == "session_meta":
            self.session_id = _string(payload.get("session_id"))
            return None
        if record_type == "turn_context":
            self.turn_id = _string(payload.get("turn_id"))
            return None
        if record_type != "response_item":
            return None

        payload_type = payload.get("type")
        if payload_type in CALL_RECORD_TYPES:
            call_id = _string(payload.get("call_id"))
            if call_id:
                self._calls[call_id] = _string(payload.get("name"))
            return None
        if payload_type not in OUTPUT_RECORD_TYPES:
            return None

        call_id = _string(payload.get("call_id"))
        return normalize_tool_output(
            record,
            session_id=self.session_id,
            turn_id=self.turn_id,
            tool_name=self._calls.get(call_id) if call_id else None,
            source_path=self.source_path,
        )


def read_tool_outputs(path: str | Path) -> list[dict[str, Any]]:
    """Replay a complete transcript file and return observed tool outputs."""

    transcript_path = Path(path).expanduser()
    parser = TranscriptParser(str(transcript_path))
    events: list[dict[str, Any]] = []
    with transcript_path.open("rb") as stream:
        for line in stream:
            event = parser.feed_line(line)
            if event is not None:
                events.append(event)
    return events

