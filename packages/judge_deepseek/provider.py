"""Bounded shadow-judge provider adapters."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
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
    receipt: dict[str, Any] | None = None


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
            receipt={
                "transport": "deterministic",
                "status": "SUCCEEDED",
                "return_code": 0,
            },
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
        started = time.perf_counter()
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
            receipt={
                "transport": "deepseek_http",
                "status": "SUCCEEDED",
                "return_code": 200,
                "duration_ms": round((time.perf_counter() - started) * 1000, 3),
                "stdout_chars": len(content),
                "stderr_chars": 0,
            },
        )


class DshJudgeProvider:
    """Invoke the local DSH headless profile as the DeepSeek entry point."""

    provider = "dsh"
    model = "deepseek-via-dsh"

    def __init__(
        self,
        *,
        executable: str | None = None,
        profile: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        self.executable = executable or os.environ.get("DSH_BIN", "dsh")
        self.profile = profile or os.environ.get("DSH_PROFILE", "headless")
        configured_timeout = os.environ.get("DSH_TIMEOUT_SECONDS", "30")
        self.timeout_seconds = (
            timeout_seconds
            if timeout_seconds is not None
            else float(configured_timeout)
        )
        self.last_receipt: dict[str, Any] | None = None

    @property
    def available(self) -> bool:
        return shutil.which(self.executable) is not None

    def _receipt(
        self,
        *,
        status: str,
        return_code: int | None,
        started: float,
        stdout: str = "",
        stderr: str = "",
    ) -> dict[str, Any]:
        receipt = {
            "transport": "dsh",
            "profile": self.profile,
            "status": status,
            "return_code": return_code,
            "duration_ms": round((time.perf_counter() - started) * 1000, 3),
            "stdout_chars": len(stdout),
            "stderr_chars": len(stderr),
        }
        self.last_receipt = receipt
        return receipt

    @staticmethod
    def _prompt(event: dict[str, Any], context: dict[str, Any]) -> str:
        bounded_input = {
            "decision_point": "tool.output.value",
            "event_type": event.get("event_type"),
            "tool_name": event.get("tool_name"),
            "tool_output": event.get("tool_output"),
            "context": context,
        }
        return (
            "Return JSON only with keys verdict and confidence. "
            "verdict must be one of KEEP, ARCHIVE, DUPLICATE, "
            "IMPORTANT_PROGRESS, UNKNOWN. confidence must be a number from "
            "0 to 1 or null. This is a shadow judgment. Do not use tools, "
            "do not modify files, and do not recommend changing runtime "
            "behavior.\n"
            + json.dumps(bounded_input, ensure_ascii=True, sort_keys=True)
        )

    def judge(self, event: dict[str, Any], context: dict[str, Any]) -> ProviderDecision:
        if not self.available:
            self.last_receipt = {
                "transport": "dsh",
                "profile": self.profile,
                "status": "NOT_FOUND",
                "return_code": None,
                "duration_ms": 0,
                "stdout_chars": 0,
                "stderr_chars": 0,
            }
            raise RuntimeError(f"DSH executable not found: {self.executable}")

        prompt = self._prompt(event, context)
        started = time.perf_counter()
        try:
            completed = subprocess.run(
                [self.executable, "--profile", self.profile, prompt],
                capture_output=True,
                text=True,
                check=False,
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
            self._receipt(
                status="TIMEOUT",
                return_code=None,
                started=started,
                stdout=stdout,
                stderr=stderr,
            )
            raise RuntimeError("DSH request timed out") from exc
        except OSError as exc:
            self._receipt(
                status="EXECUTION_ERROR",
                return_code=None,
                started=started,
                stderr=str(exc),
            )
            raise RuntimeError("DSH request could not start") from exc

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        if completed.returncode != 0:
            self._receipt(
                status="FAILED",
                return_code=completed.returncode,
                started=started,
                stdout=stdout,
                stderr=stderr,
            )
            raise RuntimeError(
                f"DSH request failed with return code {completed.returncode}"
            )

        try:
            decision = json.loads(stdout.strip())
        except json.JSONDecodeError as exc:
            self._receipt(
                status="INVALID_JSON",
                return_code=completed.returncode,
                started=started,
                stdout=stdout,
                stderr=stderr,
            )
            raise RuntimeError("DSH response was not JSON") from exc

        verdict = decision.get("verdict")
        if verdict not in ALLOWED_VERDICTS:
            self._receipt(
                status="UNSUPPORTED_VERDICT",
                return_code=completed.returncode,
                started=started,
                stdout=stdout,
                stderr=stderr,
            )
            raise RuntimeError("DSH returned an unsupported verdict")
        confidence = decision.get("confidence")
        if confidence is not None and not isinstance(confidence, (int, float)):
            confidence = None
        if confidence is not None and not 0 <= float(confidence) <= 1:
            self._receipt(
                status="INVALID_CONFIDENCE",
                return_code=completed.returncode,
                started=started,
                stdout=stdout,
                stderr=stderr,
            )
            raise RuntimeError("DSH returned an invalid confidence")

        receipt = self._receipt(
            status="SUCCEEDED",
            return_code=completed.returncode,
            started=started,
            stdout=stdout,
            stderr=stderr,
        )
        return ProviderDecision(
            verdict=verdict,
            confidence=float(confidence) if confidence is not None else None,
            provider=self.provider,
            model=self.model,
            provider_status="DSH_REAL",
            receipt=receipt,
        )


def select_provider() -> tuple[Any, str]:
    """Select a provider with DSH as the default and no silent fake fallback."""

    mode = os.environ.get("PRC_JUDGE_PROVIDER", "dsh").strip().lower()
    if mode == "dsh":
        provider = DshJudgeProvider()
        return provider, "DSH_READY" if provider.available else "DSH_NOT_FOUND"
    if mode == "deepseek_http":
        provider = DeepSeekJudgeProvider()
        if provider.available:
            return provider, "REAL_DEEPSEEK_HTTP"
        return provider, "DEEPSEEK_HTTP_NOT_CONFIGURED"
    if mode == "fake":
        return FakeJudgeProvider(), "FAKE_EXPLICIT"
    raise ValueError(
        "PRC_JUDGE_PROVIDER must be one of: dsh, deepseek_http, fake"
    )
