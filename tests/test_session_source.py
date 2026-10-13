import json
import os
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
        self.assertEqual(result["agents"], [])
        self.assertEqual(result["lineage"]["status"], "NO_NATIVE_AGENT_LINEAGE_FOUND_IN_SESSION")

    def read_fixture(self, records):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rollout-boundary.jsonl"
            path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
            with patch.object(codex_jsonl, "SESSION_ROOTS", (Path(directory),)):
                return read_session("root", path_hint=str(path))

    def test_dispatch_alias_does_not_remove_tool_result(self):
        result = self.read_fixture([
            {"type": "session_meta", "payload": {"session_id": "root"}},
            {"type": "turn_context", "payload": {"turn_id": "t"}},
            {"type": "response_item", "payload": {"type": "function_call", "name": "spawn_agent", "call_id": "call"}},
            {"type": "event_msg", "payload": {"item": {
                "type": "CollabAgentToolCall", "id": "call", "tool": "spawn_agent",
                "sender_thread_id": "root", "receiver_agents": [{"thread_id": "child"}], "prompt": "Research public docs"}}},
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "call", "output": "created child"}},
        ])
        self.assertEqual(sum(e["kind"] == "agent_event" for e in result["events"]), 1)
        self.assertEqual(sum(e["kind"] == "tool_result" for e in result["events"]), 1)
        self.assertEqual(result["events"][-1]["content"], "created child")
        self.assertEqual(len(result["events"][0]["source_locators"]), 2)
        self.assertEqual(result["lineage"]["child_count"], 1)

    def test_communication_and_missing_sender_do_not_invent_lineage(self):
        records = [{"type": "session_meta", "payload": {"session_id": "root"}}]
        for i, tool in enumerate(("wait", "send_input", "spawn_agent")):
            item = {"type": "CollabAgentToolCall", "id": str(i), "tool": tool,
                    "receiver_agents": [{"thread_id": "other"}]}
            if tool != "spawn_agent":
                item["sender_thread_id"] = "root"
            records.append({"type": "event_msg", "payload": {"item": item}})
        result = self.read_fixture(records)
        self.assertEqual(result["agents"], [])
        self.assertEqual(result["lineage"]["child_count"], 0)
        self.assertEqual(len(result["events"]), 3)

    def test_repeated_turn_id_preserves_occurrence_ownership(self):
        result = self.read_fixture([
            {"type": "session_meta", "payload": {"session_id": "root"}},
            {"type": "turn_context", "payload": {"turn_id": "same"}},
            {"type": "response_item", "payload": {"type": "message", "role": "user", "content": "first"}},
            {"type": "turn_context", "payload": {"turn_id": "same"}},
            {"type": "response_item", "payload": {"type": "message", "role": "user", "content": "second"}},
        ])
        self.assertNotEqual(result["turns"][0]["occurrence_id"], result["turns"][1]["occurrence_id"])
        self.assertNotEqual(result["events"][0]["turn_occurrence_id"], result["events"][1]["turn_occurrence_id"])

    @unittest.skipUnless(os.environ.get("PRC_LOCAL_DIAGNOSTICS") == "1", "private fixture diagnostics are opt-in")
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
