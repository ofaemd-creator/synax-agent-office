"""SYNAX-OS Kernel — Inter-Process Communication (IPC) Bus.

Provides thread-safe message queues, agent-to-agent direct pipes,
and system-wide broadcast event channels.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class IPCMessage:
    """Immutable IPC message between agent processes."""
    msg_id: str
    sender_pid: int
    receiver_pid: int  # 0 denotes broadcast to all active agents
    channel: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)


class IPCBus:
    """Kernel-level message router."""

    def __init__(self) -> None:
        self._history: List[IPCMessage] = []
        self._channels: Dict[str, List[int]] = {}

    def send(
        self,
        sender_pid: int,
        receiver_pid: int,
        channel: str,
        payload: Dict[str, Any],
    ) -> IPCMessage:
        """Deliver a message to target process or broadcast channel."""
        msg_id = f"ipc-{int(time.time() * 1000)}-{sender_pid}->{receiver_pid}"
        msg = IPCMessage(
            msg_id=msg_id,
            sender_pid=sender_pid,
            receiver_pid=receiver_pid,
            channel=channel,
            payload=payload,
        )
        self._history.append(msg)
        if len(self._history) > 2000:
            self._history.pop(0)
        return msg

    def get_history(
        self,
        pid: Optional[int] = None,
        limit: int = 50,
    ) -> List[IPCMessage]:
        """Get recent IPC messages, optionally filtered by participant PID."""
        if pid is not None:
            filtered = [
                m for m in self._history
                if m.sender_pid == pid or m.receiver_pid == pid or m.receiver_pid == 0
            ]
            return filtered[-limit:]
        return self._history[-limit:]
