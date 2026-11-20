"""SYNAX-OS Kernel — Preemptive Agent Process Scheduler.

Schedules agent tasks, enforces token quotas, and manages process states.
"""

from __future__ import annotations

import heapq
from typing import Dict, List, Optional
from synax.kernel.process import AgentProcess, ProcessPriority, ProcessState


class AgentScheduler:
    """Multi-level priority preemptive scheduler."""

    def __init__(self) -> None:
        self._processes: Dict[int, AgentProcess] = {}
        self._ready_queue: List[AgentProcess] = []
        self._next_pid: int = 1

    def register_process(self, process: AgentProcess) -> None:
        """Register process into scheduler table."""
        self._processes[process.pid] = process
        if process.state == ProcessState.READY:
            self._ready_queue.append(process)

    def allocate_pid(self) -> int:
        """Allocate unique process ID."""
        pid = self._next_pid
        self._next_pid += 1
        return pid

    def get_process(self, pid: int) -> Optional[AgentProcess]:
        """Look up process by PID."""
        return self._processes.get(pid)

    def list_processes(self) -> List[AgentProcess]:
        """Return all registered processes."""
        return list(self._processes.values())

    def schedule_next(self) -> Optional[AgentProcess]:
        """Select next process to execute using priority ordering."""
        # Filter ready processes
        ready = [p for p in self._processes.values() if p.state == ProcessState.READY]
        if not ready:
            return None
        # Sort by priority (lower integer = higher priority) then oldest active
        ready.sort(key=lambda p: (int(p.priority), p.last_active))
        chosen = ready[0]
        chosen.state = ProcessState.RUNNING
        chosen.tick()
        return chosen

    def yield_process(self, pid: int) -> None:
        """Transition process from RUNNING back to READY."""
        proc = self._processes.get(pid)
        if proc and proc.state == ProcessState.RUNNING:
            proc.state = ProcessState.READY

    def terminate_process(self, pid: int, exit_code: int = 0) -> None:
        """Terminate process and update its status."""
        proc = self._processes.get(pid)
        if proc:
            proc.state = ProcessState.TERMINATED
            proc.metadata["exit_code"] = exit_code
