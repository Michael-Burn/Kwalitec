"""Study Insights dual-run diagnostics (EP-002.1 helper + EP-002.4 live side-car).

Compares legacy ``generate_recommendations`` with Twin ``build_study_insights``.
Diagnostic only — never changes production responses or student UX.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from contextvars import ContextVar
from copy import deepcopy
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain.contracts import (
    API_BUILD_STUDY_INSIGHTS,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    get_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext

logger = logging.getLogger(__name__)

_PRODUCTION_ENVS = frozenset({"production", "prod"})

# Prevent nested dual-run while a comparison is already in flight.
_DUAL_RUN_ACTIVE: ContextVar[bool] = ContextVar(
    "ep0024_study_insights_dual_run_active", default=False
)

# Request-scoped dedupe key prefix (Flask ``g`` when available).
_REQUEST_DEDUPE_ATTR = "_ep0024_study_insights_dual_run_users"

_TWIN_FIELD_KEYS: tuple[str, ...] = (
    "todays_key_focus",
    "greatest_risk",
    "recommended_next_action",
    "strongest_area",
    "workload_explanation",
    "readiness_explanation",
    "motivational_progress_summary",
)


def is_dual_run_diagnostics_eligible(
    *,
    environ: dict[str, str] | None = None,
) -> bool:
    """True when Twin is ON and the process is not production."""
    env = environ if environ is not None else os.environ
    flags = resolve_v2_feature_flags(environ=env)
    if not flags.ENABLE_DIGITAL_TWIN:
        return False
    flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
    app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"
    return app_env not in _PRODUCTION_ENVS


def fingerprint_payload(payload: Any) -> str:
    """Stable opaque fingerprint of a serialisable payload (no PII emphasis)."""
    try:
        material = json.dumps(
            payload,
            sort_keys=True,
            default=str,
            separators=(",", ":"),
        )
    except TypeError:
        material = repr(payload)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _legacy_categories(legacy_payload: Any) -> tuple[str, ...]:
    if not isinstance(legacy_payload, list):
        return ()
    categories: list[str] = []
    seen: set[str] = set()
    for row in legacy_payload:
        if not isinstance(row, dict):
            continue
        category = str(row.get("category") or "").strip()
        if category and category not in seen:
            seen.add(category)
            categories.append(category)
    return tuple(sorted(categories))


def _twin_field_ids(twin_payload: Any) -> tuple[str, ...]:
    if not isinstance(twin_payload, dict):
        return ()
    present: list[str] = []
    for key in _TWIN_FIELD_KEYS:
        value = twin_payload.get(key)
        if value is not None:
            present.append(key)
    return tuple(present)


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


def _request_already_ran(user_id: int) -> bool:
    """Return True when dual-run already executed for this user in the request."""
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


def compare_legacy_vs_build(
    *,
    legacy_payload: Any,
    build_payload: Any,
    user_id: int,
    api_name: str = API_BUILD_STUDY_INSIGHTS,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    legacy_latency_ms: float | None = None,
    twin_latency_ms: float | None = None,
    twin_exception: bool = False,
) -> dict[str, Any] | None:
    """Compare legacy vs Twin payloads and emit dual-run telemetry when eligible.

    Returns a diagnostic dict, or ``None`` when dual-run is not eligible
    (production or Twin OFF). Never mutates inputs.
    """
    env = environ if environ is not None else dict(os.environ)
    if not is_dual_run_diagnostics_eligible(environ=env):
        return None

    flags = resolve_v2_feature_flags(environ=env)
    ids = CorrelationContext.current()
    legacy_fp = fingerprint_payload(legacy_payload)
    build_fp = fingerprint_payload(build_payload)
    match = legacy_fp == build_fp
    flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
    app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"

    legacy_unavailable = legacy_payload is None or (
        isinstance(legacy_payload, list) and len(legacy_payload) == 0
    )
    twin_unavailable = build_payload is None
    codes = _limitation_codes(build_payload)
    confidence = _confidence_level(build_payload)
    categories = _legacy_categories(legacy_payload)
    twin_fields = _twin_field_ids(build_payload)

    comparison: dict[str, Any] = {
        "api_name": api_name,
        "student_id": str(user_id),
        "legacy_fingerprint": legacy_fp,
        "build_fingerprint": build_fp,
        "twin_fingerprint": build_fp,
        "fingerprints_match": match,
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
        "legacy_unavailable": bool(legacy_unavailable),
        "twin_unavailable": bool(twin_unavailable),
        "limitation_codes": list(codes),
        "confidence_level": confidence,
        "confidence_available": bool(confidence),
        "legacy_categories": list(categories),
        "twin_field_ids": list(twin_fields),
        "correlation_id": ids.correlation_id or "",
        "causation_id": ids.causation_id or "",
        "twin_enabled": bool(flags.ENABLE_DIGITAL_TWIN),
        "authority_enabled": bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY),
        "twin_exception": bool(twin_exception),
    }

    sink = telemetry or get_consumer_chain_telemetry()
    sink.emit_dual_run(
        api_name=api_name,
        student_id=str(user_id),
        twin_enabled=bool(flags.ENABLE_DIGITAL_TWIN),
        authority_enabled=bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY),
        legacy_fingerprint=legacy_fp,
        build_fingerprint=build_fp,
        fingerprints_match=match,
        environment=app_env,
        legacy_latency_ms=comparison["legacy_latency_ms"],
        twin_latency_ms=comparison["twin_latency_ms"],
        legacy_unavailable=bool(legacy_unavailable),
        twin_unavailable=bool(twin_unavailable),
        limitation_codes=codes,
        confidence_level=confidence,
        confidence_available=bool(confidence),
        legacy_categories=categories,
        twin_field_ids=twin_fields,
        correlation_id=ids.correlation_id or "",
        causation_id=ids.causation_id or "",
    )

    try:
        from app.infrastructure.adapters.consumer_chain.dual_run_health import (
            get_study_insights_dual_run_health_metrics,
        )

        get_study_insights_dual_run_health_metrics().record(comparison)
    except Exception:  # noqa: BLE001
        logger.debug("study_insights_dual_run_metrics_failed", exc_info=True)

    return comparison


def run_study_insights_dual_run(
    user_id: int,
    legacy_recommendations: list[dict],
    *,
    legacy_latency_ms: float | None = None,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    build_study_insights: Any | None = None,
    skip_request_dedupe: bool = False,
) -> dict[str, Any] | None:
    """Execute Twin ``build_study_insights`` beside an already-computed legacy list.

    Fail-open: Twin errors are swallowed. Never mutates ``legacy_recommendations``.
    Returns the comparison dict, or ``None`` when ineligible / deduped / nested.
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
        from app.services.recommendation_service import RecommendationService

        builder = build_study_insights or RecommendationService.build_study_insights
        started = time.perf_counter()
        try:
            twin_payload = builder(user_id)
        except Exception:  # noqa: BLE001 — never affect student path
            twin_exception = True
            twin_payload = None
            logger.debug(
                "study_insights_dual_run_twin_failed user_id=%s",
                user_id,
                exc_info=True,
            )
        twin_latency_ms = (time.perf_counter() - started) * 1000.0

        # Deep-copy fingerprint material so Twin cannot share mutable refs.
        legacy_snapshot = deepcopy(list(legacy_recommendations))
        return compare_legacy_vs_build(
            legacy_payload=legacy_snapshot,
            build_payload=twin_payload,
            user_id=user_id,
            api_name=API_BUILD_STUDY_INSIGHTS,
            telemetry=telemetry,
            environ=env,
            legacy_latency_ms=legacy_latency_ms,
            twin_latency_ms=twin_latency_ms,
            twin_exception=twin_exception,
        )
    finally:
        _DUAL_RUN_ACTIVE.reset(token)


def diagnostic_compare_study_insights(
    user_id: int,
    *,
    limit: int = 5,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
) -> dict[str, Any] | None:
    """Run legacy recommendations vs ``build_study_insights`` comparison.

    Intended for non-prod ops / tests. Skips the live side-car inside
    ``generate_recommendations`` so Twin executes exactly once here.
    Returns ``None`` when dual-run diagnostics are ineligible.
    """
    env = environ if environ is not None else dict(os.environ)
    if not is_dual_run_diagnostics_eligible(environ=env):
        return None

    from app.services.recommendation_service import RecommendationService

    token = _DUAL_RUN_ACTIVE.set(True)
    try:
        started = time.perf_counter()
        legacy = RecommendationService.generate_recommendations(user_id, limit=limit)
        legacy_latency_ms = (time.perf_counter() - started) * 1000.0
    finally:
        _DUAL_RUN_ACTIVE.reset(token)

    return run_study_insights_dual_run(
        user_id,
        legacy,
        legacy_latency_ms=legacy_latency_ms,
        telemetry=telemetry,
        environ=env,
        skip_request_dedupe=True,
    )
