#!/usr/bin/env python3
"""Read-only probe for the locally installed Codex hook surface.

The probe reads only Codex configuration metadata, CLI help, and optional
installed-binary strings. It does not read auth files or session transcripts,
execute a task, invoke a hook, or write outside its stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 is unsupported.
    tomllib = None  # type: ignore[assignment]


_TARGET_EVENTS = {"posttooluse", "post_tool_use"}
_BINARY_EVENT_TOKENS = (
    "pre_tool_use",
    "post_tool_use",
    "permission_request",
    "pre_compact",
    "post_compact",
    "session_start",
    "session_end",
    "user_prompt_submit",
    "subagent_start",
    "subagent_stop",
    "interrupt",
)
_BINARY_PAYLOAD_TOKENS = (
    "hook_event_name",
    "session_id",
    "turn_id",
    "call_id",
    "tool_call_id",
    "tool_name",
    "tool_input",
    "tool_output",
    "agent_id",
    "thread_id",
)


def _norm(value: str) -> str:
    return value.replace("-", "").replace("_", "").lower()


def _load_config(path: Path) -> dict[str, Any]:
    if tomllib is None:
        return {}
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except (FileNotFoundError, OSError, tomllib.TOMLDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def summarize_hooks(config: Mapping[str, Any]) -> dict[str, Any]:
    hooks = config.get("hooks")
    if not isinstance(hooks, Mapping):
        return {
            "hook_namespace": "UNSUPPORTED",
            "configured_events": [],
            "configured_handler_types": {},
            "target_event_configured": "UNKNOWN",
        }

    configured_events: list[str] = []
    handler_types: dict[str, list[str]] = {}
    for event_name, entries in hooks.items():
        if event_name == "state":
            continue
        configured_events.append(str(event_name))
        types: list[str] = []
        if isinstance(entries, list):
            for entry in entries:
                if not isinstance(entry, Mapping):
                    continue
                nested = entry.get("hooks")
                if not isinstance(nested, list):
                    continue
                for hook in nested:
                    if isinstance(hook, Mapping) and isinstance(hook.get("type"), str):
                        types.append(hook["type"])
        handler_types[str(event_name)] = sorted(set(types))

    target_configured = (
        "OBSERVED"
        if any(_norm(event) in _TARGET_EVENTS for event in configured_events)
        else "UNKNOWN"
    )
    return {
        "hook_namespace": "OBSERVED",
        "configured_events": sorted(configured_events),
        "configured_handler_types": handler_types,
        "target_event_configured": target_configured,
    }


def _run_text(command: list[str], timeout: float = 5.0) -> str:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return completed.stdout


def _codex_metadata() -> dict[str, Any]:
    executable = shutil.which("codex")
    if executable is None:
        return {
            "available": False,
            "version": None,
            "help_mentions_hook_trust": False,
            "binary_event_tokens": [],
            "binary_payload_tokens": [],
        }

    version = _run_text([executable, "--version"]).strip().splitlines()
    help_text = _run_text([executable, "--help"])
    binary_event_tokens: list[str] = []
    binary_payload_tokens: list[str] = []
    binary_path = Path(os.path.realpath(executable))
    strings_path = shutil.which("strings")
    if strings_path and binary_path.is_file():
        binary_text = _run_text([strings_path, str(binary_path)], timeout=10.0).lower()
        for token in _BINARY_EVENT_TOKENS:
            if token in binary_text:
                binary_event_tokens.append(token)
        for token in _BINARY_PAYLOAD_TOKENS:
            if token in binary_text:
                binary_payload_tokens.append(token)

    return {
        "available": True,
        "version": version[0] if version else "UNKNOWN",
        "help_mentions_hook_trust": "--dangerously-bypass-hook-trust" in help_text,
        "binary_event_tokens": sorted(binary_event_tokens),
        "binary_payload_tokens": sorted(binary_payload_tokens),
    }


def probe(config_path: Path | None = None) -> dict[str, Any]:
    codex_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    path = config_path or codex_home / "config.toml"
    config_summary = summarize_hooks(_load_config(path))
    codex = _codex_metadata()
    binary_post_tool_use = "post_tool_use" in codex["binary_event_tokens"]
    hook_route = (
        "OBSERVED"
        if config_summary["hook_namespace"] == "OBSERVED"
        or codex["help_mentions_hook_trust"]
        else "UNSUPPORTED"
    )
    # Capability names are not delivery evidence; coverage stays unknown until
    # one real PostToolUse payload is observed.
    target_coverage = "UNKNOWN"
    return {
        "probe": "h2-hook-first",
        "probe_mode": "READ_ONLY",
        "hook_route": hook_route,
        "target_event": "PostToolUse",
        "target_event_in_binary": "OBSERVED" if binary_post_tool_use else "UNKNOWN",
        "tool_output_value_coverage": target_coverage,
        "configured_hook_surface": config_summary,
        "codex_runtime_metadata": codex,
        "limitations": [
            "No Codex task was started and no hook stdin payload was observed.",
            "No session or transcript file was read.",
            "Binary strings show capability names and candidate fields, not delivery coverage.",
            "A configured PostToolUse hook and its real payload schema remain unproven.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="Codex config.toml to inspect")
    args = parser.parse_args()
    print(json.dumps(probe(args.config), ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
