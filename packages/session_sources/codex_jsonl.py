"""Read-only Codex rollout JSONL adapter with stable source references."""

from __future__ import annotations

import hashlib
import json
import re
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
    events: list[dict[str, Any]] = []
    turns: list[dict[str, Any]] = []
    turn_by_id: dict[str, dict[str, Any]] = {}
    current_turn: str | None = None
    meta: dict[str, Any] = {}
    calls_by_id: dict[str, dict[str, Any]] = {}
    byte_offset = 0
    with path.open("rb") as stream:
        for ordinal, raw_line in enumerate(stream, start=1):
            start = byte_offset
            byte_offset += len(raw_line)
            try:
                record = json.loads(raw_line)
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            payload = record.get("payload") or {}
            record_type = record.get("type")
            if record_type == "session_meta":
                meta = payload
                continue
            if record_type == "turn_context":
                current_turn = payload.get("turn_id") or f"turn-line-{ordinal}"
                turn = {"turn_id": current_turn, "index": len(turns) + 1, "started_at": record.get("timestamp"), "event_ids": []}
                turns.append(turn)
                turn_by_id[current_turn] = turn
                continue
            if record_type == "response_item" and payload.get("type") == "reasoning":
                continue
            kind, event_type = _kind(record)
            if kind in ("other",) and record_type not in ("response_item", "event_msg"):
                continue
            item_id = payload.get("id") or payload.get("item_id")
            stable_key = item_id or payload.get("call_id") or ordinal
            event_id = f"codex:{session_id}:{stable_key}"
            if event_id in {event["event_id"] for event in events}:
                event_id = f"{event_id}:{ordinal}"
            content = _text(record)
            event = {
            "event_id": event_id,
            "ordinal": ordinal,
            "turn_id": current_turn,
            "turn_index": turn_by_id.get(current_turn, {}).get("index") if current_turn else None,
            "timestamp": record.get("timestamp"),
            "kind": kind,
            "event_type": event_type,
            "role": payload.get("role"),
            "tool_name": payload.get("name") or (calls_by_id.get(payload.get("call_id")) or {}).get("tool_name"),
            "call_id": payload.get("call_id"),
            "content": _sanitize(content),
            "native": _sanitize(payload),
            "evidence_ref": {
                "source_type": "codex.rollout_jsonl",
                "session_id": session_id,
                "source_path": str(path),
                "line": ordinal,
                "byte_offset": start,
                "native_item_id": item_id,
            },
        }
            if kind == "tool_call" and payload.get("call_id"):
                calls_by_id[payload["call_id"]] = {"tool_name": payload.get("name")}
            events.append(event)
            if current_turn and current_turn in turn_by_id:
                turn_by_id[current_turn]["event_ids"].append(event_id)
    child_links = [event for event in events if event["kind"] == "agent_event"]
    source_id = meta.get("session_id") or session_id
    agent = {
        "agent_id": None,
        "session_id": source_id,
        "label": "Assistant activity in this Codex Session",
        "identity_status": "SESSION_OBSERVED_AGENT_ID_UNAVAILABLE",
        "parent_agent_id": None,
        "child_agent_count": len(child_links),
        "status": "UNKNOWN",
        "source": meta.get("source") or "unknown",
        "cwd": meta.get("cwd") or "unknown",
        "turn_count": len(turns),
        "event_count": len(events),
        "tool_call_count": sum(event["kind"] == "tool_call" for event in events),
    }
    return {
        "session": {
            "session_id": source_id,
            "source": meta.get("source") or "unknown",
            "cwd": meta.get("cwd") or "unknown",
            "source_path": str(path),
            "file_bytes": path.stat().st_size,
            "line_count": ordinal if 'ordinal' in locals() else 0,
            "turn_count": len(turns),
        },
        "agents": [agent],
        "turns": turns,
        "events": events,
        "summary": {
            "event_count": len(events),
            "tool_call_count": agent["tool_call_count"],
            "tool_result_count": sum(event["kind"] == "tool_result" for event in events),
            "message_count": sum(event["kind"] in ("user", "assistant") for event in events),
            "native_agent_event_count": len(child_links),
            "lineage_status": "OBSERVED" if child_links else "NO_NATIVE_AGENT_LINEAGE_FOUND_IN_SESSION",
        },
    }


def stable_case_ref(node_id: str, case_id: str) -> str:
    return hashlib.sha256(f"{case_id}:{node_id}".encode()).hexdigest()[:20]
