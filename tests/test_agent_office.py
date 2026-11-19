import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from synax.synax_llm import SynaxTurkishLLM
from synax.academic_skills import AcademicLiteratureAgent, BiostatAndCritiqueAgent, ClaudeCodexSkillPack
from synax.agent_office import MultitaskOfficeOrchestrator, build_embedded_3d_office_html


class TestSynaxAgentOfficeV3(unittest.TestCase):
    def test_turkish_llm_training_and_accuracy(self):
        llm = SynaxTurkishLLM()
        metrics = llm.train(save=False)
        self.assertGreaterEqual(metrics["accuracy_pct"], 98.0)

    def test_academic_scholar_prisma_and_biostat_meta_analysis(self):
        scholar = AcademicLiteratureAgent()
        biostat = BiostatAndCritiqueAgent()
        rev = scholar.conduct_systematic_review(
            "Yoğun bakım EKG ve IBP monitörizasyonunda sıfır-sapmalı Lyapunov kalibrasyonu",
            try_live=False,
        )
        self.assertGreaterEqual(len(rev["included_studies"]), 3)
        self.assertIn("PRISMA 2020", rev["report_markdown"])
        self.assertIn("@article{", rev["bibtex"])

        meta = biostat.analyze_and_interpret(rev["included_studies"], "EKG Lyapunov")
        self.assertGreater(meta["pooled_effect_d"], 0.5)
        self.assertIn("Forest Plot", meta["imrad_manuscript_markdown"])

    def test_8_agent_multitask_and_per_agent_assignment(self):
        orch = MultitaskOfficeOrchestrator()
        # 1. Full 8-agent coordinated mission
        full_res = orch.execute_multitask("8 ajana eşzamanlı görev ver")
        self.assertEqual(full_res["total_agent_count"], 8)
        self.assertEqual(full_res["active_agent_count"], 8)
        self.assertEqual(len(full_res["desks"]), 8)

        # 2. Single-agent targeted assignment (e.g. Masa 2: agent-scholar)
        single_res = orch.execute_multitask(
            "Sepsiste hemodinamik monitörizasyon literatür taraması yap",
            target_agent_id="agent-scholar",
            engine_provider="Claude Code",
        )
        self.assertEqual(single_res["target_agent_id"], "agent-scholar")
        self.assertEqual(single_res["engine_provider"], "Claude Code")
        self.assertIn("PRISMA", single_res["deliverables"]["academic_report_md"])

    def test_v3_3d_office_html_contains_per_agent_controls(self):
        html = build_embedded_3d_office_html()
        self.assertIn("SYNAX 3D AGENT OFFICE v3.0", html)
        self.assertIn("assignTaskToSingleAgent", html)
        self.assertIn("agent-scholar", html)
        self.assertIn("agent-biostat", html)


if __name__ == "__main__":
    unittest.main()
