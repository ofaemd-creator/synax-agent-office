"""SYNAX-OS Interactive Shell (synax-sh).

Provides standard command-line interface to the SYNAX-OS Kernel.
"""

from __future__ import annotations

import json
import shlex
from typing import Any, Dict, List, Optional
from synax.kernel.kernel import SynaxOSKernel


class SynaxShell:
    """Command interpreter for SYNAX-OS."""

    def __init__(self, kernel: Optional[SynaxOSKernel] = None) -> None:
        self.kernel = kernel or SynaxOSKernel()
        if not self.kernel._is_running:
            self.kernel.boot()

    def execute_command(self, cmdline: str) -> str:
        """Parse and execute a shell command line."""
        cmdline = cmdline.strip()
        if not cmdline:
            return ""

        parts = shlex.split(cmdline)
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "help":
            return (
                "SYNAX-OS Built-in Commands:\n"
                "  ps               - List all active agent processes\n"
                "  top              - System activity and agent distribution\n"
                "  spawn <name> <r> - Spawn a new agent process\n"
                "  kill <pid>       - Terminate an agent process\n"
                "  send <s_pid> <r_pid> <msg> - Send an IPC message between agents\n"
                "  recv <pid>       - Read unread mailbox messages for an agent\n"
                "  ls <path>        - List virtual files in VAFS (e.g., ls /dev/tools)\n"
                "  cat <path>       - Read file from VAFS (e.g., cat /sys/uptime)\n"
                "  tools            - List registered device tools\n"
                "  exec <tool> <q>  - Execute a tool device via syscall\n"
                "  uptime           - Show OS uptime and version\n"
            )

        elif cmd == "ps":
            processes = self.kernel.sys_ps()
            lines = [f"{'PID':<4} {'NAME':<28} {'STATE':<12} {'CYCLES':<8} {'TOKENS':<8} {'ROLE'}"]
            lines.append("-" * 90)
            for p in processes:
                lines.append(
                    f"{p['pid']:<4} {p['name']:<28} {p['state']:<12} "
                    f"{p['cpu_cycles_used']:<8} {p['tokens_consumed']:<8} {p['role'][:35]}"
                )
            return "\n".join(lines)

        elif cmd == "top":
            summary = self.kernel.telemetry.compute_agent_summary()
            processes = self.kernel.sys_ps()
            running = sum(1 for p in processes if p["state"] == "RUNNING")
            ready = sum(1 for p in processes if p["state"] == "READY")
            return (
                f"SYNAX-OS {self.kernel.VERSION} - Uptime: {self.kernel.vafs.read_file('/sys/uptime')}\n"
                f"Tasks: {len(processes)} total, {running} running, {ready} ready\n"
                f"Events Logged: {summary['total_events']} | System Health: {summary['status']}\n"
            )

        elif cmd == "spawn":
            if len(args) < 2:
                return "Usage: spawn <name> <role>"
            name = args[0]
            role = " ".join(args[1:])
            proc = self.kernel.sys_spawn(name=name, role=role)
            return f"Process spawned successfully: PID {proc.pid} ({proc.name})"

        elif cmd == "kill":
            if not args:
                return "Usage: kill <pid>"
            try:
                pid = int(args[0])
            except ValueError:
                return "Error: PID must be an integer"
            ok = self.kernel.sys_kill(pid)
            return f"Process {pid} terminated." if ok else f"Error: PID {pid} not found."

        elif cmd == "send":
            if len(args) < 3:
                return "Usage: send <sender_pid> <receiver_pid> <message>"
            try:
                s_pid, r_pid = int(args[0]), int(args[1])
            except ValueError:
                return "Error: PIDs must be integers"
            content = " ".join(args[2:])
            msg = self.kernel.sys_send(s_pid, r_pid, "chat", {"text": content})
            return f"Message delivered: {msg.msg_id}"

        elif cmd == "recv":
            if not args:
                return "Usage: recv <pid>"
            try:
                pid = int(args[0])
            except ValueError:
                return "Error: PID must be an integer"
            messages = self.kernel.sys_recv(pid)
            return json.dumps(messages, indent=2) if messages else "No unread messages."

        elif cmd == "ls":
            path = args[0] if args else "/"
            try:
                items = self.kernel.vafs.list_dir(path)
                return "  ".join(items)
            except Exception as e:
                return f"ls error: {e}"

        elif cmd == "cat":
            if not args:
                return "Usage: cat <path>"
            try:
                return self.kernel.vafs.read_file(args[0])
            except Exception as e:
                return f"cat error: {e}"

        elif cmd == "tools":
            tools = list(self.kernel.tools_registry.keys())
            return "Available System Tools: " + ", ".join(f"/dev/tools/{t}" for t in tools)

        elif cmd == "exec":
            if not args:
                return "Usage: exec <tool_name> [query/arguments]"
            tool_name = args[0]
            query = " ".join(args[1:]) if len(args) > 1 else ""
            result = self.kernel.sys_exec_tool(tool_name, {"query": query, "code": query, "text": query})
            return json.dumps(result, indent=2)

        elif cmd == "uptime":
            return f"{self.kernel.VERSION} | Uptime: {self.kernel.vafs.read_file('/sys/uptime')}"

        else:
            return f"synax-sh: command not found: {cmd}. Type 'help' for available commands."
