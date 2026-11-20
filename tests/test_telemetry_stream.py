#!/usr/bin/env python3
"""Unit tests for SYNAX Agent Telemetry Stream."""

import unittest
from synax.telemetry_stream import AgentTelemetryStream, TelemetryEvent


class TestAgentTelemetryStream(unittest.TestCase):
    """Test suite for agent telemetry event recording and summary."""

    def setUp(self) -> None:
        self.stream = AgentTelemetryStream(max_events=10)

    def test_record_and_serialize_event(self) -> None:
        event = self.stream.record_event(
            agent_id="biomed-autocal",
            event_type="PUBMED_SEARCH",
            payload={"pmid": "38491023", "citations": 4},
        )
        self.assertIsInstance(event, TelemetryEvent)
        self.assertEqual(event.agent_id, "biomed-autocal")
        self.assertEqual(event.event_type, "PUBMED_SEARCH")
        self.assertIn("38491023", event.to_json())

    def test_event_filtering_and_max_capacity(self) -> None:
        for i in range(15):
            agent = "egraph-prover" if i % 2 == 0 else "token-shield"
            self.stream.record_event(agent_id=agent, event_type="TEST_TICK", payload={"i": i})

        events = self.stream.get_events()
        self.assertEqual(len(events), 10)  # Max capacity respected

        filtered = self.stream.get_events(agent_id="egraph-prover")
        self.assertTrue(all(e.agent_id == "egraph-prover" for e in filtered))

    def test_compute_agent_summary(self) -> None:
        self.stream.record_event("biomed-autocal", "CALIBRATE")
        self.stream.record_event("biomed-autocal", "SYNC")
        self.stream.record_event("fullstack-dev", "RENDER_3D")

        summary = self.stream.compute_agent_summary()
        self.assertEqual(summary["total_events"], 3)
        self.assertEqual(summary["agent_distribution"]["biomed-autocal"], 2)
        self.assertEqual(summary["agent_distribution"]["fullstack-dev"], 1)
        self.assertEqual(summary["status"], "HEALTHY")


if __name__ == "__main__":
    unittest.main()
