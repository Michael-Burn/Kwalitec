"""Timing helpers for pipeline and AI enrichment spans."""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class TimingRecorder:
    """Accumulate named duration samples in milliseconds."""

    samples: dict[str, list[float]] = field(default_factory=dict)

    def record(self, name: str, duration_ms: float) -> None:
        self.samples.setdefault(name, []).append(float(duration_ms))

    def last(self, name: str) -> float | None:
        values = self.samples.get(name) or []
        return values[-1] if values else None

    def clear(self) -> None:
        self.samples.clear()


@contextmanager
def timed(name: str, recorder: TimingRecorder | None = None) -> Iterator[list[float]]:
    """Context manager yielding a one-element list updated with elapsed ms."""
    slot: list[float] = [0.0]
    started = time.perf_counter()
    try:
        yield slot
    finally:
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        slot[0] = elapsed_ms
        if recorder is not None:
            recorder.record(name, elapsed_ms)
