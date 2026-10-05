import json
import tempfile
import unittest
from pathlib import Path

from transcript_watcher import TranscriptParser, TranscriptWatcher


HERE = Path(__file__).parent
FIXTURE = HERE / "fixtures" / "sanitized_tool_result.jsonl"


def fixture_events() -> list[dict]:
    parser = TranscriptParser()
    events = []
    for line in FIXTURE.read_bytes().splitlines(keepends=True):
        event = parser.feed_line(line)
        if event is not None:
            events.append(event)
    return events


class TranscriptParserTests(unittest.TestCase):
    def test_normalizes_sanitized_tool_result_with_stable_correlation(self):
        [event] = fixture_events()

        self.assertEqual(event["event_type"], "tool.output.value")
        self.assertEqual(event["mode"], "SHADOW")
        self.assertEqual(event["source"], "codex.transcript")
        self.assertEqual(event["session_id"], "session-sanitized-001")
        self.assertEqual(event["turn_id"], "turn-sanitized-001")
        self.assertEqual(event["call_id"], "call-sanitized-001")
        self.assertEqual(event["tool_name"], "read_fixture")
        self.assertEqual(event["source_ordinal"], 4)
        self.assertEqual(event["correlation_state"], "CORRELATED")
        self.assertEqual(event["tool_output"], "sanitized tool result")
        self.assertTrue(event["event_id"].startswith("codex-transcript-"))

        [same_event] = fixture_events()
        self.assertEqual(event["event_id"], same_event["event_id"])
        self.assertEqual(
            event["correlation_key"],
            "session-sanitized-001:call-sanitized-001",
        )

    def test_same_timestamp_does_not_define_event_identity(self):
        parser = TranscriptParser()
        parser.feed_record(
            {
                "type": "session_meta",
                "payload": {"session_id": "session-sanitized-002"},
            }
        )
        first = parser.feed_record(
            {
                "type": "response_item",
                "ordinal": 10,
                "timestamp": "2026-10-05T15:00:00.000Z",
                "payload": {
                    "type": "function_call_output",
                    "call_id": "call-sanitized-010",
                    "output": "first",
                },
            }
        )
        second = parser.feed_record(
            {
                "type": "response_item",
                "ordinal": 11,
                "timestamp": "2026-10-05T15:00:00.000Z",
                "payload": {
                    "type": "function_call_output",
                    "call_id": "call-sanitized-011",
                    "output": "second",
                },
            }
        )

        self.assertNotEqual(first["event_id"], second["event_id"])
        self.assertNotEqual(first["correlation_key"], second["correlation_key"])

    def test_missing_identity_is_explicitly_unresolved(self):
        parser = TranscriptParser()
        parser.feed_record(
            {
                "type": "session_meta",
                "payload": {"session_id": "session-sanitized-003"},
            }
        )
        event = parser.feed_record(
            {
                "type": "response_item",
                "ordinal": 12,
                "payload": {
                    "type": "function_call_output",
                    "output": "without call id",
                },
            }
        )

        self.assertEqual(event["correlation_state"], "PARTIAL")
        self.assertIsNone(event["event_id"])
        self.assertIsNone(event["correlation_key"])

    def test_malformed_line_is_ignored_without_inventing_an_event(self):
        parser = TranscriptParser()
        self.assertIsNone(parser.feed_line(b'{"type":'))


class TranscriptWatcherTests(unittest.TestCase):
    def test_poll_waits_for_complete_jsonl_line(self):
        session_line = (
            '{"type":"session_meta","payload":'
            '{"session_id":"session-sanitized-004"}}\n'
        )
        output_prefix = (
            '{"type":"response_item","ordinal":2,"payload":'
            '{"type":"function_call_output","call_id":"call-sanitized-004",'
            '"output":"partial'
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transcript.jsonl"
            path.write_text(session_line + output_prefix, encoding="utf-8")
            watcher = TranscriptWatcher(path)

            self.assertEqual(watcher.poll(), [])

            with path.open("a", encoding="utf-8") as stream:
                stream.write(' tool result"}}\n')

            [event] = watcher.poll()
            self.assertEqual(event["call_id"], "call-sanitized-004")
            self.assertEqual(event["tool_output"], "partial tool result")
            self.assertEqual(watcher.poll(), [])

    def test_fixture_can_be_watched_from_start_to_finish(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transcript.jsonl"
            path.write_bytes(FIXTURE.read_bytes())

            watcher = TranscriptWatcher(path)
            events = watcher.poll()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["correlation_state"], "CORRELATED")


if __name__ == "__main__":
    unittest.main()
