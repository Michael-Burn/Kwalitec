"""Background job runner with retries, structured logging, and dead-letter (PR-001).

Wraps manually invoked automation / maintenance callables. There is no
external broker (Celery/APScheduler are intentionally unused).
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, TypeVar

logger = logging.getLogger("kwalitec.jobs")

T = TypeVar("T")


@dataclass
class DeadLetterRecord:
    """Record of a job that exhausted retries."""

    job_name: str
    attempts: int
    error: str
    failed_at: str
    payload: dict[str, Any] = field(default_factory=dict)


# In-process dead-letter buffer for operator inspection / health surfaces.
_DEAD_LETTERS: list[DeadLetterRecord] = []


def dead_letters(*, limit: int = 50) -> list[DeadLetterRecord]:
    """Return recent dead-letter records (newest last)."""
    if limit <= 0:
        return list(_DEAD_LETTERS)
    return list(_DEAD_LETTERS[-limit:])


def clear_dead_letters() -> None:
    """Clear the in-process dead-letter buffer (tests / ops)."""
    _DEAD_LETTERS.clear()


@dataclass(frozen=True)
class JobResult:
    """Outcome of a job run."""

    job_name: str
    status: str  # succeeded | failed | dead_lettered
    attempts: int
    duration_ms: float
    error: str | None = None
    value: Any = None


class JobRunner:
    """Execute a callable with retries and structured job logging."""

    def __init__(
        self,
        *,
        max_attempts: int = 3,
        backoff_seconds: float = 0.25,
        retriable: tuple[type[BaseException], ...] = (Exception,),
    ) -> None:
        self.max_attempts = max(1, max_attempts)
        self.backoff_seconds = max(0.0, backoff_seconds)
        self.retriable = retriable

    def run(
        self,
        job_name: str,
        fn: Callable[[], T],
        *,
        payload: dict[str, Any] | None = None,
    ) -> JobResult:
        """Run ``fn`` with retry/backoff; dead-letter on exhaustion."""
        started = time.perf_counter()
        last_error: BaseException | None = None
        for attempt in range(1, self.max_attempts + 1):
            logger.info(
                "job_start name=%s attempt=%s/%s",
                job_name,
                attempt,
                self.max_attempts,
            )
            try:
                value = fn()
                duration_ms = round((time.perf_counter() - started) * 1000, 1)
                logger.info(
                    "job_success name=%s attempt=%s duration_ms=%s",
                    job_name,
                    attempt,
                    duration_ms,
                )
                return JobResult(
                    job_name=job_name,
                    status="succeeded",
                    attempts=attempt,
                    duration_ms=duration_ms,
                    value=value,
                )
            except self.retriable as exc:
                last_error = exc
                logger.warning(
                    "job_failure name=%s attempt=%s error=%s",
                    job_name,
                    attempt,
                    exc.__class__.__name__,
                )
                if attempt < self.max_attempts and self.backoff_seconds:
                    time.sleep(self.backoff_seconds * attempt)

        duration_ms = round((time.perf_counter() - started) * 1000, 1)
        error_text = (
            f"{last_error.__class__.__name__}: {last_error}"
            if last_error is not None
            else "unknown"
        )
        record = DeadLetterRecord(
            job_name=job_name,
            attempts=self.max_attempts,
            error=error_text,
            failed_at=datetime.now(UTC).isoformat(),
            payload=dict(payload or {}),
        )
        _DEAD_LETTERS.append(record)
        logger.error(
            "job_dead_letter name=%s attempts=%s error=%s",
            job_name,
            self.max_attempts,
            error_text,
        )
        return JobResult(
            job_name=job_name,
            status="dead_lettered",
            attempts=self.max_attempts,
            duration_ms=duration_ms,
            error=error_text,
        )
