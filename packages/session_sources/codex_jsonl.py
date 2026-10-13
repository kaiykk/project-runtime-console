"""Read-only Codex rollout JSONL adapter with stable source references."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

SESSION_ROOTS = (
    Path.home() / ".codex" / "sessions",
    Path.home() / ".codex" / "archived_sessions",
)
SENSITIVE = re.compile(
    r"(?i)(\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret|authorization)\b\s*[:=]\s*)([^\s,;\"']+)"
)
BEARER = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")
OPENAI_KEY = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")


def _sanitize(value: Any) -> Any:
    if isinstance(value, str):
        value = SENSITIVE.sub(r"\1[REDACTED]", value)
        value = BEARER.sub("Bearer [REDACTED]", value)
        value = OPENAI_KEY.sub("[REDACTED_KEY]", value)
        return value
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    if isinstance(value, dict):
        return {key: _sanitize(item) for key, item in value.items()}
    return value


def _text(record: dict[str, Any]) -> str:
    payload = record.get("payload") or {}
    if not isinstance(payload, dict):
        return ""
    if payload.get("type") == "message":
        content = payload.get("content")
        if isinstance(content, list):
            return "\n".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and isinstance(block.get("text"), str)
            )
        return content if isinstance(content, str) else ""
    for key in ("text", "command", "output", "prompt", "name"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return ""


def _session_meta(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("rb") as stream:
            first = json.loads(stream.readline())
        if first.get("type") != "session_meta":
            return None
        payload = first.get("payload") or {}
        session_id = payload.get("session_id") or payload.get("id")
        if not session_id:
            return None
        title = ""
        with path.open("rb") as stream:
            for _ in range(80):
                line = stream.readline()
                if not line:
                    break
                try:
                    record = json.loads(line)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
                item = record.get("payload") or {}
                if record.get("type") == "response_item" and item.get("type") == "message" and item.get("role") == "user":
                    title = " ".join(_text(record).split())[:140]
                    if title and "environment_context" not in title:
                        break
        return {
            "session_id": session_id,
            "source": payload.get("source") or "unknown",
            "cwd": payload.get("cwd") or "unknown",
            "path": str(path),
            "title": title or "未命名本地 Session",
            "modified_at": path.stat().st_mtime,
            "bytes": path.stat().st_size,
        }
    except (OSError, ValueError, TypeError):
        return None


def list_sessions(project: str | None = None) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for root in SESSION_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.jsonl"):
            item = _session_meta(path)
            if item and (not project or project.casefold() in item["cwd"].casefold()):
                found.append(item)
    return sorted(found, key=lambda item: item["modified_at"], reverse=True)


def _kind(record: dict[str, Any]) -> tuple[str, str]:
    payload = record.get("payload") or {}
    record_type = record.get("type") or "unknown"
    item_type = payload.get("type") or ""
    role = payload.get("role") or ""
    if record_type == "turn_context":
        return "turn", "runtime.turn"
    if record_type == "event_msg":
        return "runtime", f"runtime.{payload.get('type', 'event')}"
    if record_type == "response_item" and item_type == "message":
        return ("user" if role == "user" else "assistant"), f"message.{role or 'unknown'}"
    if record_type == "response_item" and item_type in ("function_call", "custom_tool_call"):
        return "tool_call", f"tool.call.{payload.get('name', item_type)}"
    if record_type == "response_item" and item_type in ("function_call_output", "custom_tool_call_output"):
        return "tool_result", "tool.result"
    if record_type == "response_item" and item_type in ("collabAgentToolCall", "agentSpawn", "threadSpawn"):
        return "agent_event", f"agent.{item_type}"
    return "other", f"native.{item_type or record_type}"


def _nested_native_item(record: dict[str, Any]) -> dict[str, Any] | None:
    payload = record.get("payload") or {}
    item = payload.get("item") if isinstance(payload, dict) else None
    if isinstance(item, dict) and item.get("type") == "CollabAgentToolCall":
        return item
    if isinstance(payload, dict) and payload.get("type") == "CollabAgentToolCall":
        return payload
    return None


def _locator(
    *,
    session_id: str,
    source_path: Path,
    ordinal: int,
    byte_offset: int,
    native_item_id: str | None = None,
    locator_kind: str = "record",
) -> dict[str, Any]:
    return {
        "source_type": "codex.rollout_jsonl",
        "session_id": session_id,
        "source_path": str(source_path),
        "line": ordinal,
        "byte_offset": byte_offset,
        "native_item_id": native_item_id,
        "locator_kind": locator_kind,
    }


def _stable_id(session_id: str, canonical_key: str) -> str:
    digest = hashlib.sha256(f"{session_id}:{canonical_key}".encode()).hexdigest()[:24]
    return f"codex:{session_id}:occurrence:{digest}"


def read_session(session_id: str, *, path_hint: str | None = None) -> dict[str, Any]:
    candidates = []
    if path_hint:
        hinted = Path(path_hint).expanduser().resolve()
        roots = [root.resolve() for root in SESSION_ROOTS if root.exists()]
        if not any(hinted.is_relative_to(root) for root in roots):
            raise PermissionError("Session path is outside the local Codex session roots")
        candidates = [hinted] if hinted.is_file() else []
    else:
        candidates = [Path(item["path"]) for item in list_sessions() if item["session_id"] == session_id]
    if not candidates:
        raise FileNotFoundError(f"local session not found: {session_id}")
    path = candidates[0]
    records: list[tuple[int, int, dict[str, Any]]] = []
    malformed_count = 0
    meta: dict[str, Any] = {}
    byte_offset = 0
    with path.open("rb") as stream:
        for ordinal, raw_line in enumerate(stream, start=1):
            start = byte_offset
            byte_offset += len(raw_line)
            try:
                record = json.loads(raw_line)
            except (UnicodeDecodeError, json.JSONDecodeError):
                malformed_count += 1
                continue
            if record.get("type") == "session_meta":
                meta = record.get("payload") or {}
            records.append((ordinal, start, record))

    source_id = meta.get("session_id") or session_id
    native_call_ids: set[str] = set()
    response_locators: dict[str, list[dict[str, Any]]] = {}
    for ordinal, start, record in records:
        payload = record.get("payload") or {}
        nested = _nested_native_item(record)
        if nested and nested.get("id"):
            native_call_ids.add(str(nested["id"]))
        if record.get("type") == "response_item" and payload.get("type") in ("function_call", "custom_tool_call"):
            call_id = payload.get("call_id")
            if call_id:
                response_locators.setdefault(str(call_id), []).append(
                    _locator(
                        session_id=source_id,
                        source_path=path,
                        ordinal=ordinal,
                        byte_offset=start,
                        native_item_id=str(call_id),
                        locator_kind="response_item",
                    )
                )

    turns: list[dict[str, Any]] = []
    turn_occurrences: dict[int, dict[str, Any] | None] = {}
    turn_counts: Counter[str] = Counter()
    current_turn: dict[str, Any] | None = None
    for ordinal, _start, record in records:
        if record.get("type") == "turn_context":
            payload = record.get("payload") or {}
            turn_id = str(payload.get("turn_id") or f"turn-line-{ordinal}")
            turn_counts[turn_id] += 1
            occurrence = turn_counts[turn_id]
            current_turn = {
                "turn_id": turn_id,
                "occurrence_ordinal": occurrence,
                "occurrence_id": f"turn:{source_id}:{turn_id}:{occurrence}",
                "index": len(turns) + 1,
                "started_at": record.get("timestamp"),
                "event_ids": [],
            }
            turns.append(current_turn)
        turn_occurrences[ordinal] = current_turn

    events: list[dict[str, Any]] = []
    events_by_key: dict[str, dict[str, Any]] = {}
    occurrence_counts: Counter[str] = Counter()
    telemetry_counts: Counter[str] = Counter()
    raw_record_count = 0
    for ordinal, start, record in records:
        record_type = record.get("type")
        payload = record.get("payload") or {}
        if record_type in ("session_meta", "turn_context"):
            continue
        if record_type == "response_item" and payload.get("type") == "reasoning":
            continue
        if record_type in ("world_state", "token_usage_record", "compacted"):
            telemetry_counts[record_type] += 1
            continue

        raw_record_count += 1
        turn = turn_occurrences.get(ordinal)
        nested = _nested_native_item(record)
        if nested:
            native_id = str(nested.get("id") or payload.get("call_id") or f"line-{ordinal}")
            base_key = f"native:{nested.get('type')}:{native_id}"
            occurrence_counts[base_key] += 1
            occurrence_ordinal = occurrence_counts[base_key]
            canonical_key = f"{base_key}:{occurrence_ordinal}"
            aliases = list(response_locators.get(native_id, []))
            aliases.append(
                _locator(
                    session_id=source_id,
                    source_path=path,
                    ordinal=ordinal,
                    byte_offset=start,
                    native_item_id=native_id,
                    locator_kind="nested_native_item",
                )
            )
            content = nested.get("prompt") or nested.get("tool") or nested.get("status") or ""
            event = {
                "event_id": _stable_id(source_id, canonical_key),
                "occurrence_id": canonical_key,
                "canonical_occurrence_key": canonical_key,
                "occurrence_ordinal": occurrence_ordinal,
                "ordinal": ordinal,
                "turn_id": turn.get("turn_id") if turn else None,
                "turn_occurrence_id": turn.get("occurrence_id") if turn else None,
                "ownership_status": "ASSIGNED" if turn else "UNASSIGNED_SOURCE_BOUNDARY",
                "turn_index": turn.get("index") if turn else None,
                "timestamp": record.get("timestamp"),
                "kind": "agent_event",
                "event_type": "agent.CollabAgentToolCall",
                "role": None,
                "tool_name": nested.get("tool"),
                "call_id": native_id,
                "content": _sanitize(content),
                "native": _sanitize(nested),
                "evidence_ref": aliases[-1],
                "source_locators": aliases,
            }
        else:
            call_id = payload.get("call_id")
            if (record_type == "response_item"
                    and payload.get("type") in ("function_call", "custom_tool_call")
                    and call_id and str(call_id) in native_call_ids):
                # The response_item is an alias of the nested native dispatch.
                continue
            kind, event_type = _kind(record)
            if kind == "other" and record_type not in ("response_item", "event_msg"):
                continue
            item_id = payload.get("id") or payload.get("item_id")
            base_key = f"record:{record_type}:{payload.get('type') or ''}:{item_id or call_id or ordinal}"
            occurrence_counts[base_key] += 1
            occurrence_ordinal = occurrence_counts[base_key]
            canonical_key = f"{base_key}:{occurrence_ordinal}"
            locator = _locator(
                session_id=source_id,
                source_path=path,
                ordinal=ordinal,
                byte_offset=start,
                native_item_id=str(item_id or call_id) if (item_id or call_id) else None,
            )
            event = {
                "event_id": _stable_id(source_id, canonical_key),
                "occurrence_id": canonical_key,
                "canonical_occurrence_key": canonical_key,
                "occurrence_ordinal": occurrence_ordinal,
                "ordinal": ordinal,
                "turn_id": turn.get("turn_id") if turn else None,
                "turn_occurrence_id": turn.get("occurrence_id") if turn else None,
                "ownership_status": "ASSIGNED" if turn else "UNASSIGNED_SOURCE_BOUNDARY",
                "turn_index": turn.get("index") if turn else None,
                "timestamp": record.get("timestamp"),
                "kind": kind,
                "event_type": event_type,
                "role": payload.get("role"),
                "tool_name": payload.get("name"),
                "call_id": call_id,
                "content": _sanitize(_text(record)),
                "native": _sanitize(payload),
                "evidence_ref": locator,
                "source_locators": [locator],
            }

        events_by_key[canonical_key] = event
        events.append(event)
        if turn is not None:
            turn["event_ids"].append(event["event_id"])

    native_events = [event for event in events if event["kind"] == "agent_event"]
    children: dict[str, dict[str, Any]] = {}
    edges: dict[tuple[str, str], dict[str, Any]] = {}
    for event in native_events:
        native = event.get("native") or {}
        # Only explicit spawn evidence establishes lineage. Communication recipients
        # on wait/send_input remain events, not newly inferred children.
        parent_id = native.get("sender_thread_id")
        if native.get("tool") != "spawn_agent" or not parent_id:
            continue
        receiver_agents = native.get("receiver_agents") or []
        for receiver in receiver_agents:
            if not isinstance(receiver, dict) or not receiver.get("thread_id"):
                continue
            child_id = str(receiver["thread_id"])
            nickname = str(receiver.get("agent_nickname") or "UNKNOWN")
            children.setdefault(
                child_id,
                {
                    "agent_id": child_id,
                    "session_id": source_id,
                    "label": nickname,
                    "nickname": nickname,
                    "identity_status": "NATIVE_CHILD_IDENTITY_OBSERVED",
                    "parent_agent_id": parent_id,
                    "status": native.get("status") or "UNKNOWN",
                    "source": meta.get("source") or "unknown",
                    "cwd": meta.get("cwd") or "unknown",
                    "turn_count": 0,
                    "event_count": 0,
                    "tool_call_count": 0,
                    "source_locators": [],
                },
            )
            children[child_id]["source_locators"].append(event["evidence_ref"])
            edge_key = (str(parent_id), child_id)
            edges.setdefault(
                edge_key,
                {
                    "parent_agent_id": edge_key[0],
                    "child_agent_id": child_id,
                    "nickname": nickname,
                    "source_locators": [],
                },
            )["source_locators"].append(event["evidence_ref"])

    if children:
        root = {
            "agent_id": source_id,
            "session_id": source_id,
            "label": "Root Session Agent",
            "nickname": None,
            "identity_status": "NATIVE_ROOT_SESSION_IDENTITY_OBSERVED",
            "parent_agent_id": None,
            "child_agent_count": len(children),
            "status": "OBSERVED",
            "source": meta.get("source") or "unknown",
            "cwd": meta.get("cwd") or "unknown",
            "turn_count": len(turns),
            "event_count": len(events),
            "tool_call_count": sum(event["kind"] == "tool_call" for event in events),
        }
        agents = [root, *sorted(children.values(), key=lambda item: item["agent_id"])]
        lineage_status = "OBSERVED"
    else:
        # A Session identity is still available, but it is not promoted to an Agent card.
        agents = []
        lineage_status = "NO_NATIVE_AGENT_LINEAGE_FOUND_IN_SESSION"

    session = {
        "session_id": source_id,
        "source": meta.get("source") or "unknown",
        "cwd": meta.get("cwd") or "unknown",
        "source_path": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "file_bytes": path.stat().st_size,
        "line_count": len(records) + malformed_count,
        "turn_count": len(turns),
    }
    return {
        "session": session,
        "agents": agents,
        "lineage": {
            "status": lineage_status,
            "root_agent_id": source_id if children else None,
            "child_count": len(children),
            "edge_count": len(edges),
            "edges": list(edges.values()),
            "nickname_pairs": sorted(
                [[child["agent_id"], child["nickname"]] for child in children.values()],
                key=lambda pair: pair[0],
            ),
        },
        "turns": turns,
        "events": events,
        "telemetry": {
            "world_state": telemetry_counts["world_state"],
            "token_usage_record": telemetry_counts["token_usage_record"],
            "compacted": telemetry_counts["compacted"],
            "malformed_jsonl": malformed_count,
        },
        "summary": {
            "event_count": len(events),
            "canonical_event_count": len(events),
            "raw_record_count": raw_record_count,
            "tool_call_count": sum(event["kind"] == "tool_call" for event in events),
            "tool_result_count": sum(event["kind"] == "tool_result" for event in events),
            "message_count": sum(event["kind"] in ("user", "assistant") for event in events),
            "native_agent_event_count": len(native_events),
            "native_child_count": len(children),
            "native_edge_count": len(edges),
            "lineage_status": lineage_status,
            "unassigned_event_count": sum(not event.get("turn_occurrence_id") for event in events),
            "unassigned_event_ids": [event["event_id"] for event in events if event.get("ownership_status") == "UNASSIGNED_SOURCE_BOUNDARY"],
            "mirrored_native_event_count": sum(len(event.get("source_locators", [])) > 1 for event in native_events),
        },
    }


def stable_case_ref(node_id: str, case_id: str) -> str:
    return hashlib.sha256(f"{case_id}:{node_id}".encode()).hexdigest()[:20]
