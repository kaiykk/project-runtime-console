import json
import tempfile
import unittest
from pathlib import Path

from packages.judge_deepseek.provider import FakeJudgeProvider
from packages.judgment_ledger.ledger import JsonlJudgmentLedger
from packages.judgment_sidecar.sidecar import judge_in_shadow
from packages.runtime_events.codex_transcript import read_tool_outputs
from scripts.run_step1_demo import _sanitize


FIXTURE = """\
{"type":"session_meta","payload":{"session_id":"session-test-001"}}
{"type":"turn_context","payload":{"turn_id":"turn-test-001"}}
{"type":"response_item","ordinal":3,"payload":{"type":"function_call","call_id":"call-test-001","name":"shell"}}
{"type":"response_item","ordinal":4,"payload":{"type":"function_call_output","call_id":"call-test-001","output":"tests passed"}}
"""


class Step1VerticalSliceTests(unittest.TestCase):
    def test_runtime_event_to_shadow_judgment_to_ledger_preserves_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transcript = root / "session.jsonl"
            transcript.write_text(FIXTURE, encoding="utf-8")
            [event] = read_tool_outputs(transcript)
            provider = FakeJudgeProvider()
            judgment = judge_in_shadow(event, provider=provider)
            ledger = JsonlJudgmentLedger(root / "ledger.jsonl")
            ledger.append(judgment)
            [stored] = ledger.read_all()

        self.assertEqual(event["event_id"], judgment["canonical_event_id"])
        self.assertEqual(judgment["canonical_event_id"], stored["canonical_event_id"])
        self.assertEqual(judgment["mode"], "SHADOW")
        self.assertEqual(judgment["verdict"], "IMPORTANT_PROGRESS")
        self.assertEqual(judgment["provider_status"], "FAKE_PROVIDER")

    def test_missing_event_identity_cannot_be_judged(self):
        with self.assertRaisesRegex(ValueError, "canonical event_id"):
            judge_in_shadow(
                {"event_type": "tool.output.value"},
                provider=FakeJudgeProvider(),
            )

    def test_ledger_is_jsonl_and_replayable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.jsonl"
            ledger = JsonlJudgmentLedger(path)
            record = {
                "judgment_id": "judgment-test",
                "canonical_event_id": "event-test",
                "mode": "SHADOW",
            }
            ledger.append(record)
            self.assertEqual(ledger.read_all(), [record])
            self.assertEqual(json.loads(path.read_text())["mode"], "SHADOW")

    def test_demo_redacts_non_demo_tool_output(self):
        redacted = _sanitize(
            "memory matches: private project context; "
            "token=should-not-appear"
        )
        self.assertTrue(redacted.startswith("[REDACTED_TOOL_OUTPUT chars="))
        self.assertNotIn("private project context", redacted)
        self.assertNotIn("should-not-appear", redacted)

    def test_demo_preserves_explicit_safe_marker(self):
        self.assertEqual(
            _sanitize("PRC_DEMO_TOOL_1\nPRC_DEMO_TOOL_2"),
            "PRC_DEMO_TOOL_1\nPRC_DEMO_TOOL_2",
        )


if __name__ == "__main__":
    unittest.main()
