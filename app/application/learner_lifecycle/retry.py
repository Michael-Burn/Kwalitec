"""Technical retry policy for lifecycle stage invocation (LP-001).

Retries are technical only. Educational state is never recovered by
re-interpreting evidence — recovery re-invokes EI services idempotently.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LifecycleRetryPolicy:
    """Deterministic technical retry configuration."""

    max_attempts: int = 3
    retry_on_unexpected: bool = True

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")

    @classmethod
    def none(cls) -> LifecycleRetryPolicy:
        return cls(max_attempts=1, retry_on_unexpected=False)

    @classmethod
    def technical(cls, *, max_attempts: int = 3) -> LifecycleRetryPolicy:
        return cls(max_attempts=max_attempts, retry_on_unexpected=True)

    def should_retry(self, *, attempt: int) -> bool:
        """True when another attempt is allowed after a technical failure."""
        if not self.retry_on_unexpected:
            return False
        return attempt < self.max_attempts
