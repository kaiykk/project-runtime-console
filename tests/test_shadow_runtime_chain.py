import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from packages.judge_deepseek.provider import (
    DshJudgeProvider,
    FakeJudgeProvider,
    select_provider,
)
from packages.judgment_ledger.ledger import JsonlJudgmentLedger
from packages.judgment_sidecar.sidecar import judge_in_shadow
from packages.runtime_events.codex_transcript import read_tool_outputs


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

    @patch("packages.judge_deepseek.provider.subprocess.run")
    @patch("packages.judge_deepseek.provider.shutil.which", return_value="/usr/local/bin/dsh")
    def test_dsh_provider_uses_headless_profile_and_persists_receipt(
        self, _which, run
    ):
        run.return_value = subprocess.CompletedProcess(
            args=["dsh"],
            returncode=0,
            stdout='{"verdict":"KEEP","confidence":0.8}\n',
            stderr="",
        )
        provider = DshJudgeProvider(executable="dsh", profile="headless")

        decision = provider.judge(
            {
                "event_type": "tool.output.value",
                "tool_name": "shell",
                "tool_output": "PRC_DEMO_TOOL_1",
            },
            {"scope": "test"},
        )

        command = run.call_args.args[0]
        self.assertEqual(command[:3], ["dsh", "--profile", "headless"])
        self.assertIn("Return JSON only", command[3])
        self.assertIn("PRC_DEMO_TOOL_1", command[3])
        self.assertEqual(decision.provider_status, "DSH_REAL")
        self.assertEqual(decision.receipt["transport"], "dsh")
        self.assertEqual(decision.receipt["status"], "SUCCEEDED")

    @patch("packages.judge_deepseek.provider.subprocess.run")
    @patch("packages.judge_deepseek.provider.shutil.which", return_value="/usr/local/bin/dsh")
    def test_dsh_failure_is_unknown_with_failure_receipt(self, _which, run):
        run.return_value = subprocess.CompletedProcess(
            args=["dsh"],
            returncode=2,
            stdout="",
            stderr="profile failed",
        )
        provider = DshJudgeProvider(executable="dsh", profile="headless")

        judgment = judge_in_shadow(
            {
                "event_id": "event-dsh-failure",
                "session_id": "session-test",
                "event_type": "tool.output.value",
            },
            provider=provider,
        )

        self.assertEqual(judgment["verdict"], "UNKNOWN")
        self.assertEqual(judgment["provider_status"], "DSH_ERROR:RuntimeError")
        self.assertEqual(judgment["provider_receipt"]["status"], "FAILED")
        self.assertEqual(judgment["provider_receipt"]["return_code"], 2)

    @patch.dict(os.environ, {"PRC_JUDGE_PROVIDER": "dsh"}, clear=True)
    @patch("packages.judge_deepseek.provider.shutil.which", return_value="/usr/local/bin/dsh")
    def test_dsh_is_the_default_provider(self, _which):
        provider, setup_status = select_provider()
        self.assertIsInstance(provider, DshJudgeProvider)
        self.assertEqual(setup_status, "DSH_READY")


if __name__ == "__main__":
    unittest.main()
