"""Readiness Intelligence dual-run diagnostics (EP-002.6).

Compares legacy readiness surface (score + weak/strong topics) with Twin
``build_readiness_intelligence``. Diagnostic only — never changes student UX.
"""

from __future__ import annotations

import logging
import os
import time
from contextvars import ContextVar
from copy import deepcopy
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain.contracts import (
    API_BUILD_READINESS_INTELLIGENCE,
)
from app.infrastructure.adapters.consumer_chain.dual_run import (
    fingerprint_payload,
    is_dual_run_diagnostics_eligible,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    get_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext

logger = logging.getLogger(__name__)

_DUAL_RUN_ACTIVE: ContextVar[bool] = ContextVar(
    "ep0026_readiness_dual_run_active", default=False
)

_REQUEST_DEDUPE_ATTR = "_ep0026_readiness_dual_run_users"

_SCORE_AGREEMENT_TOLERANCE = 10.0


def is_readiness_dual_run_active() -> bool:
    """True while a readiness dual-run comparison is in flight."""
    return bool(_DUAL_RUN_ACTIVE.get())


def _limitation_codes(twin_payload: Any) -> tuple[str, ...]:
    if not isinstance(twin_payload, dict):
        return ()
    codes_raw = twin_payload.get("limitations_codes") or twin_payload.get(
        "limitations"
    ) or ()
    if isinstance(codes_raw, str):
        return (codes_raw,) if codes_raw else ()
    return tuple(str(c) for c in codes_raw if c)


def _confidence_level(twin_payload: Any) -> str:
    if not isinstance(twin_payload, dict):
        return ""
    return str(twin_payload.get("confidence_level") or "").strip()


def _legacy_score(legacy_surface: Any) -> float | None:
    if not isinstance(legacy_surface, dict):
        return None
    readiness = legacy_surface.get("readiness")
    if isinstance(readiness, dict) and readiness.get("score") is not None:
        try:
            return float(readiness["score"])
        except (TypeError, ValueError):
            return None
    return None


def _twin_score(twin_payload: Any) -> float | None:
    if not isinstance(twin_payload, dict):
        return None
    value = twin_payload.get("readiness_score")
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _topic_ids_from_rows(rows: Any) -> tuple[str, ...]:
    if not isinstance(rows, list):
        return ()
    ids: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        topic_id = str(row.get("topic_id") or "").strip()
        if topic_id and topic_id not in seen:
            seen.add(topic_id)
            ids.append(topic_id)
    return tuple(ids)


def _twin_area_ids(twin_payload: Any, *, key: str) -> tuple[str, ...]:
    if not isinstance(twin_payload, dict):
        return ()
    return _topic_ids_from_rows(twin_payload.get(key) or [])


def _score_agreement(
    legacy_score: float | None, twin_score: float | None
) -> bool:
    if legacy_score is None and twin_score is None:
        return True
    if legacy_score is None or twin_score is None:
        return False
    return abs(legacy_score - twin_score) <= _SCORE_AGREEMENT_TOLERANCE


def _request_already_ran(user_id: int) -> bool:
    try:
        from flask import g, has_request_context

        if not has_request_context():
            return False
        seen = getattr(g, _REQUEST_DEDUPE_ATTR, None)
        if seen is None:
            seen = set()
            setattr(g, _REQUEST_DEDUPE_ATTR, seen)
        if user_id in seen:
            return True
        seen.add(user_id)
        return False
    except Exception:  # noqa: BLE001 — dual-run must never break student path
        return False


def compare_legacy_vs_readiness_intelligence(
    *,
    legacy_surface: Any,
    twin_payload: Any,
    user_id: int,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    legacy_latency_ms: float | None = None,
    twin_latency_ms: float | None = None,
    twin_exception: bool = False,
) -> dict[str, Any] | None:
    """Compare legacy readiness surface vs Twin assessment; emit dual-run telemetry."""
    env = environ if environ is not None else dict(os.environ)
    if not is_dual_run_diagnostics_eligible(environ=env):
        return None

    flags = resolve_v2_feature_flags(environ=env)
    ids = CorrelationContext.current()
    legacy_fp = fingerprint_payload(legacy_surface)
    twin_fp = fingerprint_payload(twin_payload)
    flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
    app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"

    legacy_score = _legacy_score(legacy_surface)
    twin_score = _twin_score(twin_payload)
    codes = _limitation_codes(twin_payload)
    confidence = _confidence_level(twin_payload)

    legacy_weak = ()
    legacy_strong = ()
    if isinstance(legacy_surface, dict):
        legacy_weak = _topic_ids_from_rows(legacy_surface.get("weakest_topics"))
        legacy_strong = _topic_ids_from_rows(legacy_surface.get("strongest_topics"))
    twin_weak = _twin_area_ids(twin_payload, key="weakest_areas")
    twin_strong = _twin_area_ids(twin_payload, key="strongest_areas")

    readiness_agreement = _score_agreement(legacy_score, twin_score)
    confidence_agreement = bool(confidence) if twin_score is not None else True
    limitation_agreement = True  # diagnostic: codes captured for ops
    area_overlap = bool(
        set(legacy_weak + legacy_strong) & set(twin_weak + twin_strong)
    ) or (not (legacy_weak or legacy_strong or twin_weak or twin_strong))

    comparison: dict[str, Any] = {
        "api_name": API_BUILD_READINESS_INTELLIGENCE,
        "student_id": str(user_id),
        "legacy_fingerprint": legacy_fp,
        "build_fingerprint": twin_fp,
        "twin_fingerprint": twin_fp,
        "fingerprints_match": legacy_fp == twin_fp,
        "environment": app_env,
        "diagnostic_only": True,
        "influences_student": False,
        "legacy_latency_ms": (
            round(float(legacy_latency_ms), 3)
            if legacy_latency_ms is not None
            else None
        ),
        "twin_latency_ms": (
            round(float(twin_latency_ms), 3) if twin_latency_ms is not None else None
        ),
        "legacy_unavailable": legacy_surface is None,
        "twin_unavailable": twin_payload is None,
        "limitation_codes": list(codes),
        "confidence_level": confidence,
        "confidence_available": bool(confidence),
        "legacy_score": legacy_score,
        "twin_score": twin_score,
        "readiness_agreement": readiness_agreement,
        "confidence_agreement": confidence_agreement,
        "limitation_agreement": limitation_agreement,
        "area_overlap": area_overlap,
        "legacy_weak_topic_ids": list(legacy_weak),
        "legacy_strong_topic_ids": list(legacy_strong),
        "twin_weak_topic_ids": list(twin_weak),
        "twin_strong_topic_ids": list(twin_strong),
        "correlation_id": ids.correlation_id or "",
        "causation_id": ids.causation_id or "",
        "twin_enabled": bool(flags.ENABLE_DIGITAL_TWIN),
        "authority_enabled": bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY),
        "twin_exception": bool(twin_exception),
    }

    sink = telemetry or get_consumer_chain_telemetry()
    sink.emit_dual_run(
        api_name=API_BUILD_READINESS_INTELLIGENCE,
        student_id=str(user_id),
        twin_enabled=bool(flags.ENABLE_DIGITAL_TWIN),
        authority_enabled=bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY),
        legacy_fingerprint=legacy_fp,
        build_fingerprint=twin_fp,
        fingerprints_match=legacy_fp == twin_fp,
        environment=app_env,
        legacy_latency_ms=comparison["legacy_latency_ms"],
        twin_latency_ms=comparison["twin_latency_ms"],
        legacy_unavailable=bool(comparison["legacy_unavailable"]),
        twin_unavailable=bool(comparison["twin_unavailable"]),
        limitation_codes=codes,
        confidence_level=confidence,
        confidence_available=bool(confidence),
        legacy_categories=(),
        twin_field_ids=(
            ("readiness_score",) if twin_score is not None else ()
        ),
        correlation_id=ids.correlation_id or "",
        causation_id=ids.causation_id or "",
    )

    try:
        from app.infrastructure.adapters.consumer_chain import (
            readiness_dual_run_health as _health,
        )

        _health.get_readiness_dual_run_health_metrics().record(comparison)
    except Exception:  # noqa: BLE001
        logger.debug("readiness_dual_run_metrics_failed", exc_info=True)

    return comparison


def run_readiness_intelligence_dual_run(
    user_id: int,
    legacy_surface: dict[str, Any],
    *,
    legacy_latency_ms: float | None = None,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    build_readiness_intelligence: Any | None = None,
    skip_request_dedupe: bool = False,
) -> dict[str, Any] | None:
    """Execute Twin ``build_readiness_intelligence`` beside an already-computed surface.

    Fail-open: Twin errors are swallowed. Never mutates ``legacy_surface``.
    """
    env = environ if environ is not None else dict(os.environ)
    if not is_dual_run_diagnostics_eligible(environ=env):
        return None
    if _DUAL_RUN_ACTIVE.get():
        return None
    if not skip_request_dedupe and _request_already_ran(user_id):
        return None

    token = _DUAL_RUN_ACTIVE.set(True)
    twin_payload: Any = None
    twin_latency_ms = 0.0
    twin_exception = False
    try:
        from app.services.readiness_service import ReadinessService

        builder = (
            build_readiness_intelligence
            or ReadinessService.build_readiness_intelligence
        )
        started = time.perf_counter()
        try:
            twin_payload = builder(user_id)
        except Exception:  # noqa: BLE001 — never affect student path
            twin_exception = True
            twin_payload = None
            logger.debug(
                "readiness_dual_run_twin_failed user_id=%s",
                user_id,
                exc_info=True,
            )
        twin_latency_ms = (time.perf_counter() - started) * 1000.0

        return compare_legacy_vs_readiness_intelligence(
            legacy_surface=deepcopy(legacy_surface),
            twin_payload=twin_payload,
            user_id=user_id,
            telemetry=telemetry,
            environ=env,
            legacy_latency_ms=legacy_latency_ms,
            twin_latency_ms=twin_latency_ms,
            twin_exception=twin_exception,
        )
    finally:
        _DUAL_RUN_ACTIVE.reset(token)
