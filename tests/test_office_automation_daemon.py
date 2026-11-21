#!/usr/bin/env python3
"""
Unit tests for SYNAX 24/7 Autonomous Agent Office Automation Daemon
(`src/synax/office_automation_daemon.py`).
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from synax.office_automation_daemon import AutonomousOfficeAutomationDaemon


class TestAutonomousOfficeAutomationDaemon(unittest.TestCase):
    def test_enqueue_and_execute_real_office_mission(self) -> None:
        """Verifies that a queued mission transitions QUEUED -> COMPLETED and writes real files to disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = Path(tmpdir) / "SYNAX_Workspace"
            daemon = AutonomousOfficeAutomationDaemon(workspace_root=ws)

            queued = daemon.enqueue_mission(
                prompt="Yoğun bakım EKG ve hemodinamik monitörizasyonda sıfır-sapmalı Lyapunov kalibrasyonu",
                skill_id="hypothesis-generation",
                target_agent_id="agent-scholar",
            )
            self.assertEqual(queued["state"], "QUEUED")

            completed = daemon.execute_next_mission(force_autonomous_if_empty=False)
            self.assertEqual(completed["mission_id"], queued["mission_id"])
            self.assertEqual(completed["state"], "COMPLETED")
            self.assertTrue(completed["sandbox_verified"])
            self.assertGreaterEqual(len(completed["saved_files"]), 5)
            for f in completed["saved_files"]:
                self.assertTrue(Path(f).exists())

    def test_inbox_file_drop_auto_ingestion(self) -> None:
        """Verifies that dropping a .txt task file into automation_inbox/ automatically queues and executes it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = Path(tmpdir) / "SYNAX_Workspace"
            daemon = AutonomousOfficeAutomationDaemon(workspace_root=ws)
            task_file = daemon.inbox_dir / "cardiology_mission.txt"
            task_file.write_text("Artificial intelligence in ICU electrocardiogram monitoring", encoding="utf-8")

            ingested = daemon.scan_inbox_directory()
            self.assertEqual(len(ingested), 1)
            self.assertFalse(task_file.exists())  # moved to processed/

            status = daemon.get_status()
            self.assertEqual(status["queued_count"], 1)


if __name__ == "__main__":
    unittest.main()
