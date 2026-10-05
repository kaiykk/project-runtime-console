#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


adapter = load_module("h2_hook_adapter", "hook_adapter.py")
probe = load_module("h2_hook_probe", "probe_hook_surface.py")


class HookAdapterTests(unittest.TestCase):
    def test_normalizes_post_tool_use_with_stable_identity(self) -> None:
        payload = {
            "hook_event_name": "PostToolUse",
            "session_id": "session-1",
            "turn_id": "turn-2",
            "tool_call_id": "call-3",
            "agent_id": "agent-main",
            "tool_name": "shell",
            "tool_output": {"stdout": "bounded"},
            "timestamp": "ignored-for-identity",
        }

        first = adapter.normalize_post_tool_use(payload)
        second = adapter.normalize_post_tool_use(payload)

        self.assertEqual(first, second)
        self.assertEqual(first["event_type"], "tool.result")
        self.assertEqual(first["correlation_status"], "CORRELATED")
        self.assertEqual(first["tool_call_id"], "call-3")
        self.assertEqual(first["value"], {"stdout": "bounded"})
        self.assertNotIn("timestamp", first)
        self.assertTrue(first["event_id"].startswith("codex-hook-"))

    def test_rejects_timestamp_only_correlation(self) -> None:
        payload = {
            "hook_event_name": "PostToolUse",
            "session_id": "session-1",
            "turn_id": "turn-2",
            "tool_output": "bounded",
            "timestamp": "only-time",
        }

        with self.assertRaisesRegex(ValueError, "timestamp-only"):
            adapter.normalize_post_tool_use(payload)

    def test_rejects_non_post_tool_use_event(self) -> None:
        payload = {
            "hook_event_name": "Interrupt",
            "session_id": "session-1",
            "turn_id": "turn-2",
            "tool_call_id": "call-3",
            "tool_output": "bounded",
        }

        with self.assertRaisesRegex(ValueError, "not an observed PostToolUse"):
            adapter.normalize_post_tool_use(payload)


class HookProbeTests(unittest.TestCase):
    def test_summarizes_only_hook_metadata(self) -> None:
        summary = probe.summarize_hooks(
            {
                "hooks": {
                    "Interrupt": [
                        {
                            "hooks": [
                                {"type": "command", "command": "not returned"}
                            ]
                        }
                    ],
                    "state": {"private": {"trusted_hash": "not returned"}},
                }
            }
        )

        self.assertEqual(summary["hook_namespace"], "OBSERVED")
        self.assertEqual(summary["configured_events"], ["Interrupt"])
        self.assertEqual(summary["configured_handler_types"], {"Interrupt": ["command"]})
        self.assertEqual(summary["target_event_configured"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
