"""Correlation ID context for cross-adapter request linkage."""

from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass
from uuid import uuid4

_CORRELATION: ContextVar[str] = ContextVar("v2_correlation_id", default="")
_CAUSATION: ContextVar[str] = ContextVar("v2_causation_id", default="")


@dataclass(frozen=True)
class CorrelationIds:
    """Pair of correlation / causation identifiers."""

    correlation_id: str
    causation_id: str


class CorrelationContext:
    """Manage correlation and causation IDs for a request / pipeline."""

    @staticmethod
    def new_correlation_id() -> str:
        """Allocate a new correlation id."""
        return uuid4().hex

    @staticmethod
    def get_correlation_id() -> str:
        """Return the current correlation id (may be empty)."""
        return _CORRELATION.get()

    @staticmethod
    def get_causation_id() -> str:
        """Return the current causation id (may be empty)."""
        return _CAUSATION.get()

    @staticmethod
    def current() -> CorrelationIds:
        """Return the current correlation pair."""
        return CorrelationIds(
            correlation_id=_CORRELATION.get(),
            causation_id=_CAUSATION.get(),
        )

    @staticmethod
    def set(
        *,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> tuple[Token[str], Token[str]]:
        """Set correlation context; returns tokens for reset."""
        corr = (correlation_id or "").strip() or uuid4().hex
        cause = (causation_id or "").strip()
        t1 = _CORRELATION.set(corr)
        t2 = _CAUSATION.set(cause)
        return t1, t2

    @staticmethod
    def reset(tokens: tuple[Token[str], Token[str]]) -> None:
        """Reset correlation context using tokens from ``set``."""
        _CORRELATION.reset(tokens[0])
        _CAUSATION.reset(tokens[1])

    @classmethod
    def bind(
        cls,
        *,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ):
        """Context manager binding correlation ids."""

        class _Binder:
            def __enter__(self) -> CorrelationIds:
                self._tokens = cls.set(
                    correlation_id=correlation_id,
                    causation_id=causation_id,
                )
                return cls.current()

            def __exit__(self, *exc) -> None:
                cls.reset(self._tokens)

        return _Binder()
