#!/usr/bin/env python3
"""
Unit tests for SYNAX Multi-Agent Orchestration Pipeline
(`src/synax/agent_pipeline.py`).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from synax.agent_pipeline import (
    PipelineTask,
    TaskState,
    ThreeAgentResearchPipeline,
)


class TestAgentPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = ThreeAgentResearchPipeline()

    def test_task_state_transitions(self) -> None:
        """Tests that task transitions follow structured state machine."""
        task = self.pipeline.create_task(
            agent_id="test-agent",
            description="Sample testing task",
            input_data={"data": 123},
        )
        self.assertEqual(task.state, TaskState.QUEUED)
        self.assertEqual(len(task.events), 1)

        task.transition(TaskState.RUNNING, "Starting execution")
        self.assertEqual(task.state, TaskState.RUNNING)
        self.assertEqual(len(task.events), 2)

        task.transition(TaskState.COMPLETED, "Execution complete")
        self.assertEqual(task.state, TaskState.COMPLETED)
        self.assertEqual(len(task.events), 3)

    def test_three_agent_pipeline_end_to_end(self) -> None:
        """Tests end-to-end execution of Research -> Analysis -> Verification pipeline."""
        topic = "Yoğun bakım EKG ve hemodinamik monitörizasyon"
        result = self.pipeline.execute_pipeline(
            research_topic=topic,
            auto_approve_sandbox=True,
            try_live=False,
        )

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(len(result["stages"]), 3)

        # Stage 1: Research
        s1 = result["stages"][0]
        self.assertEqual(s1["agent_id"], "agent-scholar")
        self.assertEqual(s1["state"], "COMPLETED")

        # Stage 2: Analysis
        s2 = result["stages"][1]
        self.assertEqual(s2["agent_id"], "agent-biostat")
        self.assertEqual(s2["state"], "COMPLETED")
        self.assertIn("reproducible_code", s2["output_data"])

        # Stage 3: Verification
        s3 = result["stages"][2]
        self.assertEqual(s3["agent_id"], "agent-verifier")
        self.assertEqual(s3["state"], "COMPLETED")

        # Verification certificate assertions
        cert = result["final_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert["status"], "VERIFIED")
        self.assertAlmostEqual(cert["test_results"]["discrepancy"], 0.0, places=3)

    def test_pipeline_approval_checkpoint(self) -> None:
        """Tests that when auto_approve_sandbox is False, pipeline pauses at WAITING_FOR_APPROVAL."""
        topic = "Yoğun bakım EKG monitörizasyon"
        result = self.pipeline.execute_pipeline(
            research_topic=topic,
            auto_approve_sandbox=False,
            try_live=False,
        )
        self.assertEqual(result["status"], "WAITING_FOR_APPROVAL")
        self.assertIn("pending_task", result)
        self.assertEqual(result["pending_task"]["state"], "WAITING_FOR_APPROVAL")


if __name__ == "__main__":
    unittest.main()
