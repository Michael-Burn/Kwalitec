"""Execution tracing for adapter / pipeline spans."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from time import perf_counter
from typing import Any
from uuid import uuid4

from app.infrastructure.diagnostics.correlation import CorrelationContext


@dataclass(frozen=True)
class TraceSpan:
    """One operational execution span."""

    span_id: str
    name: str
    started_at: datetime
    ended_at: datetime | None
    duration_ms: float | None
    status: str
    correlation_id: str
    causation_id: str
    attributes: dict[str, Any] = field(default_factory=dict)


class ExecutionTracer:
    """Collect operational spans (no educational interpretation)."""

    def __init__(self) -> None:
        self._spans: list[TraceSpan] = []
        self._open: dict[str, tuple[str, float, datetime, dict[str, Any]]] = {}

    def start(
        self,
        name: str,
        *,
        span_id: str | None = None,
        **attributes: Any,
    ) -> str:
        """Start a span; returns span_id."""
        sid = (span_id or "").strip() or uuid4().hex
        ids = CorrelationContext.current()
        self._open[sid] = (
            name,
            perf_counter(),
            datetime.now(tz=UTC),
            {
                **attributes,
                "correlation_id": ids.correlation_id,
                "causation_id": ids.causation_id,
            },
        )
        return sid

    def end(
        self,
        span_id: str,
        *,
        status: str = "ok",
        **attributes: Any,
    ) -> TraceSpan:
        """End a span and store it."""
        if span_id not in self._open:
            raise KeyError(f"unknown span_id: {span_id}")
        name, t0, started, attrs = self._open.pop(span_id)
        ended = datetime.now(tz=UTC)
        duration_ms = (perf_counter() - t0) * 1000.0
        merged = {**attrs, **attributes}
        span = TraceSpan(
            span_id=span_id,
            name=name,
            started_at=started,
            ended_at=ended,
            duration_ms=duration_ms,
            status=status,
            correlation_id=str(merged.get("correlation_id") or ""),
            causation_id=str(merged.get("causation_id") or ""),
            attributes={
                k: v
                for k, v in merged.items()
                if k not in {"correlation_id", "causation_id"}
            },
        )
        self._spans.append(span)
        return span

    def spans(self) -> tuple[TraceSpan, ...]:
        """Return completed spans in order."""
        return tuple(self._spans)

    def clear(self) -> None:
        """Clear completed and open spans."""
        self._spans.clear()
        self._open.clear()

    def diagnostics(self) -> dict[str, Any]:
        """Operational tracer diagnostics."""
        return {
            "completed_spans": len(self._spans),
            "open_spans": len(self._open),
            "names": [s.name for s in self._spans],
        }
