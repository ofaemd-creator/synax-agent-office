#!/usr/bin/env python3
"""
Unit tests for SYNAX Verification State Model & Scientific Assurance
(`src/synax/verification.py`).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from synax.verification import (
    NumericalVerifier,
    VerificationCertificate,
    VerificationStatus,
)


class TestVerificationModule(unittest.TestCase):
    def test_lyapunov_contractivity_success(self) -> None:
        """Tests that contractive convergence rate 0 < gamma < 1 achieves VERIFIED status."""
        cert = NumericalVerifier.verify_lyapunov_contractivity(gamma=0.25, initial_error=2.0, iterations=30)
        self.assertEqual(cert.status, VerificationStatus.VERIFIED)
        self.assertEqual(cert.ulp_bound, 0)
        self.assertTrue(cert.test_results["is_strictly_decreasing"])
        self.assertLess(cert.test_results["final_V"], cert.test_results["initial_V"])

    def test_lyapunov_contractivity_failure(self) -> None:
        """Tests that invalid or unstable gamma rates produce FAILED status."""
        cert_unstable = NumericalVerifier.verify_lyapunov_contractivity(gamma=2.5, initial_error=1.0)
        self.assertEqual(cert_unstable.status, VerificationStatus.FAILED)
        self.assertIn("FAILED", cert_unstable.disclaimer)

        cert_negative = NumericalVerifier.verify_lyapunov_contractivity(gamma=-0.1, initial_error=1.0)
        self.assertEqual(cert_negative.status, VerificationStatus.FAILED)

    def test_ieee754_interval_bounds(self) -> None:
        """Tests interval abstract interpretation safety checks."""
        valid_cert = NumericalVerifier.verify_ieee754_interval_bounds(
            expr_str="fmaf(a, 0.985f, 0.0f)",
            input_bounds={"a": (-5.0, 5.0)},
        )
        self.assertEqual(valid_cert.status, VerificationStatus.VERIFIED)
        self.assertTrue(valid_cert.test_results["overflow_safe"])

        invalid_cert = NumericalVerifier.verify_ieee754_interval_bounds(
            expr_str="faulty_range",
            input_bounds={"a": (5.0, -5.0)},  # Invalid: lo > hi
        )
        self.assertEqual(invalid_cert.status, VerificationStatus.FAILED)

    def test_certificate_serializability(self) -> None:
        """Ensures VerificationCertificate produces JSON-compliant dictionary."""
        cert = NumericalVerifier.verify_lyapunov_contractivity(gamma=0.2, initial_error=1.0, iterations=10)
        d = cert.to_dict()
        self.assertEqual(d["status"], "VERIFIED")
        self.assertIn("artifact_id", d)
        self.assertIn("assumptions", d)
        self.assertIn("disclaimer", d)


if __name__ == "__main__":
    unittest.main()
