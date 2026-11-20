#!/usr/bin/env python3
"""
Unit tests for SYNAX Academic Research & Biostatistical Skills
(`src/synax/academic_skills.py`).
"""

import math
import unittest

from synax.academic_skills import (
    AcademicLiteratureAgent,
    BiostatAndCritiqueAgent,
    VERIFIED_BENCHMARK_CORPUS,
)


class TestAcademicLiteratureSkills(unittest.TestCase):
    def setUp(self) -> None:
        self.scholar = AcademicLiteratureAgent()
        self.biostat = BiostatAndCritiqueAgent()

    def test_verified_benchmark_corpus_integrity(self) -> None:
        """Ensures verified benchmark corpus contains genuine identifiers and no NaN/falsified values."""
        self.assertGreaterEqual(len(VERIFIED_BENCHMARK_CORPUS), 4)
        for study in VERIFIED_BENCHMARK_CORPUS:
            self.assertTrue(study["pmid"].isdigit() or study["pmid"].startswith("CR-"))
            self.assertTrue("doi" in study and len(study["doi"]) > 5)
            self.assertGreater(study["year"], 1980)
            self.assertIsNotNone(study["effect_d"])
            self.assertIsNotNone(study["se"])
            self.assertGreater(study["se"], 0)

    def test_systematic_review_dynamic_prisma(self) -> None:
        """Tests dynamic PRISMA flow accounting without hardcoded values."""
        topic = "Yoğun bakım EKG monitörizasyon"
        rev = self.scholar.conduct_systematic_review(topic, try_live=False)

        self.assertIn("prisma_flow", rev)
        flow = rev["prisma_flow"]
        self.assertGreater(flow["identified_records_total"], 0)
        self.assertEqual(
            flow["records_screened_title_abstract"],
            flow["identified_records_total"] - flow["duplicates_removed"],
        )
        self.assertEqual(len(rev["included_studies"]), flow["studies_included_in_qualitative_synthesis"])

    def test_dersimonian_laird_known_numerical_benchmark(self) -> None:
        """
        Validates DerSimonian-Laird random effects calculations against known mathematical reference:
        Two trials with:
          y1 = 0.5, se1 = 0.1 (v1 = 0.01, w1 = 100)
          y2 = 1.0, se2 = 0.1 (v2 = 0.01, w2 = 100)
        Fixed pooled: theta_fixed = (50 + 100) / 200 = 0.75
        Q = 100*(0.5-0.75)^2 + 100*(1.0-0.75)^2 = 100*(0.0625) + 100*(0.0625) = 12.5
        df = 1
        c_denom = 200 - (20000 / 200) = 200 - 100 = 100
        tau^2 = (12.5 - 1) / 100 = 0.115
        """
        effects = [0.5, 1.0]
        variances = [0.01, 0.01]

        res = BiostatAndCritiqueAgent.calculate_dersimonian_laird(effects, variances)
        self.assertAlmostEqual(res["pooled_fixed"], 0.75, places=3)
        self.assertAlmostEqual(res["cochran_q"], 12.5, places=3)
        self.assertAlmostEqual(res["tau_sq"], 0.115, places=3)
        self.assertAlmostEqual(res["pooled_random"], 0.75, places=3)
        self.assertEqual(res["df"], 1)
        self.assertGreater(res["i_squared_pct"], 90.0)

    def test_insufficient_verified_data_handling(self) -> None:
        """Ensures that missing quantitative data returns INSUFFICIENT_VERIFIED_DATA instead of hallucinating."""
        empty_studies = [
            {"title": "Qualitative Survey", "authors": "Smith J", "year": 2024}
        ]
        res = self.biostat.analyze_and_interpret(empty_studies, "Qualitative exploratory survey")
        self.assertEqual(res["status"], "INSUFFICIENT_VERIFIED_DATA")
        self.assertIn("remedy", res)
        self.assertIn("INSUFFICIENT_VERIFIED_DATA", res["imrad_manuscript_markdown"])


if __name__ == "__main__":
    unittest.main()
