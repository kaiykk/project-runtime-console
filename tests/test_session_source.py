import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from packages.session_sources import codex_jsonl
from packages.session_sources.codex_jsonl import read_session


class CodexJsonlAdapterTest(unittest.TestCase):
    def test_preserves_turns_and_excludes_reasoning_from_presented_events(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rollout-test.jsonl"
            records = [
                {"type": "session_meta", "payload": {"session_id": "s-1", "cwd": "/tmp/project", "source": "test"}},
                {"type": "turn_context", "payload": {"turn_id": "t-1"}},
                {"type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"text": "hello"}]}},
                {"type": "response_item", "payload": {"type": "reasoning", "id": "reasoning-secret"}},
                {"type": "response_item", "payload": {"type": "function_call", "name": "exec_command", "call_id": "c-1", "command": "printf ok"}},
                {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "c-1", "output": "ok"}},
            ]
            path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
            with patch.object(codex_jsonl, "SESSION_ROOTS", (Path(directory),)):
                result = read_session("s-1", path_hint=str(path))

        self.assertEqual(result["session"]["session_id"], "s-1")
        self.assertEqual(result["session"]["turn_count"], 1)
        self.assertEqual(result["summary"]["tool_call_count"], 1)
        self.assertTrue(all(event["event_type"] != "native.reasoning" for event in result["events"]))
        self.assertEqual(result["events"][-1]["evidence_ref"]["line"], 6)
        self.assertEqual(result["agents"][0]["identity_status"], "SESSION_OBSERVED_AGENT_ID_UNAVAILABLE")

    def test_real_target_session_is_read_only_and_lineage_boundary_is_explicit(self):
        path = Path.home() / ".codex/sessions/2026/06/29/rollout-2026-06-29T17-13-29-019f12a7-b9b1-72d3-92a4-6894c5d34a86.jsonl"
        if not path.exists():
            self.skipTest("local Codex target session is unavailable")
        result = read_session("019f12a7-b9b1-72d3-92a4-6894c5d34a86", path_hint=str(path))
        self.assertGreater(result["session"]["turn_count"], 1)
        self.assertGreater(result["summary"]["tool_call_count"], 0)
        self.assertEqual(result["summary"]["lineage_status"], "NO_NATIVE_AGENT_LINEAGE_FOUND_IN_SESSION")


if __name__ == "__main__":
    unittest.main()
