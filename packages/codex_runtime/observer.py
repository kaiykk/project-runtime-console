"""Provider-specific projection from Codex native runtime data to PRC views."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .app_server import CodexAppServerClient

CODEX_THREAD_SOURCE_KINDS = [
    "cli",
    "vscode",
    "exec",
    "appServer",
    "subAgent",
    "subAgentReview",
    "subAgentCompact",
    "subAgentThreadSpawn",
    "subAgentOther",
    "unknown",
]


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _status(value: Any) -> str:
    if isinstance(value, dict):
        return _text(value.get("type")) or "unknown"
    return _text(value) or "unknown"


def _native_thread(thread: dict[str, Any]) -> dict[str, Any]:
    thread_id = _text(thread.get("id")) or "unknown-thread"
    native_session_id = _text(thread.get("sessionId")) or thread_id
    return {
        "runtime_agent_instance_id": thread_id,
        "run_id": native_session_id,
        "native_session_id": native_session_id,
        "parent_runtime_agent_instance_id": _text(thread.get("parentThreadId")),
        "role": _text(thread.get("agentRole")),
        "nickname": _text(thread.get("agentNickname")),
        "status": _status(thread.get("status")),
        "started_at": thread.get("createdAt"),
        "updated_at": thread.get("updatedAt"),
        "cwd": _text(thread.get("cwd")),
        "name": _text(thread.get("name")),
        "preview": _text(thread.get("preview")),
        "source": "codex.app-server",
        "native": {
            "sessionId": thread.get("sessionId"),
            "id": thread.get("id"),
            "parentThreadId": thread.get("parentThreadId"),
            "threadSource": thread.get("threadSource"),
            "model": thread.get("model"),
            "modelProvider": thread.get("modelProvider"),
            "path": thread.get("path"),
        },
    }


def _root_run_id(agent: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> str:
    """Group descendants by the root Thread session without changing identity."""

    current = agent
    seen: set[str] = set()
    while current.get("parent_runtime_agent_instance_id"):
        current_id = current["runtime_agent_instance_id"]
        if current_id in seen:
            break
        seen.add(current_id)
        parent = by_id.get(current["parent_runtime_agent_instance_id"])
        if parent is None:
            break
        current = parent
    return current.get("native_session_id") or current["runtime_agent_instance_id"]


def _assign_run_groups(agents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {agent["runtime_agent_instance_id"]: agent for agent in agents}
    grouped = []
    for agent in agents:
        copy = dict(agent)
        root_run_id = _root_run_id(agent, by_id)
        copy["run_id"] = root_run_id
        if root_run_id != agent.get("native_session_id"):
            copy["run_group_source"] = "root_thread.sessionId via parentThreadId"
        grouped.append(copy)
    return grouped


def _tree_order(agents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {agent["runtime_agent_instance_id"]: agent for agent in agents}

    def depth(agent: dict[str, Any]) -> int:
        current = agent
        seen: set[str] = set()
        result = 0
        while current.get("parent_runtime_agent_instance_id"):
            current_id = current["runtime_agent_instance_id"]
            if current_id in seen:
                break
            seen.add(current_id)
            parent = by_id.get(current["parent_runtime_agent_instance_id"])
            if parent is None:
                break
            result += 1
            current = parent
        return result

    return sorted(agents, key=lambda agent: (depth(agent), -(agent.get("updated_at") or 0)))


def _run_status(agents: list[dict[str, Any]]) -> str:
    statuses = {agent["status"] for agent in agents}
    if "active" in statuses or "running" in statuses or "inProgress" in statuses:
        return "working"
    if statuses and statuses <= {"completed", "idle", "notLoaded"} and "completed" in statuses:
        return "completed"
    if "errored" in statuses or "failed" in statuses:
        return "errored"
    if statuses == {"notLoaded"}:
        return "notLoaded"
    return "unknown"


def _summary(value: Any, limit: int = 500) -> str | None:
    if isinstance(value, str):
        compact = " ".join(value.split())
        return compact[:limit] + ("..." if len(compact) > limit else "")
    if isinstance(value, list):
        parts = [_summary(item, limit) for item in value]
        return " ".join(part for part in parts if part)[:limit] or None
    if isinstance(value, dict):
        for key in ("text", "content", "aggregatedOutput", "output", "command", "name"):
            result = _summary(value.get(key), limit)
            if result:
                return result
    return None


def _content_text(item: dict[str, Any], limit: int = 1000) -> str | None:
    content = item.get("content")
    if not isinstance(content, list):
        return None
    parts: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        text = block.get("text")
        if isinstance(text, str) and text.strip():
            parts.append(text.strip())
    if not parts:
        return None
    compact = "\n".join(parts)
    return compact[:limit] + ("..." if len(compact) > limit else "")


def _native_evidence(item: dict[str, Any]) -> dict[str, Any] | None:
    """Expose bounded native fields for presentation without declaring outcomes."""

    item_type = _text(item.get("type"))
    if item_type == "fileChange":
        changes = item.get("changes")
        files = []
        for change in changes if isinstance(changes, list) else []:
            if not isinstance(change, dict):
                continue
            path = _text(change.get("path"))
            kind = change.get("kind")
            kind_value = _text(kind.get("type")) if isinstance(kind, dict) else _text(kind)
            if path:
                files.append({"path": path, "kind": kind_value})
        return {"kind": "file_change", "files": files, "change_count": len(files)}

    if item_type == "commandExecution":
        return {
            "kind": "command",
            "command": _text(item.get("command")),
            "cwd": _text(item.get("cwd")),
            "status": _status(item.get("status")),
            "exit_code": item.get("exitCode"),
            "duration_ms": item.get("durationMs"),
            "output_summary": _summary(item.get("aggregatedOutput")),
        }

    if item_type == "agentMessage":
        return {"kind": "agent_message", "text": _text(item.get("text"))}

    if item_type == "userMessage":
        return {"kind": "user_message", "text": _content_text(item)}

    if item_type == "collabAgentToolCall":
        receiver_ids = item.get("receiverThreadIds")
        return {
            "kind": "agent_dispatch",
            "tool": _text(item.get("tool")),
            "status": _status(item.get("status")),
            "receiver_thread_ids": receiver_ids if isinstance(receiver_ids, list) else [],
            "prompt": _text(item.get("prompt")),
        }

    return None


def _event(
    thread: dict[str, Any],
    turn: dict[str, Any],
    item: dict[str, Any],
    *,
    turn_index: int | None = None,
) -> dict[str, Any]:
    thread_id = _text(thread.get("id")) or "unknown-thread"
    turn_id = _text(turn.get("id"))
    item_id = _text(item.get("id")) or "unknown-item"
    item_type = _text(item.get("type")) or "unknown"
    call_id = _text(item.get("callId")) or _text(item.get("call_id"))
    event = {
        "observation_id": f"live:{thread_id}:{turn_id or 'unknown-turn'}:{item_id}",
        "canonical_event_id": None,
        "runtime_agent_instance_id": thread_id,
        "run_id": _text(thread.get("sessionId")) or thread_id,
        "turn_id": turn_id,
        "provider_item_id": item_id,
        "call_id": call_id,
        "event_type": item_type,
        "observed_at": item.get("completedAt") or item.get("startedAt") or turn.get("startedAt"),
        "payload_ref": "in-memory native item; not persisted",
        "summary": _content_text(item) or _summary(item),
        "reconciliation": "RECONCILIATION_UNRESOLVED",
        "source": "codex.app-server",
        "turn_status": _status(turn.get("status")),
        "turn_started_at": turn.get("startedAt"),
        "turn_completed_at": turn.get("completedAt"),
        "turn_duration_ms": turn.get("durationMs"),
        "turn_index": turn_index,
    }
    native_evidence = _native_evidence(item)
    if native_evidence is not None:
        event["native_evidence"] = native_evidence
    return event


class CodexRuntimeObserver:
    """Read-only observer over one native app-server connection."""

    def __init__(self, client: CodexAppServerClient | None = None) -> None:
        self.client = client or CodexAppServerClient()
        self._notification_cursor = 0

    def start(self) -> dict[str, Any]:
        info = self.client.start()
        return {
            "source": "codex.app-server",
            "user_agent": info.user_agent,
            "codex_home": info.codex_home,
            "platform_family": info.platform_family,
            "platform_os": info.platform_os,
            "read_only": True,
            "runtime_effect": "NONE",
        }

    def close(self) -> None:
        self.client.close()

    def _ensure_started(self) -> None:
        if not getattr(self.client, "started", False):
            self.client.start()

    def list_threads(self, *, limit: int = 50, cwd: str | None = None) -> list[dict[str, Any]]:
        self._ensure_started()
        params: dict[str, Any] = {
            "limit": max(1, min(limit, 200)),
            "archived": False,
            "sourceKinds": CODEX_THREAD_SOURCE_KINDS,
        }
        if cwd:
            params["cwd"] = cwd
        data: list[Any] = []
        cursor: str | None = None
        for _ in range(10):
            page_params = dict(params)
            if cursor:
                page_params["cursor"] = cursor
            result = self.client.request("thread/list", page_params)
            page = result.get("data", [])
            if isinstance(page, list):
                data.extend(page)
            next_cursor = _text(result.get("nextCursor"))
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor
        by_id: dict[str, dict[str, Any]] = {}
        duplicate_counts: dict[str, int] = defaultdict(int)
        for item in data:
            if not isinstance(item, dict):
                continue
            normalized = _native_thread(item)
            thread_id = normalized["runtime_agent_instance_id"]
            duplicate_counts[thread_id] += 1
            previous = by_id.get(thread_id)
            if previous is None or (normalized.get("updated_at") or 0) >= (previous.get("updated_at") or 0):
                by_id[thread_id] = normalized
        for thread_id, count in duplicate_counts.items():
            if count > 1:
                by_id[thread_id]["identity_warning"] = "DUPLICATE_NATIVE_THREAD_ID_IN_LIST"
                by_id[thread_id]["native"]["duplicate_list_record_count"] = count
        return _assign_run_groups(list(by_id.values()))

    def list_runs(self, *, limit: int = 50, cwd: str | None = None) -> list[dict[str, Any]]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for agent in self.list_threads(limit=limit, cwd=cwd):
            groups[agent["run_id"]].append(agent)
        runs = []
        for run_id, agents in groups.items():
            ordered_agents = _tree_order(agents)
            root = ordered_agents[0]
            runs.append(
                {
                    "run_id": run_id,
                    "project_id": root.get("cwd") or "unknown-project",
                    "status": _run_status(agents),
                    "agent_ids": [agent["runtime_agent_instance_id"] for agent in ordered_agents],
                    "agent_count": len(ordered_agents),
                    "root_agent_id": root["runtime_agent_instance_id"],
                    "updated_at": max((agent.get("updated_at") or 0 for agent in agents), default=None),
                    "source": "codex.app-server.thread/list",
                }
            )
        return sorted(runs, key=lambda run: run.get("updated_at") or 0, reverse=True)

    def read_agent(self, thread_id: str) -> dict[str, Any]:
        self._ensure_started()
        result = self.client.request(
            "thread/read",
            {"threadId": thread_id, "includeTurns": True},
        )
        thread = result.get("thread")
        if not isinstance(thread, dict):
            raise ValueError("thread/read returned no thread")
        agent = _native_thread(thread)
        turns = thread.get("turns", [])
        events: list[dict[str, Any]] = []
        normalized_turns: list[dict[str, Any]] = []
        for turn_index, turn in enumerate(turns if isinstance(turns, list) else []):
            if not isinstance(turn, dict):
                continue
            turn_id = _text(turn.get("id"))
            normalized_turns.append(
                {
                    "turn_id": turn_id,
                    "status": _status(turn.get("status")),
                    "started_at": turn.get("startedAt"),
                    "completed_at": turn.get("completedAt"),
                    "duration_ms": turn.get("durationMs"),
                    "event_count": len(turn.get("items", [])) if isinstance(turn.get("items"), list) else 0,
                }
            )
            for item in turn.get("items", []) if isinstance(turn.get("items"), list) else []:
                if isinstance(item, dict):
                    events.append(_event(thread, turn, item, turn_index=turn_index))
        cursor, notifications = self.client.notifications_since(self._notification_cursor)
        self._notification_cursor = cursor
        return {
            "agent": agent,
            "run": {
                "run_id": agent["run_id"],
                "status": agent["status"],
                "source": "codex.app-server.thread/read",
                "history_available": True,
            },
            "turns": normalized_turns,
            "events": events,
            "notifications": [
                {"method": item.get("method"), "params": item.get("params", {})}
                for item in notifications
                if isinstance(item, dict)
            ],
            "live_notification_count": len(notifications),
            "reconciliation": {
                "status": "RECONCILIATION_UNRESOLVED",
                "reason": "Native item IDs were observed; persisted canonical_event_id relation was not established by this read.",
            },
        }

    def read_run(self, run_id: str, *, limit: int = 20) -> dict[str, Any]:
        all_agents = self.list_threads(limit=max(limit, 200))
        agents = [agent for agent in all_agents if agent["run_id"] == run_id]
        if not agents:
            native_match = next(
                (agent for agent in all_agents if agent.get("native_session_id") == run_id),
                None,
            )
            if native_match:
                run_id = native_match["run_id"]
                agents = [agent for agent in all_agents if agent["run_id"] == run_id]
        if not agents:
            raise KeyError(f"run not found: {run_id}")
        agents = _tree_order(agents)
        selected = agents[0]
        agent_payloads = []
        for agent in agents:
            payload = self.read_agent(agent["runtime_agent_instance_id"])
            payload["agent"]["run_id"] = agent["run_id"]
            payload["agent"]["run_group_source"] = agent.get("run_group_source")
            for event in payload["events"]:
                event["run_id"] = agent["run_id"]
            agent_payloads.append(payload)
        all_events = [event for payload in agent_payloads for event in payload["events"]]
        return {
            "run": {
                "run_id": run_id,
                "project_id": selected.get("cwd") or "unknown-project",
                "status": _run_status(agents),
                "source": "codex.app-server",
                "history_available": all(payload["run"]["history_available"] for payload in agent_payloads),
            },
            "agents": [payload["agent"] for payload in agent_payloads],
            "turns": [turn for payload in agent_payloads for turn in payload["turns"]],
            "events": all_events,
            "notifications": [notification for payload in agent_payloads for notification in payload["notifications"]],
            "live_notification_count": sum(payload["live_notification_count"] for payload in agent_payloads),
            "reconciliation": {
                "status": "RECONCILIATION_UNRESOLVED",
                "unresolved_event_count": sum(
                    event["reconciliation"] == "RECONCILIATION_UNRESOLVED" for event in all_events
                ),
            },
        }
