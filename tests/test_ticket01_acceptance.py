import unittest
from pathlib import Path
from unittest.mock import patch
import os

from packages.session_sources.codex_jsonl import read_session
from packages.session_sources.ticket01_acceptance import run_ticket01_acceptance


class Ticket01AcceptanceTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("PRC_LOCAL_DIAGNOSTICS") == "1", "private fixture diagnostics are opt-in")
    def test_pinned_27_agent_projection_preserves_lineage_and_native_mirrors(self):
        path = Path("/Users/kai/.codex/sessions/2026/09/29/rollout-2026-09-29T18-09-54-01a0eca4-7029-7f92-b5a9-2006edb08721.jsonl")
        if not path.exists():
            self.skipTest("pinned 27-Agent Session is unavailable")
        result = read_session("01a0eca4-7029-7f92-b5a9-2006edb08721", path_hint=str(path))
        self.assertEqual(result["lineage"]["child_count"], 26)
        self.assertEqual(result["lineage"]["edge_count"], 26)
        self.assertEqual(len(result["lineage"]["nickname_pairs"]), 26)
        self.assertEqual(sum(pair[1] == "Halley" for pair in result["lineage"]["nickname_pairs"]), 2)
        native = [event for event in result["events"] if event["kind"] == "agent_event"]
        self.assertEqual(len(native), 65)
        self.assertTrue(all(len(event["source_locators"]) == 2 for event in native))

    @unittest.skipUnless(os.environ.get("PRC_LOCAL_DIAGNOSTICS") == "1", "private fixture diagnostics are opt-in")
    def test_pinned_no_lineage_projection_is_empty_and_explicit(self):
        path = Path("/Users/kai/.codex/sessions/2026/07/29/rollout-2026-07-29T16-11-42-019faced-f11a-75e1-ac20-8b95e24d4628.jsonl")
        if not path.exists():
            self.skipTest("pinned no-lineage Session is unavailable")
        result = read_session("019faced-f11a-75e1-ac20-8b95e24d4628", path_hint=str(path))
        self.assertEqual(result["agents"], [])
        self.assertEqual(result["lineage"]["status"], "NO_NATIVE_AGENT_LINEAGE_FOUND_IN_SESSION")
        self.assertEqual(result["lineage"]["edge_count"], 0)

    def test_diagnostic_pass_is_not_product_acceptance(self):
        case = {"status": "PASS", "available": True,
                "checks": [{"severity": "hard", "status": "PASS", "passed": True}]}
        with patch("packages.session_sources.ticket01_acceptance._case_result", return_value=case), \
             patch("packages.session_sources.ticket01_acceptance.BASELINE_FILES", ()):
            result = run_ticket01_acceptance()
        self.assertEqual(result["status"], "DIAGNOSTIC_PASS")
        self.assertEqual(result["product_acceptance"], "NOT_ASSESSED")
        self.assertFalse(result["dsh"]["formal"])
        self.assertTrue(result["read_only"])


if __name__ == "__main__":
    unittest.main()
