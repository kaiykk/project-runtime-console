"""Read-only historical fixture diagnostics; not product acceptance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .codex_jsonl import read_session

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PINNED_CASES = (
    {
        "case_id": "27-agent",
        "label": "27-Agent 真实 Session",
        "session_id": "01a0eca4-7029-7f92-b5a9-2006edb08721",
        "path": str(Path.home() / ".codex/sessions/2026/09/29/rollout-2026-09-29T18-09-54-01a0eca4-7029-7f92-b5a9-2006edb08721.jsonl"),
        "sha256": "ac6f45740d57de5329c48163a2c8faafe0b685677bb264fb3ea6416cbbad9116",
        "expected": {"root_count": 1, "child_count": 26, "edge_count": 26, "pair_count": 26},
        "telemetry": {"world_state": 49, "token_usage_record": 1182, "compacted": 10},
    },
    {
        "case_id": "no-lineage",
        "label": "没有 Agent lineage 的真实 Session",
        "session_id": "019faced-f11a-75e1-ac20-8b95e24d4628",
        "path": str(Path.home() / ".codex/sessions/2026/07/29/rollout-2026-07-29T16-11-42-019faced-f11a-75e1-ac20-8b95e24d4628.jsonl"),
        "sha256": "3431182486fdf498244f2bfbaa4e85916999601cf879398f8bcb81c1c333e3ac",
        "expected": {"root_count": 0, "child_count": 0, "edge_count": 0, "pair_count": 0},
        "telemetry": {"world_state": 3, "token_usage_record": 0, "compacted": 0},
    },
)

BASELINE_FILES = (
    {
        "label": "C v0.2 权威 baseline",
        "path": str(Path.home() / "Downloads/prc_agents_surface_C_v02_interactive.html"),
        "sha256": "be6cd377285683adab19f743e0ae774a9877b482db842c952be49e55d255250d",
    },
    {
        "label": "Work B2 reference",
        "path": str(
            PROJECT_ROOT
            / "PRC_STAGEWISE_CASE_PACK"
            / "PRC_VERTICAL_SLICE_HANDOFF_v1"
            / "mock"
            / "work"
            / "PRC_AISAILING_WORK_B2.html"
        ),
        "sha256": "b32c6fba78e3bb287bba1584879af84cc04b9e61b44f55f39f07f3d6763fe553",
    },
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check(check_id: str, label: str, passed: bool, detail: str, *, severity: str = "hard") -> dict[str, Any]:
    return {
        "check_id": check_id,
        "label": label,
        "status": "PASS" if passed else "FAIL",
        "passed": passed,
        "severity": severity,
        "detail": detail,
    }


def _projection_snapshot(projection: dict[str, Any]) -> dict[str, Any]:
    return {
        "agents": [
            (agent.get("agent_id"), agent.get("parent_agent_id"), agent.get("nickname"))
            for agent in projection.get("agents", [])
        ],
        "edges": [
            (edge.get("parent_agent_id"), edge.get("child_agent_id"), edge.get("nickname"))
            for edge in projection.get("lineage", {}).get("edges", [])
        ],
        "turns": [turn.get("occurrence_id") for turn in projection.get("turns", [])],
        "events": [
            (
                event.get("event_id"),
                event.get("turn_occurrence_id"),
                tuple(
                    (locator.get("line"), locator.get("byte_offset"), locator.get("locator_kind"))
                    for locator in event.get("source_locators", [])
                ),
            )
            for event in projection.get("events", [])
        ],
    }


def _case_result(case: dict[str, Any]) -> dict[str, Any]:
    path = Path(case["path"])
    if not path.exists():
        return {
            "case_id": case["case_id"],
            "label": case["label"],
            "status": "INCONCLUSIVE",
            "available": False,
            "path": str(path),
            "checks": [_check("source-available", "源文件可读取", False, "本机找不到固定的真实 Session 文件")],
            "projection": None,
        }

    before_hash = _sha256(path)
    first = read_session(case["session_id"], path_hint=str(path))
    second = read_session(case["session_id"], path_hint=str(path))
    after_hash = _sha256(path)
    lineage = first.get("lineage", {})
    summary = first.get("summary", {})
    telemetry = first.get("telemetry", {})
    expected = case["expected"]
    pairs = first.get("lineage", {}).get("nickname_pairs", [])
    halley_count = sum(pair[1] == "Halley" for pair in pairs if len(pair) == 2)
    event_ids = [event.get("event_id") for event in first.get("events", [])]
    source_event_ids = [event.get("canonical_occurrence_key") for event in first.get("events", [])]
    unassigned = summary.get("unassigned_event_count", 0)
    ownership_count = len(event_ids) == len(set(event_ids)) and all(
        bool(event.get("turn_occurrence_id")) or event.get("ownership_status") == "UNASSIGNED_SOURCE_BOUNDARY"
        for event in first.get("events", [])
    )
    mirrored = summary.get("mirrored_native_event_count", 0)
    expected_mirrored = summary.get("native_agent_event_count", 0) if case["case_id"] == "27-agent" else 0
    checks = [
        _check("source-hash", "真实源文件的 SHA-256 没有变化", before_hash == case["sha256"] and after_hash == before_hash, f"执行前 {before_hash}；执行后 {after_hash}"),
        _check("root-count", "根 Agent 数量", lineage.get("root_agent_id") is not None if expected["root_count"] else lineage.get("root_agent_id") is None, f"当前结果：{1 if lineage.get('root_agent_id') else 0}；期望：{expected['root_count']}"),
        _check("child-count", "child Agent 数量", lineage.get("child_count") == expected["child_count"], f"当前结果：{lineage.get('child_count', 0)}；期望：{expected['child_count']}"),
        _check("edge-count", "父子关系数量", lineage.get("edge_count") == expected["edge_count"], f"当前结果：{lineage.get('edge_count', 0)}；期望：{expected['edge_count']}"),
        _check("nickname-pairs", "Agent ID + 名字的组合数量", len(pairs) == expected["pair_count"], f"当前结果：{len(pairs)}；期望：{expected['pair_count']}"),
        _check("halley-identity", "两个同名 Halley 仍是两个 Agent", halley_count == (2 if case["case_id"] == "27-agent" else 0), f"Halley 组合数量：{halley_count}"),
        _check("lineage-state", "27-Agent lineage 已观察到" if case["case_id"] == "27-agent" else "没有 lineage 时明确显示没有证据", (lineage.get("status") == "OBSERVED") if case["case_id"] == "27-agent" else (lineage.get("status") == "NO_NATIVE_AGENT_LINEAGE_FOUND_IN_SESSION" and len(first.get("agents", [])) == 0), f"状态：{lineage.get('status')}; native Agent 数量：{len(first.get('agents', []))}"),
        _check("event-ownership", "每条展示事件只归属一个 Turn 或明确未归类", ownership_count, f"展示事件：{len(event_ids)}；未归类：{unassigned}"),
        _check("event-id-determinism", "重复运行得到相同的事件和 Turn ID", _projection_snapshot(first) == _projection_snapshot(second), "同一源文件连续读取两次，投影完全一致"),
        _check("native-mirror-dedup", "同一次 native 派发只显示一次但保留两处证据", mirrored == expected_mirrored, f"带多个 source locator 的 native occurrence：{mirrored}；期望：{expected_mirrored}"),
        _check("telemetry-audit", "后台记账保留在查账区，不混入 Agent 行为", all(telemetry.get(key, 0) == value for key, value in case["telemetry"].items()), f"world_state={telemetry.get('world_state', 0)}，token_usage_record={telemetry.get('token_usage_record', 0)}，compacted={telemetry.get('compacted', 0)}"),
        _check("canonical-ids", "展示事件没有重复的 canonical occurrence", len(source_event_ids) == len(set(source_event_ids)), f"canonical occurrence：{len(source_event_ids)}"),
    ]
    return {
        "case_id": case["case_id"],
        "label": case["label"],
        "status": "PASS" if all(check["passed"] for check in checks) else "FAIL",
        "available": True,
        "path": str(path),
        "session_id": case["session_id"],
        "sha256": after_hash,
        "checks": checks,
        "projection": {
            "lineage": lineage,
            "summary": summary,
            "telemetry": telemetry,
            "turn_count": len(first.get("turns", [])),
            "event_count": len(first.get("events", [])),
            "sample_agents": [
                {"agent_id": agent.get("agent_id"), "nickname": agent.get("nickname"), "parent_agent_id": agent.get("parent_agent_id")}
                for agent in (
                    first.get("agents", [])[:8]
                    + [agent for agent in first.get("agents", []) if agent.get("nickname") == "Halley"]
                )
            ],
            "sample_mirrors": [
                {
                    "event_id": event.get("event_id"),
                    "call_id": event.get("call_id"),
                    "source_locators": event.get("source_locators", []),
                }
                for event in first.get("events", [])
                if len(event.get("source_locators", [])) > 1
            ][:5],
        },
    }


def run_ticket01_acceptance() -> dict[str, Any]:
    cases = [_case_result(case) for case in PINNED_CASES]
    baseline_checks = []
    for baseline in BASELINE_FILES:
        path = Path(baseline["path"])
        if not path.exists():
            baseline_checks.append(_check(f"baseline:{baseline['label']}", f"{baseline['label']} 未被改动", False, "baseline 文件当前不可读取", severity="boundary"))
            continue
        actual = _sha256(path)
        baseline_checks.append(_check(f"baseline:{baseline['label']}", f"{baseline['label']} 未被改动", actual == baseline["sha256"], f"当前 SHA-256：{actual}" , severity="boundary"))

    hard_checks = [check for case in cases for check in case["checks"] if check["severity"] == "hard"]
    if any(case["status"] == "INCONCLUSIVE" for case in cases) or any(check["status"] == "FAIL" and check["severity"] == "boundary" for check in baseline_checks):
        status = "INCONCLUSIVE"
    elif not all(check["passed"] for check in hard_checks + baseline_checks):
        status = "RETURN_TO_REPAIR"
    else:
        status = "DIAGNOSTIC_PASS"
    dsh = {"status": "NOT_REVIEWED", "formal": False,
           "message": "本页不读取历史 DSH 回执，也不代表当前代码已独立复核。"}
    return {
        "standard": "TICKET_01_ACCEPTANCE_STANDARD_20261010",
        "status": status,
        "round_result": "POSITIVE" if status == "DIAGNOSTIC_PASS" else "INCONCLUSIVE" if status == "INCONCLUSIVE" else "REGRESSION",
        "read_only": True,
        "product_acceptance": "NOT_ASSESSED",
        "cases": cases,
        "baseline_checks": baseline_checks,
        "hard_check_count": len(hard_checks),
        "passed_check_count": sum(check["passed"] for check in hard_checks + baseline_checks),
        "total_check_count": len(hard_checks + baseline_checks),
        "next_step": "固定样本机械检查通过；不能据此推进产品阶段" if status == "DIAGNOSTIC_PASS" else "必须先修复或补齐证据",
        "dsh": dsh,
    }
