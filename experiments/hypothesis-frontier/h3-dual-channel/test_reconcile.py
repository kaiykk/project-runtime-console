import unittest

from reconcile import ReconciliationState, reconcile


def fixture(**overrides):
    event = {
        "event_id": "evt-001",
        "provider_event_id": "provider-evt-001",
        "provider": "codex",
        "run_id": "run-sanitized",
        "agent_id": "agent-main",
        "kind": "tool.output.value",
        "tool_name": "sanitized_tool",
        "value": "[sanitized result: ok]",
        "observed_at": "2026-10-05T10:00:00Z",
    }
    event.update(overrides)
    return event


class ReconciliationProbeTests(unittest.TestCase):
    def test_duplicate_hook_observations_are_collapsed_by_stable_identity(self):
        records = reconcile(
            [
                fixture(observed_at="2026-10-05T10:00:00Z"),
                fixture(observed_at="2026-10-05T10:00:01Z"),
            ],
            [],
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].terminal_state, ReconciliationState.HOOK_ONLY)
        self.assertEqual(
            records[0].states,
            (
                ReconciliationState.HOOK_OBSERVED,
                ReconciliationState.HOOK_ONLY,
            ),
        )

    def test_matching_provider_event_ids_correlate_without_event_id(self):
        records = reconcile(
            [
                fixture(
                    event_id=None,
                    provider_event_id="provider-evt-007",
                    observed_at="2026-10-05T10:00:00Z",
                )
            ],
            [
                fixture(
                    event_id=None,
                    provider_event_id="provider-evt-007",
                    provider=None,
                    observed_at="2026-10-05T10:00:03Z",
                )
            ],
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].terminal_state, ReconciliationState.CORRELATED)
        self.assertEqual(
            records[0].states,
            (
                ReconciliationState.HOOK_OBSERVED,
                ReconciliationState.TRANSCRIPT_OBSERVED,
                ReconciliationState.CORRELATED,
            ),
        )

    def test_same_identity_with_different_sanitized_payload_is_conflict(self):
        records = reconcile(
            [fixture()],
            [fixture(value="[sanitized result: changed]")],
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].terminal_state, ReconciliationState.CONFLICT)
        self.assertEqual(
            records[0].states[-1],
            ReconciliationState.CONFLICT,
        )

    def test_same_timestamp_without_stable_identity_does_not_correlate(self):
        records = reconcile(
            [
                fixture(
                    event_id=None,
                    provider_event_id=None,
                    observed_at="2026-10-05T10:00:00Z",
                )
            ],
            [
                fixture(
                    event_id=None,
                    provider_event_id=None,
                    observed_at="2026-10-05T10:00:00Z",
                )
            ],
        )

        self.assertEqual(
            [record.terminal_state for record in records],
            [
                ReconciliationState.HOOK_ONLY,
                ReconciliationState.TRANSCRIPT_ONLY,
            ],
        )

    def test_unmatched_transcript_is_retained_as_transcript_only(self):
        records = reconcile(
            [],
            [fixture(event_id="evt-transcript-only")],
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(
            records[0].terminal_state,
            ReconciliationState.TRANSCRIPT_ONLY,
        )
        self.assertEqual(
            records[0].states,
            (
                ReconciliationState.TRANSCRIPT_OBSERVED,
                ReconciliationState.TRANSCRIPT_ONLY,
            ),
        )


if __name__ == "__main__":
    unittest.main()
