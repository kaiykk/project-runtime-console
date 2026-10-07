"""Evidence-bounded WorkStage projection for the PRC V2.5 probe."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

TARGET_RUN_ID = "01a0eca4-7029-7f92-b5a9-2006edb08721"

# These anchors are explicit user requests in the selected run. They are not
# a classifier: the projection only turns bounded, manually reviewed anchors
# into navigable labels and keeps the source runtime records attached.
ANCHORS = (
    (0, "恢复 Agent Capability Evolution Lab 上下文", "用户先要求理解交接上下文，并以项目 artifacts 核验状态。"),
    (13, "重新审视 Skill Evolution 目标", "用户要求检查 objective drift，并暂停继续推进 Stage 4。"),
    (15, "切换到 Legal Working Agent", "用户明确暂停前一项目，把后续主题切换为 legal working agent。"),
    (28, "确定 Legal Working Agent 产品 wedge", "用户 ratify 了 multi-session contract negotiation continuity 方向。"),
    (49, "Memory / Context 机制发现", "用户启动了 Memory + Context core mechanism discovery round。"),
    (59, "Phase A reference framing", "用户启动 Legal Agent Harness 的 Phase A reference framing，并随后进入治理 closure。"),
)


def _events_for_agent(events: Iterable[dict[str, Any]], agent_id: str) -> list[dict[str, Any]]:
    return [event for event in events if event.get("runtime_agent_instance_id") == agent_id]


def _safe_event(event: dict[str, Any]) -> dict[str, Any]:
    """Keep native identity and bounded evidence, excluding raw message text."""

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
    }
    native = event.get("native_evidence")
    if isinstance(native, dict):
        result["native_evidence"] = native
    return result


def project_run(run: dict[str, Any]) -> dict[str, Any]:
    """Project one observer result without manufacturing native outcomes."""

    agents = run.get("agents") if isinstance(run.get("agents"), list) else []
    events = run.get("events") if isinstance(run.get("events"), list) else []
    root = next((agent for agent in agents if agent.get("parent_runtime_agent_instance_id") is None), None)
    root_id = (root or {}).get("runtime_agent_instance_id") or TARGET_RUN_ID
    root_user_events = [
        event
        for event in _events_for_agent(events, root_id)
        if event.get("event_type") == "userMessage"
    ]

    stages: dict[str, dict[str, Any]] = {}
    top: list[str] = []
    for index, (anchor_index, title, outcome) in enumerate(ANCHORS, start=1):
        stage_id = f"stage-{index:02d}"
        anchor = root_user_events[anchor_index] if anchor_index < len(root_user_events) else None
        refs = [anchor] if anchor else []
        if anchor:
            same_turn = [
                event
                for event in _events_for_agent(events, root_id)
                if event.get("turn_id") == anchor.get("turn_id")
                and event.get("event_type") in {"agentMessage", "commandExecution", "fileChange"}
            ]
            refs.extend(same_turn[:2])
        safe_refs = [_safe_event(event) for event in refs]
        evidence = [
            {
                "type": "runtime-record",
                "title": "用户请求锚点" if position == 0 else "同一 turn 的 native runtime record",
                "note": "该条记录来自 Codex app-server thread/read；stage 标题和 outcome 是受限 derived summary。",
                "supports": "仅支持用户明确提出或决定的内容；不支持执行成功、因果影响或完整工作边界。",
                "data_class": "NATIVE_FACT",
                "evidence_ref": event.get("observation_id"),
            }
            for position, event in enumerate(safe_refs)
        ]
        stage = {
            "ord": f"{index:02d}",
            "name": title,
            "type": "unknown",
            "kind": "derived workstage label",
            "status": "unknown",
            "outcome": outcome,
            "actions": ["查看该 stage 绑定的 native runtime records"],
            "evidence": evidence,
            "data_class": "DERIVED_SUMMARY",
            "outcome_status": "NOT_ESTABLISHED",
            "source_anchor_ref": anchor.get("observation_id") if anchor else None,
            "raw_events": safe_refs,
        }
        stages[stage_id] = stage
        top.append(stage_id)

    run_meta = run.get("run") if isinstance(run.get("run"), dict) else {}
    return {
        "schema_version": "prc.real-run-workstage.v1",
        "projection": {
            "mode": "bounded-user-anchor-projection",
            "status": "PARTIAL",
            "semantic_policy": "Titles/outcomes are derived only from explicit user-message anchors; unsupported completion and causality remain NOT_ESTABLISHED.",
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
        "subs": {},
        "nodes": stages,
        "raw_events": {
            event.get("observation_id"): _safe_event(event)
            for stage in stages.values()
            for event in stage["raw_events"]
            if event.get("observation_id")
        },
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
