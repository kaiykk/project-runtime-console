"""DeepSeek and deterministic fake provider adapters for shadow judgments."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

ALLOWED_VERDICTS = frozenset(
    {"KEEP", "ARCHIVE", "DUPLICATE", "IMPORTANT_PROGRESS", "UNKNOWN"}
)


@dataclass(frozen=True)
class ProviderDecision:
    verdict: str
    confidence: float | None
    provider: str
    model: str
    provider_status: str


class FakeJudgeProvider:
    """Deterministic provider used when no external API key is available."""

    provider = "fake"
    model = "step1-deterministic"

    def judge(self, event: dict[str, Any], context: dict[str, Any]) -> ProviderDecision:
        text = str(event.get("tool_output", "")).lower()
        if any(token in text for token in ("error", "failed", "exception")):
            verdict = "UNKNOWN"
        elif any(token in text for token in ("created", "updated", "passed", "success")):
            verdict = "IMPORTANT_PROGRESS"
        else:
            verdict = "KEEP"
        return ProviderDecision(
            verdict=verdict,
            confidence=0.5,
            provider=self.provider,
            model=self.model,
            provider_status="FAKE_PROVIDER",
        )


class DeepSeekJudgeProvider:
    """Minimal JSON-over-HTTP DeepSeek adapter with no SDK dependency."""

    provider = "deepseek"

    def __init__(self) -> None:
        self.api_key = os.environ.get("DEEPSEEK_API_KEY")
        self.model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
        self.base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def judge(self, event: dict[str, Any], context: dict[str, Any]) -> ProviderDecision:
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY is not configured")

        bounded_input = {
            "decision_point": "tool.output.value",
            "event_type": event.get("event_type"),
            "tool_name": event.get("tool_name"),
            "tool_output": event.get("tool_output"),
            "context": context,
        }
        prompt = (
            "Return JSON only with keys verdict and confidence. "
            "verdict must be one of KEEP, ARCHIVE, DUPLICATE, "
            "IMPORTANT_PROGRESS, UNKNOWN. This is a shadow judgment and "
            "must not recommend changing runtime behavior.\n"
            + json.dumps(bounded_input, ensure_ascii=True, sort_keys=True)
        )
        request_body = json.dumps(
            {
                "model": self.model,
                "temperature": 0,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a bounded shadow judge.",
                    },
                    {"role": "user", "content": prompt},
                ],
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=request_body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"DeepSeek request failed: {type(exc).__name__}") from exc

        content = (
            payload.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )
        try:
            decision = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError("DeepSeek response was not JSON") from exc

        verdict = decision.get("verdict")
        if verdict not in ALLOWED_VERDICTS:
            raise RuntimeError("DeepSeek returned an unsupported verdict")
        confidence = decision.get("confidence")
        if confidence is not None and not isinstance(confidence, (int, float)):
            confidence = None
        return ProviderDecision(
            verdict=verdict,
            confidence=float(confidence) if confidence is not None else None,
            provider=self.provider,
            model=self.model,
            provider_status="REAL_API",
        )


def select_provider() -> tuple[Any, str]:
    provider = DeepSeekJudgeProvider()
    if provider.available:
        return provider, "REAL_DEEPSEEK"
    return FakeJudgeProvider(), "HUMAN_SETUP_REQUIRED"

