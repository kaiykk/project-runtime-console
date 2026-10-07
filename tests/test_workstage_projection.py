import unittest

from packages.workstage_projection import project_run


class WorkStageProjectionTests(unittest.TestCase):
    def test_projection_segments_native_windows_without_target_stage_list(self):
        run = {
            "run": {"run_id": "run-1", "source": "codex.app-server", "history_available": True},
            "agents": [
                {"runtime_agent_instance_id": "root", "parent_runtime_agent_instance_id": None},
                {"runtime_agent_instance_id": "child", "parent_runtime_agent_instance_id": "root"},
            ],
            "turns": [{}, {}],
            "events": [
                {
                    "observation_id": "live:root:turn-1:user-1",
                    "runtime_agent_instance_id": "root",
                    "run_id": "run-1",
                    "turn_id": "turn-1",
                    "provider_item_id": "user-1",
                    "event_type": "userMessage",
                    "observed_at": "2026-10-01T00:00:00Z",
                    "native_evidence": {"kind": "user_message", "text": "先研究这个问题，并记录真实的原始证据和验证结果。"},
                    "reconciliation": "RECONCILIATION_UNRESOLVED",
                    "source": "codex.app-server",
                    "turn_status": "completed",
                },
                {
                    "observation_id": "live:root:turn-2:user-2",
                    "runtime_agent_instance_id": "root",
                    "run_id": "run-1",
                    "turn_id": "turn-2",
                    "provider_item_id": "user-2",
                    "event_type": "userMessage",
                    "observed_at": "2026-10-01T01:00:00Z",
                    "native_evidence": {"kind": "user_message", "text": "切换到验证阶段，并保留每一条可回溯的原始证据记录。"},
                    "reconciliation": "RECONCILIATION_UNRESOLVED",
                    "source": "codex.app-server",
                    "turn_status": "completed",
                },
                {
                    "observation_id": "live:child:turn-3:cmd-1",
                    "runtime_agent_instance_id": "child",
                    "run_id": "run-1",
                    "turn_id": "turn-3",
                    "provider_item_id": "cmd-1",
                    "event_type": "commandExecution",
                    "observed_at": "2026-10-01T00:30:00Z",
                    "native_evidence": {"kind": "command", "status": "completed", "exit_code": 0},
                    "reconciliation": "RECONCILIATION_UNRESOLVED",
                    "source": "codex.app-server",
                    "turn_status": "completed",
                },
            ],
        }
        projected = project_run(run)

        self.assertEqual(projected["projection"]["status"], "PARTIAL")
        self.assertFalse(projected["projection"]["manual_target_stage_enumeration"])
        self.assertEqual(len(projected["top"]), 2)
        self.assertEqual(len(projected["nodes"]), 3)
        first = projected["nodes"][projected["top"][0]]
        self.assertEqual(first["data_class"], "DERIVED_SUMMARY")
        self.assertEqual(first["outcome_status"], "NOT_ESTABLISHED")
        self.assertEqual(first["evidence"][0]["evidence_ref"], "live:root:turn-1:user-1")
        self.assertIn("live:root:turn-1:user-1", projected["raw_events"])
        self.assertEqual(first["branch_count"], 1)
        self.assertIn("live:child:turn-3:cmd-1", projected["raw_events"])

    def test_child_dispatch_lineage_wins_over_late_child_event_time(self):
        run = {
            "run": {"run_id": "run-2", "source": "codex.app-server", "history_available": True},
            "agents": [
                {"runtime_agent_instance_id": "root", "parent_runtime_agent_instance_id": None},
                {"runtime_agent_instance_id": "child", "parent_runtime_agent_instance_id": "root"},
            ],
            "events": [
                {
                    "observation_id": "root-anchor-1",
                    "runtime_agent_instance_id": "root",
                    "event_type": "userMessage",
                    "observed_at": "2026-10-01T00:00:00Z",
                    "native_evidence": {"kind": "user_message", "text": "先研究这个问题并记录证据。"},
                },
                {
                    "observation_id": "dispatch-1",
                    "runtime_agent_instance_id": "root",
                    "event_type": "collabAgentToolCall",
                    "observed_at": "2026-10-01T00:10:00Z",
                    "native_evidence": {"kind": "agent_dispatch", "receiver_thread_ids": ["child"]},
                },
                {
                    "observation_id": "root-anchor-2",
                    "runtime_agent_instance_id": "root",
                    "event_type": "userMessage",
                    "observed_at": "2026-10-01T01:00:00Z",
                    "native_evidence": {"kind": "user_message", "text": "切换到验证并保留原始记录。"},
                },
                {
                    "observation_id": "child-event-1",
                    "runtime_agent_instance_id": "child",
                    "event_type": "agentMessage",
                    "observed_at": "2026-10-01T01:10:00Z",
                    "native_evidence": {"kind": "agent_message", "text": "child result"},
                },
            ],
        }
        projected = project_run(run)
        self.assertEqual(projected["subs"]["stage-01"], ["stage-01-branch-01"])
        self.assertEqual(projected["nodes"]["stage-01-branch-01"]["evidence"][0]["title"], "Agent message")

    def test_stage_counts_use_all_child_events_while_evidence_remains_bounded(self):
        events = [
            {
                "observation_id": "anchor",
                "runtime_agent_instance_id": "root",
                "event_type": "userMessage",
                "observed_at": "2026-10-01T00:00:00Z",
                "native_evidence": {"kind": "user_message", "text": "请执行这个验证任务并保留证据。"},
            }
        ]
        for index in range(13):
            events.append(
                {
                    "observation_id": f"child-{index}",
                    "runtime_agent_instance_id": "child",
                    "event_type": "agentMessage",
                    "observed_at": f"2026-10-01T00:{index + 1:02d}:00Z",
                    "native_evidence": {"kind": "agent_message", "text": f"message {index}"},
                }
            )
        projected = project_run({
            "run": {"run_id": "run-3"},
            "agents": [
                {"runtime_agent_instance_id": "root", "parent_runtime_agent_instance_id": None},
                {"runtime_agent_instance_id": "child", "parent_runtime_agent_instance_id": "root"},
            ],
            "events": events,
        })
        branch = projected["nodes"]["stage-01-branch-01"]
        self.assertIn("13 agent messages", branch["outcome"])
        self.assertEqual(len(branch["raw_events"]), 13)
        self.assertEqual(len(branch["evidence"]), 12)


if __name__ == "__main__":
    unittest.main()
