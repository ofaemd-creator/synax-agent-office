"""SYNAX-OS Kernel — Agent Process & Lifecycle Management.

Defines the Agent Process Descriptor (PCB - Process Control Block),
execution states, priorities, and token/CPU resource limits.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class ProcessState(str, Enum):
    """Lifecycle states of an agent process in SYNAX-OS."""
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    SLEEPING = "SLEEPING"
    BLOCKED = "BLOCKED"
    TERMINATED = "TERMINATED"
    ZOMBIE = "ZOMBIE"


class ProcessPriority(int, Enum):
    """Scheduling priority levels."""
    SYSTEM_CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND_IDLE = 4


@dataclass
class AgentProcess:
    """Process Control Block (PCB) representing an active Agent Process."""
    pid: int
    name: str
    role: str
    priority: ProcessPriority = ProcessPriority.NORMAL
    state: ProcessState = ProcessState.NEW
    cpu_cycles_used: int = 0
    tokens_consumed: int = 0
    token_budget: int = 100000
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    parent_pid: Optional[int] = None
    mailbox: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    entrypoint: Optional[Callable[..., Any]] = None

    def tick(self, cycles: int = 1) -> None:
        """Advance CPU execution cycle count."""
        self.cpu_cycles_used += cycles
        self.last_active = time.time()

    def consume_tokens(self, amount: int) -> bool:
        """Deduct tokens from the assigned process budget. Returns False if budget exceeded."""
        if self.tokens_consumed + amount > self.token_budget:
            return False
        self.tokens_consumed += amount
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Serialize process status for `/proc/agents/<pid>`."""
        return {
            "pid": self.pid,
            "name": self.name,
            "role": self.role,
            "state": self.state.value,
            "priority": self.priority.name,
            "cpu_cycles_used": self.cpu_cycles_used,
            "tokens_consumed": self.tokens_consumed,
            "token_budget": self.token_budget,
            "uptime_seconds": round(time.time() - self.created_at, 2),
            "unread_messages": len(self.mailbox),
            "parent_pid": self.parent_pid,
            "metadata": self.metadata,
        }
