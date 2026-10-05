#!/usr/bin/env python3
"""Create a local, bounded Project Runtime Console Step 1 demo state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from packages.judge_deepseek.provider import select_provider  # noqa: E402
from packages.judgment_ledger.ledger import JsonlJudgmentLedger  # noqa: E402
from packages.judgment_sidecar.sidecar import judge_in_shadow  # noqa: E402
from packages.runtime_events.codex_transcript import read_tool_outputs  # noqa: E402

SECRET_PATTERNS = (
    re.compile(r"(?i)\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{16,}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*\S+"),
)
SAFE_DEMO_LINE = re.compile(r"^PRC_DEMO_[A-Z0-9_ -]{1,80}$")


def _sanitize(value: Any, limit: int = 600) -> Any:
    if isinstance(value, dict):
        return {str(key): _sanitize(item, limit) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize(item, limit) for item in value[:40]]
    text = str(value)
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if non_empty_lines and all(SAFE_DEMO_LINE.fullmatch(line) for line in non_empty_lines):
        return "\n".join(non_empty_lines)
    if non_empty_lines:
        return f"[REDACTED_TOOL_OUTPUT chars={len(text)}]"
    if len(text) > limit:
        text = text[:limit] + "…"
    return text


def _session_id(events: list[dict[str, Any]]) -> str:
    for event in events:
        if event.get("session_id"):
            return str(event["session_id"])
    return "unknown-session"


def _run_id(session_id: str, transcript: Path) -> str:
    if session_id != "unknown-session":
        return session_id
    digest = hashlib.sha256(str(transcript).encode("utf-8")).hexdigest()[:16]
    return f"codex-run-{digest}"


def build_state(transcript: Path, output_path: Path, max_events: int) -> dict[str, Any]:
    events = read_tool_outputs(transcript)
    if not events:
        raise RuntimeError("No Codex tool-output events were observed.")

    selected = []
    for event in events:
        if event.get("event_id") and event.get("correlation_state") == "CORRELATED":
            normalized = dict(event)
            normalized["tool_output"] = _sanitize(event.get("tool_output"))
            normalized["agent_id"] = event.get("session_id")
            selected.append(normalized)
        if len(selected) >= max_events:
            break
    if not selected:
        raise RuntimeError("Observed outputs did not contain stable event identity.")

    provider, setup_status = select_provider()
    ledger = JsonlJudgmentLedger(output_path.with_suffix(".ledger.jsonl"))
    judgments = []
    for event in selected:
        judgment = judge_in_shadow(
            event,
            provider=provider,
            context={"scope": "Step 1 tool-result shadow judgment"},
        )
        ledger.append(judgment)
        judgments.append(judgment)

    session_id = _session_id(selected)
    run_id = _run_id(session_id, transcript)
    for event in selected:
        event["run_id"] = run_id

    return {
        "schema": "project-runtime-console.step1-demo.v0",
        "generated_at": selected[-1].get("observed_at"),
        "project": {
            "id": "codex-local",
            "name": "Local Codex Runtime",
        },
        "run": {
            "id": run_id,
            "source": "codex.transcript",
            "source_path": str(transcript),
            "status": "OBSERVED",
            "status_semantics": "runtime observation only; not done/blocked",
            "agent_count": 1,
        },
        "agents": [
            {
                "id": session_id,
                "label": "Codex session",
                "role": "session-bound agent",
                "parent_id": None,
                "relation_status": "OBSERVED_SESSION_ONLY",
                "status": "OBSERVED",
            }
        ],
        "events": selected,
        "judgments": judgments,
        "judge_setup": setup_status,
        "shadow_invariant": {
            "mode": "SHADOW",
            "runtime_effect": "NONE",
            "verified_by": "local vertical-slice tests",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "output" / "demo-state.json",
    )
    parser.add_argument("--max-events", type=int, default=5)
    args = parser.parse_args()

    state = build_state(args.transcript.expanduser(), args.output, args.max_events)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(
        {
            "output": str(args.output),
            "ledger": str(args.output.with_suffix(".ledger.jsonl")),
            "events": len(state["events"]),
            "judgments": len(state["judgments"]),
            "judge_setup": state["judge_setup"],
            "run_id": state["run"]["id"],
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
