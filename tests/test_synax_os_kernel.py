#!/usr/bin/env python3
"""Comprehensive Unit Tests for SYNAX-OS Kernel, Shell & Subsystems."""

import unittest
from synax.kernel.kernel import SynaxOSKernel
from synax.kernel.process import ProcessPriority, ProcessState
from synax.shell import SynaxShell


class TestSynaxOSKernel(unittest.TestCase):
    """Test suite for SYNAX-OS Kernel."""

    def setUp(self) -> None:
        self.kernel = SynaxOSKernel()
        self.kernel.boot()
        self.shell = SynaxShell(kernel=self.kernel)

    def test_boot_subsystems_and_initial_daemons(self) -> None:
        """Verify kernel boots and starts default daemons."""
        self.assertTrue(self.kernel._is_running)
        processes = self.kernel.sys_ps()
        self.assertGreaterEqual(len(processes), 8)
        names = {p["name"] for p in processes}
        self.assertIn("synax-init", names)
        self.assertIn("synax-biomed-autocal", names)
        self.assertIn("synax-egraph-prover", names)
        self.assertIn("synax-super-llm", names)

    def test_process_spawn_and_kill_lifecycle(self) -> None:
        """Test sys_spawn and sys_kill syscalls."""
        proc = self.kernel.sys_spawn(
            name="test-worker",
            role="Worker Agent",
            priority=ProcessPriority.NORMAL,
            token_budget=50000,
        )
        self.assertIsNotNone(proc.pid)
        self.assertEqual(proc.state, ProcessState.READY)

        # Check in VAFS
        status_json = self.kernel.vafs.read_file(f"/proc/agents/{proc.pid}/status")
        self.assertIn("test-worker", status_json)

        # Terminate
        ok = self.kernel.sys_kill(proc.pid, exit_code=0)
        self.assertTrue(ok)
        self.assertEqual(proc.state, ProcessState.TERMINATED)

    def test_ipc_messaging_between_agents(self) -> None:
        """Test inter-process messaging via IPC bus."""
        p1 = self.kernel.sys_spawn("sender", "Role A")
        p2 = self.kernel.sys_spawn("receiver", "Role B")

        msg = self.kernel.sys_send(p1.pid, p2.pid, "telemetry", {"temperature": 37.0})
        self.assertEqual(msg.sender_pid, p1.pid)
        self.assertEqual(msg.receiver_pid, p2.pid)

        # Receiver should have unread message in mailbox
        inbox = self.kernel.sys_recv(p2.pid)
        self.assertEqual(len(inbox), 1)
        self.assertEqual(inbox[0]["temperature"], 37.0)

        # Subsequent recv should be empty
        self.assertEqual(len(self.kernel.sys_recv(p2.pid)), 0)

    def test_vafs_virtual_file_system_operations(self) -> None:
        """Test reading /sys and /dev/tools."""
        version = self.kernel.vafs.read_file("/sys/version")
        self.assertIn("6.1.0-SovereignOS", version)

        tools = self.kernel.vafs.list_dir("/dev/tools")
        self.assertIn("pubmed", tools)
        self.assertIn("python_sandbox", tools)
        self.assertIn("egraph_prover", tools)

    def test_synax_shell_commands(self) -> None:
        """Test shell CLI execution."""
        out_help = self.shell.execute_command("help")
        self.assertIn("SYNAX-OS Built-in Commands", out_help)

        out_ps = self.shell.execute_command("ps")
        self.assertIn("synax-biomed-autocal", out_ps)

        out_top = self.shell.execute_command("top")
        self.assertIn("Tasks:", out_top)

        out_tools = self.shell.execute_command("tools")
        self.assertIn("/dev/tools/pubmed", out_tools)

        out_exec = self.shell.execute_command("exec pubmed 'ECG zero-drift'")
        self.assertIn("NCBI PubMed Live E-utilities", out_exec)


if __name__ == "__main__":
    unittest.main()
