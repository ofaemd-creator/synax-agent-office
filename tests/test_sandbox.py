#!/usr/bin/env python3
"""
Unit tests for SYNAX Restricted Sandbox & AST Safety Auditor
(`src/synax/sandbox.py`).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from synax.sandbox import ASTSafetyAuditor, SynaxRestrictedSandbox


class TestSandboxModule(unittest.TestCase):
    def setUp(self) -> None:
        self.sandbox = SynaxRestrictedSandbox(timeout_seconds=2.0)

    def test_benign_code_execution(self) -> None:
        """Tests that safe mathematical code executes successfully in sandbox."""
        code = "import math\nx = math.sqrt(16.0)\nprint(f'RESULT={x}')"
        res = self.sandbox.execute(code, user_approved=False)
        self.assertTrue(res.success)
        self.assertIn("RESULT=4.0", res.stdout)
        self.assertEqual(len(res.violations), 0)

    def test_forbidden_imports_blocked(self) -> None:
        """Tests that os, subprocess, and dangerous modules are blocked by AST auditor."""
        forbidden_snippets = [
            "import os\nos.system('ls')",
            "import subprocess\nsubprocess.run(['whoami'])",
            "import socket\ns = socket.socket()",
            "eval('2 + 2')",
        ]
        for snippet in forbidden_snippets:
            violations = self.sandbox.audit_code(snippet)
            self.assertGreater(len(violations), 0, f"Expected violations for: {snippet}")

            # Execution without user approval must be blocked
            res = self.sandbox.execute(snippet, user_approved=False)
            self.assertFalse(res.success)
            self.assertTrue(res.requires_approval)

    def test_timeout_containment(self) -> None:
        """Tests that infinite loops or runaway processes are terminated by timeout."""
        code = "import time\nwhile True:\n    pass"
        # We test with a short timeout sandbox
        short_sandbox = SynaxRestrictedSandbox(timeout_seconds=0.8)
        res = short_sandbox.execute(code, user_approved=True)
        self.assertFalse(res.success)
        self.assertIn("timeout", res.stderr.lower())


if __name__ == "__main__":
    unittest.main()
