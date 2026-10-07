import unittest

from packages.workstage_projection import project_run


class WorkStageProjectionTests(unittest.TestCase):
    def test_projection_keeps_native_refs_and_marks_derived_semantics(self):
        run = {
            "run": {"run_id": "run-1", "source": "codex.app-server", "history_available": True},
            "agents": [
                {"runtime_agent_instance_id": "root", "parent_runtime_agent_instance_id": None},
                {"runtime_agent_instance_id": "child", "parent_runtime_agent_instance_id": "root"},
            ],
            "turns": [{}],
            "events": [
                {
                    "observation_id": "live:root:turn-1:user-1",
                    "runtime_agent_instance_id": "root",
                    "run_id": "run-1",
                    "turn_id": "turn-1",
                    "provider_item_id": "user-1",
                    "event_type": "userMessage",
                    "reconciliation": "RECONCILIATION_UNRESOLVED",
                    "source": "codex.app-server",
                    "turn_status": "completed",
                }
            ],
        }
        projected = project_run(run)

        self.assertEqual(projected["projection"]["status"], "PARTIAL")
        self.assertEqual(len(projected["nodes"]), 6)
        first = projected["nodes"][projected["top"][0]]
        self.assertEqual(first["data_class"], "DERIVED_SUMMARY")
        self.assertEqual(first["outcome_status"], "NOT_ESTABLISHED")
        self.assertEqual(first["evidence"][0]["evidence_ref"], "live:root:turn-1:user-1")
        self.assertIn("live:root:turn-1:user-1", projected["raw_events"])


if __name__ == "__main__":
    unittest.main()
