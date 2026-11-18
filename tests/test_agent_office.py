import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from synax.synax_llm import SynaxTurkishLLM
from synax.agent_office import MultitaskOfficeOrchestrator, build_embedded_3d_office_html


class TestSynaxAgentOfficeAndLLM(unittest.TestCase):
    def test_turkish_llm_training_and_accuracy(self):
        llm = SynaxTurkishLLM()
        metrics = llm.train(save=False)
        self.assertGreaterEqual(metrics["accuracy_pct"], 98.0)
        self.assertLess(metrics["final_loss"], metrics["initial_loss"] + 0.05)

    def test_turkish_conversation_understanding(self):
        llm = SynaxTurkishLLM()
        r1 = llm.chat("Merhaba SYNAX, nasılsın?")
        self.assertIn("SYNAX-LLM", r1["reply"])
        r2 = llm.chat("Biyomedikal EKG cihazında sapmayı nasıl sıfırlıyorsun?")
        self.assertEqual(r2["intent"], "biomedical_autocal")
        self.assertIn("Lyapunov", r2["reply"])
        r3 = llm.chat("25 * 4 kaç eder hesapla")
        self.assertIn("100", r3["reply"])

    def test_3d_multitask_office_orchestrator(self):
        orch = MultitaskOfficeOrchestrator()
        res = orch.execute_multitask("3D Ajan Ofisindeki 6 ajana aynı anda multitask görev ver")
        self.assertEqual(res["total_agent_count"], 6)
        self.assertEqual(res["active_agent_count"], 6)
        self.assertEqual(len(res["desks"]), 6)
        self.assertGreater(len(res["packet_beams"]), 0)

    def test_standalone_3d_office_html_bundle(self):
        html = build_embedded_3d_office_html()
        self.assertIn("office3dCanvas", html)
        self.assertIn("SYNAX-LLM", html)
        self.assertIn("Agent-Lyapunov", html)


if __name__ == "__main__":
    unittest.main()
