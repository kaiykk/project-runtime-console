"""Small, read-only Codex transcript watcher for the H1 Step 1 spike."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


CALL_RECORD_TYPES = frozenset({"function_call", "custom_tool_call"})
OUTPUT_RECORD_TYPES = frozenset(
    {"function_call_output", "custom_tool_call_output"}
)


def _non_empty_string(value: Any) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


def _stable_event_id(
    session_id: str | None, call_id: str | None, source_ordinal: Any
) -> str | None:
    if not session_id or not call_id or source_ordinal is None:
        return None

    identity = json.dumps(
        {
            "call_id": call_id,
            "session_id": session_id,
            "source_ordinal": source_ordinal,
        },
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
    return f"codex-transcript-{digest}"


def _correlation_state(
    session_id: str | None, call_id: str | None
) -> str:
    if session_id and call_id:
        return "CORRELATED"
    if session_id or call_id:
        return "PARTIAL"
    return "UNKNOWN"


def normalize_tool_output(
    record: dict[str, Any],
    *,
    session_id: str | None = None,
    turn_id: str | None = None,
    tool_name: str | None = None,
) -> dict[str, Any] | None:
    """Normalize one transcript output record without changing the source."""

    if record.get("type") != "response_item":
        return None

    payload = record.get("payload")
    if not isinstance(payload, dict):
        return None

    source_record_type = payload.get("type")
    if source_record_type not in OUTPUT_RECORD_TYPES:
        return None

    normalized_session_id = _non_empty_string(session_id)
    normalized_turn_id = _non_empty_string(turn_id)
    call_id = _non_empty_string(payload.get("call_id"))
    normalized_tool_name = _non_empty_string(tool_name)
    correlation_state = _correlation_state(normalized_session_id, call_id)

    return {
        "event_id": _stable_event_id(
            normalized_session_id, call_id, record.get("ordinal")
        ),
        "event_type": "tool.output.value",
        "mode": "SHADOW",
        "source": "codex.transcript",
        "source_record_type": source_record_type,
        "source_ordinal": record.get("ordinal"),
        "observed_at": record.get("timestamp"),
        "session_id": normalized_session_id,
        "turn_id": normalized_turn_id,
        "call_id": call_id,
        "tool_name": normalized_tool_name,
        "correlation_key": (
            f"{normalized_session_id}:{call_id}"
            if normalized_session_id and call_id
            else None
        ),
        "correlation_state": correlation_state,
        "tool_output": payload.get("output"),
    }


class TranscriptParser:
    """Stateful parser for the ordered JSONL transcript record stream."""

    def __init__(self) -> None:
        self.session_id: str | None = None
        self.turn_id: str | None = None
        self._calls: dict[str, str | None] = {}

    def feed_line(self, line: bytes | str) -> dict[str, Any] | None:
        if isinstance(line, bytes):
            line = line.decode("utf-8")

        try:
            record = json.loads(line)
        except (TypeError, UnicodeDecodeError, json.JSONDecodeError):
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
            self.session_id = _non_empty_string(payload.get("session_id"))
            return None

        if record_type == "turn_context":
            self.turn_id = _non_empty_string(payload.get("turn_id"))
            return None

        if record_type != "response_item":
            return None

        payload_type = payload.get("type")
        if payload_type in CALL_RECORD_TYPES:
            call_id = _non_empty_string(payload.get("call_id"))
            if call_id:
                self._calls[call_id] = _non_empty_string(payload.get("name"))
            return None

        if payload_type not in OUTPUT_RECORD_TYPES:
            return None

        call_id = _non_empty_string(payload.get("call_id"))
        return normalize_tool_output(
            record,
            session_id=self.session_id,
            turn_id=self.turn_id,
            tool_name=self._calls.get(call_id) if call_id else None,
        )


class TranscriptWatcher:
    """Poll a transcript for newly appended, complete JSONL records."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.parser = TranscriptParser()
        self._read_offset = 0
        self._pending = b""

    def poll(self) -> list[dict[str, Any]]:
        """Return newly observed tool outputs; incomplete final lines are held."""

        with self.path.open("rb") as stream:
            stream.seek(self._read_offset)
            chunk = stream.read()

        if not chunk:
            return []

        self._read_offset += len(chunk)
        data = self._pending + chunk
        lines = data.splitlines(keepends=True)
        complete_line_count = len(lines)

        if lines and not lines[-1].endswith((b"\n", b"\r")):
            complete_line_count -= 1

        events: list[dict[str, Any]] = []
        consumed = 0
        for line in lines[:complete_line_count]:
            consumed += len(line)
            event = self.parser.feed_line(line)
            if event is not None:
                events.append(event)

        self._pending = data[consumed:]
        return events
