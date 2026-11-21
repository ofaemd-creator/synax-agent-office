#!/usr/bin/env python3
"""
Unit tests for SYNAX Autonomous Self-Evolution & Continuous Skill Growth Engine
(`src/synax/self_evolution_engine.py`).
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from synax.self_evolution_engine import SynaxAutonomousEvolutionEngine


class TestAutonomousSelfEvolution(unittest.TestCase):
    def test_autonomous_skill_synthesis_and_website_feed_update(self) -> None:
        """Verifies that an evolution cycle passes the verification gate, writes a new SKILL.md, and updates docs/evolution_feed.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_repo = Path(tmpdir)
            engine = SynaxAutonomousEvolutionEngine(
                repo_root=tmp_repo,
                plugin_skills_root=tmp_repo / "plugin_skills",
            )
            feed1 = engine.run_evolution_cycle(sync_plugin_dir=True)
            self.assertEqual(feed1["status"], "AUTONOMOUS_EVOLUTION_ACTIVE")
            self.assertEqual(feed1["evolution_epoch"], 1)
            self.assertTrue(feed1["verification_gate"]["passed"])
            sid1 = feed1["latest_evolved_skill"]["id"]
            self.assertTrue((tmp_repo / "skills" / sid1 / "SKILL.md").exists())
            self.assertTrue((tmp_repo / "docs" / "evolution_feed.json").exists())

            # Run a second cycle with a custom topic
            feed2 = engine.run_evolution_cycle(custom_topic="Pediatric ICU Sepsis Telemetry", sync_plugin_dir=True)
            self.assertEqual(feed2["evolution_epoch"], 2)
            self.assertGreaterEqual(feed2["total_installed_skills"], 2)

    def test_malicious_topic_is_sanitized_during_evolution(self) -> None:
        """Ensures zero code injection even if an external topic contains shell/script payloads."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_repo = Path(tmpdir)
            engine = SynaxAutonomousEvolutionEngine(repo_root=tmp_repo, plugin_skills_root=tmp_repo / "p")
            feed = engine.run_evolution_cycle(custom_topic="Telemetry; rm -rf / <script>alert(1)</script>")
            skill_file = tmp_repo / feed["latest_evolved_skill"]["installed_path"]
            content = skill_file.read_text(encoding="utf-8")
            self.assertNotIn("rm -rf", content)
            self.assertNotIn("<script>", content)


if __name__ == "__main__":
    unittest.main()
