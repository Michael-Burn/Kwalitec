"""Observation wrapper for Twin-gated ``build_*`` APIs.

Records invocation, duration, outcome, availability, and flag state without
mutating return values or educational behaviour.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, TypeVar

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain.contracts import (
    OUTCOME_LIMITATION,
    OUTCOME_SUCCESS,
    OUTCOME_UNAVAILABLE,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    get_consumer_chain_telemetry,
)

T = TypeVar("T")


def _flag_snapshot(
    *, environ: dict[str, str] | None = None
) -> tuple[bool, bool]:
    flags = resolve_v2_feature_flags(environ=environ)
    return bool(flags.ENABLE_DIGITAL_TWIN), bool(
        flags.ENABLE_DIGITAL_TWIN_AUTHORITY
    )


def classify_build_result(
    result: Any,
) -> tuple[str, bool, tuple[str, ...], bool | None]:
    """Classify a ``build_*`` return value for observability.

    Returns:
        (outcome, returned_none, limitation_codes, confidence_available)
    """
    if result is None:
        return OUTCOME_UNAVAILABLE, True, (), None
    if not isinstance(result, dict):
        return OUTCOME_SUCCESS, False, (), None

    codes_raw = result.get("limitations_codes") or result.get("limitations") or ()
    if isinstance(codes_raw, str):
        codes: tuple[str, ...] = (codes_raw,) if codes_raw else ()
    else:
        codes = tuple(str(c) for c in codes_raw if c)

    confidence_available: bool | None = None
    if "confidence_level" in result:
        confidence_available = bool(result.get("confidence_level"))
    elif "confidence" in result:
        confidence_available = result.get("confidence") is not None

    if codes:
        return OUTCOME_LIMITATION, False, codes, confidence_available
    return OUTCOME_SUCCESS, False, (), confidence_available


def observe_build_api(
    *,
    service_name: str,
    api_name: str,
    user_id: int,
    call: Callable[[], T],
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
) -> T:
    """Invoke ``call`` and emit structured observability around it.

    Preserves the exact return value / exception of ``call``. Never alters
    student-facing payloads.
    """
    sink = telemetry or get_consumer_chain_telemetry()
    twin_enabled, authority_enabled = _flag_snapshot(environ=environ)
    timestamp = datetime.now(tz=UTC).isoformat()
    student_id = str(user_id)

    sink.emit_requested(
        service_name=service_name,
        api_name=api_name,
        student_id=student_id,
        twin_enabled=twin_enabled,
        authority_enabled=authority_enabled,
        timestamp=timestamp,
    )

    started = time.perf_counter()
    try:
        result = call()
    except Exception as exc:  # noqa: BLE001 — observational boundary
        duration_ms = (time.perf_counter() - started) * 1000.0
        sink.emit_failed(
            service_name=service_name,
            api_name=api_name,
            student_id=student_id,
            twin_enabled=twin_enabled,
            authority_enabled=authority_enabled,
            duration_ms=duration_ms,
            error_code=type(exc).__name__,
            error_message=str(exc),
            timestamp=datetime.now(tz=UTC).isoformat(),
        )
        raise

    duration_ms = (time.perf_counter() - started) * 1000.0
    outcome, returned_none, codes, confidence = classify_build_result(result)
    sink.emit_completed(
        service_name=service_name,
        api_name=api_name,
        student_id=student_id,
        twin_enabled=twin_enabled,
        authority_enabled=authority_enabled,
        outcome=outcome,
        duration_ms=duration_ms,
        returned_none=returned_none,
        limitation_codes=codes,
        confidence_available=confidence,
        timestamp=datetime.now(tz=UTC).isoformat(),
    )
    return result
