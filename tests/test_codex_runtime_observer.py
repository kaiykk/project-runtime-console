import unittest

from packages.codex_runtime.app_server import AppServerInfo
from packages.codex_runtime.observer import CodexRuntimeObserver, _event


class FakeClient:
    def __init__(self):
        self.info = AppServerInfo("Codex test", "/tmp/codex", "unix", "macos")
        self.started = False
        self.requests = []

    def start(self):
        self.started = True
        return self.info

    def close(self):
        self.started = False

    def request(self, method, params=None):
        self.requests.append((method, params))
        if method == "thread/list":
            return {"data": [
                {
                    "id": "child-1",
                    "sessionId": "child-session-1",
                    "parentThreadId": "root-1",
                    "status": {"type": "completed"},
                    "cwd": "/tmp/project",
                    "agentRole": "worker",
                },
                {
                    "id": "root-1",
                    "sessionId": "run-1",
                    "parentThreadId": None,
                    "status": {"type": "active"},
                    "cwd": "/tmp/project",
                    "agentRole": "coordinator",
                },
            ]}
        if method == "thread/read":
            thread_id = params["threadId"]
            return {"thread": {
                "id": thread_id,
                "sessionId": "run-1",
                "parentThreadId": "root-1" if thread_id == "child-1" else None,
                "status": {"type": "completed" if thread_id == "child-1" else "active"},
                "cwd": "/tmp/project",
                "turns": [{
                    "id": f"turn-{thread_id}",
                    "status": {"type": "completed"},
                    "items": [{
                        "id": f"item-{thread_id}",
                        "type": "functionCallOutput",
                        "callId": f"call-{thread_id}",
                        "output": "private output is not persisted",
                    }],
                }],
            }}
        raise AssertionError(method)

    def notifications_since(self, cursor=0):
        return 1, [{"method": "thread/status/changed", "params": {"threadId": "root-1"}}]


class CodexRuntimeObserverTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeClient()
        self.observer = CodexRuntimeObserver(self.client)

    def test_groups_native_thread_ids_without_session_collision(self):
        runs = self.observer.list_runs()

        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["run_id"], "run-1")
        self.assertEqual(set(runs[0]["agent_ids"]), {"root-1", "child-1"})
        self.assertEqual(runs[0]["run_id"], "run-1")
        self.assertEqual(
            dict(self.client.requests)["thread/list"]["sourceKinds"][-1],
            "unknown",
        )
        self.assertEqual(runs[0]["status"], "working")

    def test_read_run_preserves_native_lineage_and_marks_reconciliation(self):
        result = self.observer.read_run("run-1")

        agents = {agent["runtime_agent_instance_id"]: agent for agent in result["agents"]}
        self.assertIsNone(agents["root-1"]["parent_runtime_agent_instance_id"])
        self.assertEqual(agents["child-1"]["parent_runtime_agent_instance_id"], "root-1")
        self.assertEqual(result["events"][0]["provider_item_id"], "item-root-1")
        self.assertIsNone(result["events"][0]["canonical_event_id"])
        self.assertEqual(result["events"][0]["reconciliation"], "RECONCILIATION_UNRESOLVED")
        self.assertEqual(result["reconciliation"]["unresolved_event_count"], 2)
        self.assertTrue(any(method == "thread/read" for method, _ in self.client.requests))

    def test_read_agent_projects_native_change_evidence_without_calling_it_an_outcome(self):
        file_event = _event(
            {"id": "root-1", "sessionId": "run-1"},
            {"id": "turn-1", "status": {"type": "completed"}},
            {
                "id": "file-1",
                "type": "fileChange",
                "changes": [{"path": "/tmp/project/result.py", "kind": {"type": "update"}}],
            },
        )
        command_event = _event(
            {"id": "root-1", "sessionId": "run-1"},
            {"id": "turn-1", "status": {"type": "completed"}},
            {
                "id": "command-1",
                "type": "commandExecution",
                "command": "pytest -q",
                "cwd": "/tmp/project",
                "status": "completed",
                "exitCode": 0,
                "durationMs": 42,
                "aggregatedOutput": "2 passed",
            },
        )

        self.assertEqual(file_event["native_evidence"], {
            "kind": "file_change",
            "files": [{"path": "/tmp/project/result.py", "kind": "update"}],
            "change_count": 1,
        })
        self.assertEqual(command_event["native_evidence"]["status"], "completed")
        self.assertEqual(command_event["native_evidence"]["exit_code"], 0)
        self.assertEqual(command_event["native_evidence"]["output_summary"], "2 passed")
        self.assertNotIn("outcome", file_event)
        self.assertNotIn("outcome", command_event)


if __name__ == "__main__":
    unittest.main()
