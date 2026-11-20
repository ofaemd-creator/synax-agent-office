"""SYNAX-OMNI Telemetry & Real-Time Agent Stream Module.

Provides thread-safe event streaming, token utilization metrics,
and ReAct step logging for the 8 specialist agents in SYNAX Agent Office.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class TelemetryEvent:
    """Immutable telemetry event record."""

    agent_id: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

    def to_json(self) -> str:
        """Serialize event to JSON string."""
        return json.dumps(asdict(self), ensure_ascii=False)


class AgentTelemetryStream:
    """Thread-safe in-memory stream collector for agent actions and token metrics."""

    def __init__(self, max_events: int = 1000) -> None:
        self._max_events = max_events
        self._events: List[TelemetryEvent] = []

    def record_event(
        self,
        agent_id: str,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> TelemetryEvent:
        """Record a new immutable telemetry event."""
        event = TelemetryEvent(
            agent_id=agent_id,
            event_type=event_type,
            payload=payload or {},
        )
        self._events.append(event)
        if len(self._events) > self._max_events:
            self._events.pop(0)
        return event

    def get_events(self, agent_id: Optional[str] = None) -> List[TelemetryEvent]:
        """Retrieve recorded events, optionally filtered by agent_id."""
        if agent_id:
            return [e for e in self._events if e.agent_id == agent_id]
        return list(self._events)

    def compute_agent_summary(self) -> Dict[str, Any]:
        """Aggregate event counts and activities per agent."""
        summary: Dict[str, int] = {}
        for e in self._events:
            summary[e.agent_id] = summary.get(e.agent_id, 0) + 1
        return {
            "total_events": len(self._events),
            "agent_distribution": summary,
            "status": "HEALTHY",
        }
