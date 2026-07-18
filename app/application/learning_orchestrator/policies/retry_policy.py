"""Stateless retry rules for technical port call retries.

Retries are technical only. The orchestrator never retries to recover
educational state.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    """Deterministic technical retry configuration.

    Attributes:
        max_attempts: Maximum port-call attempts (including the first).
        retry_on_unavailable: When True, retry if the port raises
            ``PortUnavailable`` / reports unavailable mid-call.
        retry_on_port_error: When True, retry on generic ``PortError``.
        retry_on_unexpected: When True, retry on unexpected exceptions
            raised by a port (technical isolation only).
    """

    max_attempts: int = 1
    retry_on_unavailable: bool = False
    retry_on_port_error: bool = False
    retry_on_unexpected: bool = False

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")

    @classmethod
    def none(cls) -> RetryPolicy:
        """No retries — single attempt only."""
        return cls(max_attempts=1)

    @classmethod
    def technical(cls, *, max_attempts: int = 3) -> RetryPolicy:
        """Retry technical port failures up to ``max_attempts``."""
        return cls(
            max_attempts=max_attempts,
            retry_on_unavailable=True,
            retry_on_port_error=True,
            retry_on_unexpected=True,
        )

    def should_retry(self, *, attempt: int, error_kind: str) -> bool:
        """True when another attempt is allowed after ``error_kind``.

        Args:
            attempt: 1-based attempt number that just failed.
            error_kind: ``unavailable`` | ``port_error`` | ``other``.
        """
        if attempt >= self.max_attempts:
            return False
        if error_kind == "unavailable":
            return self.retry_on_unavailable
        if error_kind == "port_error":
            return self.retry_on_port_error
        if error_kind == "other":
            return self.retry_on_unexpected
        return False
