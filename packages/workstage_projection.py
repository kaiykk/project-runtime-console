"""Evidence-grounded trajectory segmentation for the PRC V2.5 view.

This module deliberately does not contain a target-run stage list. It derives
candidate WorkStages from native root user-message windows and attaches child
agent activity to the window where it was observed. Derived labels are
navigational; completion, contribution, causality, and outcomes remain unknown
unless native evidence directly supports them.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime
from typing import Any

TARGET_RUN_ID = "01a0eca4-7029-7f92-b5a9-2006edb08721"
SIGNIFICANT_EVENT_TYPES = frozenset(
    {
        "userMessage",
        "agentMessage",
        "commandExecution",
        "fileChange",
        "collabAgentToolCall",
        "webSearch",
        "mcpToolCall",
    }
)
TRANSITION_RE = re.compile(
    r"(?:切换|换成|改为|改用|暂停|重新|开始新|下一轮|进入下一|reopen|switch|start a new|new round|resume)",
    re.IGNORECASE,
)
NOISE_PREFIXES = (
    "# agents.md instructions",
    "<app-context>",
    "## files pasted by the user",
    "# files pasted by the user",
    "pasted text contains the user's request",
    "# response annotations",
    "you are codex",
)


def _events_for_agent(events: Iterable[dict[str, Any]], agent_id: str) -> list[dict[str, Any]]:
    return [event for event in events if event.get("runtime_agent_instance_id") == agent_id]


def _native_text(event: dict[str, Any]) -> str:
    native = event.get("native_evidence")
    if isinstance(native, dict):
        for key in ("text", "prompt", "command"):
            value = native.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    summary = event.get("summary")
    return summary.strip() if isinstance(summary, str) else ""


def _clean_user_text(text: str) -> str:
    """Remove transport wrappers while preserving the user's actual request."""

    if "## My request:" in text:
        text = text.split("## My request:", 1)[1]
    text = re.sub(r"\n+#+\s*Files pasted by the user:.*?(?=\n## My request:|$)", "", text, flags=re.S | re.I)
    return text.strip()


def _is_substantive_user_event(event: dict[str, Any]) -> bool:
    text = _clean_user_text(_native_text(event))
    if not text:
        return False
    lowered = text.lstrip().lower()
    if lowered.startswith(NOISE_PREFIXES):
        return False
    return len(text) >= 24


def _title_from_text(text: str) -> str:
    text = _clean_user_text(text)
    lines = [re.sub(r"^[-*#>\s]+", "", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line and not line.startswith("```")]
    candidate = next((line for line in lines if len(line) >= 8), "用户请求")
    candidate = re.split(r"[。！？.!?]", candidate, maxsplit=1)[0].strip()
    if len(candidate) > 72:
        candidate = candidate[:69].rstrip() + "..."
    return candidate or "用户请求"


def _timestamp(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _event_time(event: dict[str, Any]) -> float | None:
    return _timestamp(
        event.get("observed_at")
        or event.get("turn_started_at")
        or event.get("turn_completed_at")
    )


def _has_transition(text: str) -> bool:
    return bool(TRANSITION_RE.search(_clean_user_text(text)))


def _safe_event(event: dict[str, Any]) -> dict[str, Any]:
    """Keep native identity and bounded evidence for reversible drill-down."""

    result = {
        "observation_id": event.get("observation_id"),
        "canonical_event_id": event.get("canonical_event_id"),
        "runtime_agent_instance_id": event.get("runtime_agent_instance_id"),
        "run_id": event.get("run_id"),
        "turn_id": event.get("turn_id"),
        "provider_item_id": event.get("provider_item_id"),
        "event_type": event.get("event_type"),
        "observed_at": event.get("observed_at"),
        "reconciliation": event.get("reconciliation"),
        "source": event.get("source"),
        "turn_status": event.get("turn_status"),
        "turn_index": event.get("turn_index"),
    }
    native = event.get("native_evidence")
    if isinstance(native, dict):
        result["native_evidence"] = native
    return result


def _significant(events: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [event for event in events if event.get("event_type") in SIGNIFICANT_EVENT_TYPES]


def _event_label(event: dict[str, Any], *, child_context: bool = False) -> tuple[str, str]:
    event_type = event.get("event_type") or "unknown"
    native = event.get("native_evidence") if isinstance(event.get("native_evidence"), dict) else {}
    if event_type == "userMessage":
        if child_context:
            return "Agent dispatch prompt", "该记录是 parent Agent 发给 child Agent 的 native dispatch prompt，不单独证明 Human 请求。"
        return "用户请求", "该记录保留了用户在此窗口提出的原始请求。"
    if event_type == "commandExecution":
        return "命令执行", f"native command status={native.get('status', 'UNAVAILABLE')} exit_code={native.get('exit_code', 'UNAVAILABLE')}。"
    if event_type == "fileChange":
        return "文件变更", f"native file change count={native.get('change_count', 'UNAVAILABLE')}。"
    if event_type == "collabAgentToolCall":
        return "Agent dispatch", f"native child dispatch status={native.get('status', 'UNAVAILABLE')}。"
    if event_type == "agentMessage":
        return "Agent message", "native agent message record；不单独证明工作结果。"
    return event_type, "native runtime record。"


def _stage_outcome(events: list[dict[str, Any]], child_count: int) -> str:
    counts: defaultdict[str, int] = defaultdict(int)
    for event in events:
        counts[str(event.get("event_type") or "unknown")] += 1
    observed = [
        f"{counts['commandExecution']} command executions",
        f"{counts['fileChange']} file changes",
        f"{counts['agentMessage']} agent messages",
    ]
    if child_count:
        observed.append(f"{child_count} child-agent branches")
    return "Observed " + ", ".join(observed) + "; outcome UNKNOWN / NOT ESTABLISHED."


def _make_evidence(events: list[dict[str, Any]], *, child_context: bool = False) -> list[dict[str, Any]]:
    evidence = []
    for event in events:
        ref = event.get("observation_id")
        if not ref:
            continue
        title, supports = _event_label(event, child_context=child_context)
        evidence.append(
            {
                "type": "runtime-record",
                "title": title,
                "note": "该条目来自 Codex app-server 的 native record，可继续进入 Raw Trace。",
                "supports": supports,
                "data_class": "NATIVE_FACT",
                "evidence_ref": ref,
            }
        )
    return evidence


def _group_anchor_windows(anchors: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    if not anchors:
        return []
    groups: list[list[dict[str, Any]]] = [[anchors[0]]]
    for previous, current in zip(anchors, anchors[1:]):
        previous_time = _event_time(previous)
        current_time = _event_time(current)
        gap = current_time - previous_time if previous_time is not None and current_time is not None else None
        split = _has_transition(_native_text(current)) or (gap is not None and gap > 12 * 60 * 60)
        if split:
            groups.append([current])
        else:
            groups[-1].append(current)
    return groups


def _nearest_stage_index(event: dict[str, Any], stages: list[dict[str, Any]]) -> int:
    when = _event_time(event)
    if when is None:
        return 0
    distances = []
    for index, stage in enumerate(stages):
        start = stage["start_time"]
        end = stage["end_time"]
        if start is not None and end is not None and start <= when <= end:
            return index
        reference = start if start is not None else end
        distances.append((abs(when - reference) if reference is not None else float("inf"), index))
    return min(distances)[1] if distances else 0


def _dispatch_stage_map(root_events: list[dict[str, Any]], stages: list[dict[str, Any]]) -> dict[str, int]:
    """Bind child IDs to the root stage that natively dispatched them."""

    result: dict[str, int] = {}
    for index, stage in enumerate(stages):
        next_start = stages[index + 1]["start_index"] if index + 1 < len(stages) else len(root_events)
        for event in _significant(root_events[stage["start_index"] : next_start]):
            if event.get("event_type") != "collabAgentToolCall":
                continue
            native = event.get("native_evidence")
            receiver_ids = native.get("receiver_thread_ids") if isinstance(native, dict) else None
            for child_id in receiver_ids if isinstance(receiver_ids, list) else []:
                if isinstance(child_id, str):
                    result[child_id] = index
    return result


def project_run(run: dict[str, Any]) -> dict[str, Any]:
    """Project one real run using generic trajectory windows, never target stages."""

    agents = run.get("agents") if isinstance(run.get("agents"), list) else []
    events = run.get("events") if isinstance(run.get("events"), list) else []
    root = next((agent for agent in agents if agent.get("parent_runtime_agent_instance_id") is None), None)
    root_id = (root or {}).get("runtime_agent_instance_id") or TARGET_RUN_ID
    root_events = _events_for_agent(events, root_id)
    anchors = [event for event in root_events if event.get("event_type") == "userMessage" and _is_substantive_user_event(event)]
    anchor_groups = _group_anchor_windows(anchors)

    stages: list[dict[str, Any]] = []
    for group in anchor_groups:
        start = group[0]
        end = group[-1]
        start_index = root_events.index(start)
        end_index = root_events.index(end)
        stages.append(
            {
                "anchors": group,
                "start_index": start_index,
                "end_index": end_index,
                "start_time": _event_time(start),
                "end_time": _event_time(end),
            }
        )
    if not stages:
        stages = [{"anchors": [], "start_index": 0, "end_index": len(root_events), "start_time": None, "end_time": None}]

    dispatch_stage_by_child = _dispatch_stage_map(root_events, stages)
    children_by_stage: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)
    child_events_by_id: dict[str, list[dict[str, Any]]] = {}
    for agent in agents:
        agent_id = agent.get("runtime_agent_instance_id")
        if not agent_id or agent_id == root_id:
            continue
        child_events = _significant(_events_for_agent(events, agent_id))
        child_events_by_id[agent_id] = child_events
        if child_events:
            stage_index = dispatch_stage_by_child.get(agent_id)
            if stage_index is None:
                stage_index = _nearest_stage_index(child_events[0], stages)
            children_by_stage[stage_index].append(agent)

    nodes: dict[str, dict[str, Any]] = {}
    top: list[str] = []
    subs: dict[str, list[str]] = {}

    for stage_index, stage_window in enumerate(stages, start=1):
        start_index = stage_window["start_index"]
        next_start = stages[stage_index]["start_index"] if stage_index < len(stages) else len(root_events)
        root_stage_events = _significant(root_events[start_index:next_start])
        stage_id = f"stage-{stage_index:02d}"
        children = children_by_stage.get(stage_index - 1, [])
        stage_events = list(root_stage_events)
        sub_ids: list[str] = []
        for child_index, agent in enumerate(children, start=1):
            agent_id = agent.get("runtime_agent_instance_id")
            child_events = child_events_by_id.get(agent_id, [])
            if not child_events:
                continue
            child_id = f"{stage_id}-branch-{child_index:02d}"
            child_text = next((_native_text(event) for event in child_events if _native_text(event)), "")
            child_title = _title_from_text(child_text) if child_text else f"Agent branch {child_index:02d}"
            child_evidence_events = child_events[:12]
            nodes[child_id] = {
                "ord": f"{stage_index:02d}.{child_index:02d}",
                "parent": stage_id,
                "name": child_title,
                "type": "unknown",
                "kind": "derived agent branch",
                "status": "unknown",
                "outcome": _stage_outcome(child_events, 0),
                "actions": ["查看该 branch 绑定的 native runtime records"],
                "evidence": _make_evidence(child_evidence_events, child_context=True),
                "data_class": "DERIVED_SUMMARY",
                "outcome_status": "NOT_ESTABLISHED",
                "source_task_refs": [event.get("observation_id") for event in child_evidence_events if event.get("observation_id")],
                "evidence_refs": [event.get("observation_id") for event in child_events if event.get("observation_id")],
                "raw_events": [_safe_event(event) for event in child_events],
                "agent_id": agent_id,
            }
            sub_ids.append(child_id)
            stage_events.extend(child_events)
        if sub_ids:
            subs[stage_id] = sub_ids
        anchor = stage_window["anchors"][0] if stage_window["anchors"] else None
        anchor_text = _native_text(anchor) if anchor else ""
        evidence_events: list[dict[str, Any]] = []
        if anchor:
            evidence_events.append(anchor)
        evidence_events.extend(root_stage_events[:5])
        evidence_events = list(
            {event.get("observation_id"): event for event in evidence_events if event.get("observation_id")}.values()
        )
        title = _title_from_text(anchor_text) if anchor_text else "未解析的 runtime activity"
        nodes[stage_id] = {
            "ord": f"{stage_index:02d}",
            "name": title,
            "type": "parallel" if sub_ids else "unknown",
            "kind": "derived trajectory workstage",
            "status": "unknown",
            "outcome": _stage_outcome(stage_events, len(sub_ids)),
            "actions": ["查看该 WorkStage 绑定的 native runtime records"],
            "evidence": _make_evidence(evidence_events),
            "data_class": "DERIVED_SUMMARY",
            "outcome_status": "NOT_ESTABLISHED",
            "source_anchor_ref": anchor.get("observation_id") if anchor else None,
            "source_task_refs": [event.get("observation_id") for event in stage_window["anchors"] if event.get("observation_id")],
            "evidence_refs": [event.get("observation_id") for event in evidence_events if event.get("observation_id")],
            "raw_events": [_safe_event(event) for event in stage_events],
            "branch_count": len(sub_ids),
        }
        top.append(stage_id)

    run_meta = run.get("run") if isinstance(run.get("run"), dict) else {}
    raw_events: dict[str, dict[str, Any]] = {}
    for node in nodes.values():
        for event in node.get("raw_events", []):
            if event.get("observation_id"):
                raw_events[event["observation_id"]] = event
    return {
        "schema_version": "prc.real-run-workstage.v2",
        "projection": {
            "mode": "evidence-grounded-trajectory-segmentation",
            "status": "PARTIAL",
            "manual_target_stage_enumeration": False,
            "segmentation_policy": "Generic windows from substantive root user-message boundaries and native child-agent activity; no target-run stage list.",
            "semantic_policy": "Titles and observed activity counts are derived from attached native records; completion, causality, contribution, and outcome remain NOT_ESTABLISHED.",
            "native_fact_policy": "Native identity, lineage, event type, timestamp, turn and bounded evidence are retained.",
        },
        "run": {
            "run_id": run_meta.get("run_id") or TARGET_RUN_ID,
            "project_id": run_meta.get("project_id"),
            "status": run_meta.get("status"),
            "source": run_meta.get("source"),
            "history_available": run_meta.get("history_available"),
            "agent_count": len(agents),
            "root_count": sum(1 for agent in agents if not agent.get("parent_runtime_agent_instance_id")),
            "child_count": sum(1 for agent in agents if agent.get("parent_runtime_agent_instance_id")),
            "event_count": len(events),
            "turn_count": len(run.get("turns") or []),
            "reconciliation": run.get("reconciliation"),
        },
        "top": top,
        "subs": subs,
        "nodes": nodes,
        "raw_events": raw_events,
        "agents": [
            {
                "runtime_agent_instance_id": agent.get("runtime_agent_instance_id"),
                "parent_runtime_agent_instance_id": agent.get("parent_runtime_agent_instance_id"),
                "role": agent.get("role"),
                "status": agent.get("status"),
                "native": agent.get("native"),
            }
            for agent in agents
        ],
    }
