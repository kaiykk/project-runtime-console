"""Bounded shadow judgment sidecar logic."""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Any


def _judgment_id(event_id: str, verdict: str, provider: str) -> str:
    identity = json.dumps(
        [event_id, verdict, provider],
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"judgment-{hashlib.sha256(identity).hexdigest()[:24]}"


def judge_in_shadow(
    event: dict[str, Any],
    *,
    provider: Any,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Judge one event and return a ledger-ready SHADOW record."""

    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("shadow judgment requires a canonical event_id")
    bounded_context = context or {}
    started = time.perf_counter()
    try:
        decision = provider.judge(event, bounded_context)
        provider_status = decision.provider_status
        verdict = decision.verdict
        confidence = decision.confidence
        provider_name = decision.provider
        model = decision.model
        provider_receipt = decision.receipt
    except Exception as exc:
        error_prefix = (
            "DSH_ERROR"
            if getattr(provider, "provider", None) == "dsh"
            else "ERROR"
        )
        provider_status = f"{error_prefix}:{type(exc).__name__}"
        verdict = "UNKNOWN"
        confidence = None
        provider_name = getattr(provider, "provider", "unknown")
        model = getattr(provider, "model", "unknown")
        provider_receipt = getattr(provider, "last_receipt", None)

    latency_ms = round((time.perf_counter() - started) * 1000, 3)
    return {
        "judgment_id": _judgment_id(event_id, verdict, provider_name),
        "canonical_event_id": event_id,
        "run_id": event.get("session_id"),
        "agent_id": event.get("agent_id"),
        "decision_point": "tool.output.value",
        "verdict": verdict,
        "confidence": confidence,
        "mode": "SHADOW",
        "judge_provider": provider_name,
        "judge_model": model,
        "provider_status": provider_status,
        "provider_receipt": provider_receipt,
        "latency_ms": latency_ms,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_reference": {
            "source": event.get("source"),
            "source_path": event.get("source_path"),
            "source_ordinal": event.get("source_ordinal"),
        },
    }
